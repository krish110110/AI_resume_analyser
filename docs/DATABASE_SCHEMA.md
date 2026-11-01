# Database Schema

## Collections

### users
| Field | Type | Description |
|-------|------|-------------|
| _id | ObjectId | Primary key |
| name | string | Full name |
| email | string | Unique email |
| hashed_password | string | Bcrypt hash |
| role | string | user or admin |
| is_active | boolean | Account status |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### resumes
| Field | Type | Description |
|-------|------|-------------|
| _id | ObjectId | Primary key |
| user_id | string | Owner user ID |
| filename | string | Original filename |
| file_path | string | Storage path |
| file_type | string | pdf or docx |
| file_size | int | Size in bytes |
| status | string | pending/processing/completed/failed |
| ats_score | float | ATS compatibility score |
| similarity_score | float | Job match score |
| skill_match_percentage | float | Skills match % |
| missing_keywords | array | Missing job keywords |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### job_descriptions
| Field | Type | Description |
|-------|------|-------------|
| _id | ObjectId | Primary key |
| title | string | Job title |
| company | string | Company name |
| description | string | Full job description |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### analyses
| Field | Type | Description |
|-------|------|-------------|
| _id | ObjectId | Primary key |
| resume_id | string | Resume reference |
| job_description_id | string | Job reference |
| parsed_data | object | Parsed resume sections |
| features | object | Extracted features |
| classification | object | Category and quality |
| scores | object | ATS, similarity, match scores |
| recommendations | array | Improvement suggestions |
| created_at | datetime | Creation timestamp |

### reports
| Field | Type | Description |
|-------|------|-------------|
| _id | ObjectId | Primary key |
| user_id | string | Owner user ID |
| resume_id | string | Resume reference |
| analysis_id | string | Analysis reference |
| filename | string | Resume filename |
| ats_score | float | ATS score |
| similarity_score | float | Similarity score |
| skill_match_percentage | float | Skills match % |
| skills | array | Extracted skills |
| missing_keywords | array | Missing keywords |
| recommendations | array | Recommendations |
| created_at | datetime | Creation timestamp |
