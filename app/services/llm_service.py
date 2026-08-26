import time

from groq import RateLimitError
from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY

from app.prompts import (
    requirement_prompt,
    blueprint_prompt,
    model_prompt,
    schema_prompt,
    crud_prompt,
    database_prompt,
    api_prompt,
    main_prompt
)

from app.utils import parse_json


class LLMService:

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0
    )

    @staticmethod
    def invoke(
        prompt: str,
        max_tokens: int
    ):

        model = ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=GROQ_API_KEY,
            temperature=0,
            max_tokens=max_tokens,
            model_kwargs={
                "response_format": {
                    "type": "json_object"
                }
            }
        )

        for attempt in range(3):

            try:

                response = model.invoke(
                    prompt
                )

                return response

            except RateLimitError as error:

                if attempt == 2:
                    raise error

                wait_time = 15 * (attempt + 1)

                print(
                    f"Rate limit hit. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(
                    wait_time
                )

    # ==========================================
    # REQUIREMENT
    # ==========================================

    @staticmethod
    def analyze_srd(
        context: str
    ):

        prompt = requirement_prompt.format(
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=1200
        )

        return parse_json(
            response.content
        )

    # ==========================================
    # BLUEPRINT
    # ==========================================

    @staticmethod
    def generate_blueprint(
        requirements: dict,
        context: str
    ):

        prompt = blueprint_prompt.format(
            requirements=requirements,
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=1800
        )

        return parse_json(
            response.content
        )

    # ==========================================
    # MODELS
    # ==========================================

    @staticmethod
    def generate_models(
        blueprint: dict,
        context: str
    ):

        prompt = model_prompt.format(
            blueprint=blueprint,
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=5000
        )

        return parse_json(
            response.content
        )

    # ==========================================
    # SCHEMAS
    # ==========================================

    @staticmethod
    def generate_schemas(
        blueprint: dict,
        models: dict,
        context: str
    ):

        prompt = schema_prompt.format(
            blueprint=blueprint,
            models=models,
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=5000
        )

        return parse_json(
            response.content
        )

    # ==========================================
    # CRUD
    # ==========================================

    @staticmethod
    def generate_crud(
        blueprint: dict,
        models: dict,
        schemas: dict,
        context: str
    ):

        prompt = crud_prompt.format(
            blueprint=blueprint,
            models=models,
            schemas=schemas,
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=5500
        )

        return parse_json(
            response.content
        )

    # ==========================================
    # DATABASE
    # ==========================================

    @staticmethod
    def generate_database(
        blueprint: dict,
        context: str
    ):

        prompt = database_prompt.format(
            blueprint=blueprint,
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=1800
        )

        print(
            "\n========== DATABASE RESPONSE =========="
        )
        print(
            repr(response.content)
        )
        print(
            "=======================================\n"
        )

        return parse_json(
            response.content
        )

    # ==========================================
    # API
    # ==========================================

    @staticmethod
    def generate_apis(
        blueprint: dict,
        models: dict,
        schemas: dict,
        context: str
    ):

        prompt = api_prompt.format(
            blueprint=blueprint,
            models=models,
            schemas=schemas,
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=5000
        )

        return parse_json(
            response.content
        )

    # ==========================================
    # MAIN
    # ==========================================

    @staticmethod
    def generate_main(
        blueprint: dict,
        apis: dict,
        context: str
    ):

        prompt = main_prompt.format(
            blueprint=blueprint,
            apis=apis,
            context=context
        )

        response = LLMService.invoke(
            prompt,
            max_tokens=2000
        )

        return parse_json(
            response.content
        )