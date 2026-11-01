import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.security import decode_token
from app.core.config import settings

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2YTdkZjNlMWRmY2FmZGY1NDBlODA0ZmYiLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3ODY4ODc3MjN9.wE4zYQXc0BEoDBn-iuiY3KjH8Rrm_XnJShTV7RrVyzw"
print("secret:", settings.secret_key)
print("algorithm:", settings.algorithm)
payload = decode_token(token)
print("payload:", payload)
