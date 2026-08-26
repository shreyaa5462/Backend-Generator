
# pip install chromadb langchain-chroma langchain-huggingface sentence-transformers

from fastapi import FastAPI

from app.routes import router
from app.logger import logger

app = FastAPI(

    title="Generative AI Backend Generator",

    version="1.0.0"

)


@app.on_event("startup")
def startup():

    logger.info(
        "Application Started"
    )


app.include_router(router)


@app.get("/")
def home():

    return {

        "message": "Welcome to Generative AI Backend Generator 🚀"

    }