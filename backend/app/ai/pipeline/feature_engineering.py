class FeatureEngineering:
    @staticmethod
    def extract_features(text: str) -> dict:
        return {"word_count": len(text.split()), "char_count": len(text)}
