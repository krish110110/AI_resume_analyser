import os
import pickle
import numpy as np
from typing import List, Dict


class SimilarityService:
    def __init__(self):
        self.model = None
        self.index = None
        self.job_embeddings = None
        self.job_metadata = None
        self._model_loaded = False
        self._index_built = False
    
    def _load_model(self):
        """Load the sentence transformer model lazily."""
        if self._model_loaded:
            return
        try:
            from sentence_transformers import SentenceTransformer
            model_name = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")
            self.model = SentenceTransformer(model_name)
            self._model_loaded = True
            print(f"Loaded sentence transformer: {model_name}")
        except Exception as e:
            print(f"Warning: Could not load sentence transformer: {e}")
            self.model = None
            self._model_loaded = True
    
    def _build_index(self):
        """Build FAISS index from job descriptions."""
        if self._index_built:
            return
        self._load_model()
        if self.model is None:
            self._index_built = True
            return
        try:
            import faiss
            import pandas as pd
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            jobs_path = os.path.join(base_dir, "ml", "datasets", "raw", "jobs.csv")
            
            if os.path.exists(jobs_path):
                df_jobs = pd.read_csv(jobs_path)
                
                # Create text for each job
                texts = []
                metadata = []
                for _, row in df_jobs.iterrows():
                    text = f"{row['title']} {row['description']} {row['skills']}"
                    texts.append(text)
                    metadata.append({
                        'id': row['id'],
                        'title': row['title'],
                        'company': row['company'],
                        'skills': row['skills']
                    })
                
                # Generate embeddings
                print(f"Generating embeddings for {len(texts)} jobs...")
                embeddings = self.model.encode(texts, show_progress_bar=True)
                
                # Build FAISS index
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
                faiss.normalize_L2(embeddings)
                self.index.add(embeddings)
                
                self.job_embeddings = embeddings
                self.job_metadata = metadata
                print(f"Built FAISS index with {self.index.ntotal} jobs")
            else:
                print("No jobs.csv found, similarity service will work with direct text comparison only")
        except Exception as e:
            print(f"Warning: Could not build FAISS index: {e}")
            self.index = None
        finally:
            self._index_built = True
    
    async def calculate_similarity(self, text: str, job_desc: str) -> float:
        """Calculate cosine similarity between resume text and job description."""
        self._load_model()
        if self.model is None:
            return 0.0
        
        # Encode both texts
        resume_emb = self.model.encode([text], convert_to_numpy=True)
        job_emb = self.model.encode([job_desc], convert_to_numpy=True)
        
        # Normalize for cosine similarity
        faiss.normalize_L2(resume_emb)
        faiss.normalize_L2(job_emb)
        
        # Cosine similarity
        similarity = np.dot(resume_emb[0], job_emb[0]) * 100
        return round(float(np.clip(similarity, 0, 100)), 1)
    
    async def get_similarity_breakdown(self, features: dict, job_features: dict) -> dict:
        """Get detailed similarity breakdown by section."""
        if self.model is None:
            return {"skills": 0.0, "experience": 0.0, "education": 0.0}
        
        breakdown = {}
        
        # Skills similarity
        resume_skills = " ".join(features.get("skills", []))
        job_skills = " ".join(job_features.get("skills", []))
        if resume_skills and job_skills:
            resume_emb = self.model.encode([resume_skills])
            job_emb = self.model.encode([job_skills])
            faiss.normalize_L2(resume_emb)
            faiss.normalize_L2(job_emb)
            breakdown["skills"] = round(float(np.dot(resume_emb[0], job_emb[0]) * 100), 1)
        else:
            breakdown["skills"] = 0.0
        
        # Experience similarity
        resume_exp = " ".join([str(e) for e in features.get("experience", [])])
        job_exp = job_features.get("description", "")
        if resume_exp and job_exp:
            resume_emb = self.model.encode([resume_exp])
            job_emb = self.model.encode([job_exp])
            faiss.normalize_L2(resume_emb)
            faiss.normalize_L2(job_emb)
            breakdown["experience"] = round(float(np.dot(resume_emb[0], job_emb[0]) * 100), 1)
        else:
            breakdown["experience"] = 0.0
        
        # Education similarity
        resume_edu = " ".join(features.get("education", []))
        job_edu = job_features.get("education", "")
        if resume_edu and job_edu:
            resume_emb = self.model.encode([resume_edu])
            job_emb = self.model.encode([job_edu])
            faiss.normalize_L2(resume_emb)
            faiss.normalize_L2(job_emb)
            breakdown["education"] = round(float(np.dot(resume_emb[0], job_emb[0]) * 100), 1)
        else:
            breakdown["education"] = 0.0
        
        return breakdown
    
    async def find_missing_keywords(self, text: str, job_desc: str) -> List[str]:
        """Find canonical skills in the job description that the resume lacks."""
        from app.ai.extraction.skill_extractor import SkillExtractor

        extractor = SkillExtractor()
        resume_skills = {s.lower() for s in await extractor.extract(text)}
        job_skills = await extractor.extract(job_desc)

        return [skill for skill in job_skills if skill.lower() not in resume_skills]
    
    async def find_similar_jobs(self, resume_text: str, top_k: int = 5) -> List[Dict]:
        """Find most similar jobs from the index."""
        if self.index is None or self.model is None:
            return []
        
        # Encode resume
        query_emb = self.model.encode([resume_text], convert_to_numpy=True)
        faiss.normalize_L2(query_emb)
        
        # Search
        scores, indices = self.index.search(query_emb, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.job_metadata):
                results.append({
                    "job": self.job_metadata[idx],
                    "similarity": round(float(score) * 100, 1)
                })
        
        return results