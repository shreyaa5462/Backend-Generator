import os

from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

UPLOAD_DIR = "app/uploads"

GENERATED_DIR = "app/generated"


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    GENERATED_DIR,
    exist_ok=True
)