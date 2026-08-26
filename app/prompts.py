from langchain_core.prompts import PromptTemplate


# ============================================================
# REQUIREMENT
# ============================================================

requirement_prompt = PromptTemplate.from_template(
    """
You are an expert Backend Software Architect.

Analyze the relevant sections of the Software Requirement
Specification provided below.

IMPORTANT:
Use only the provided context.
Do not invent requirements.

Return ONLY valid JSON.
Do not return markdown.
Do not return ```json.
Do not return explanations.

Use exactly this structure:

{{
    "project_name": "",
    "description": "",
    "authentication": "",
    "modules": [],
    "database_tables": [],
    "entities": [],
    "apis": []
}}

Relevant SRD Context:

{context}
"""
)


# ============================================================
# BLUEPRINT
# ============================================================

blueprint_prompt = PromptTemplate.from_template(
    """
You are a senior backend architect.

Using the requirement analysis and relevant SRD context,
create the backend blueprint.

Technology:

- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Pydantic v2

IMPORTANT:
Use only the provided information.
Do not repeat the entire SRD.

Return ONLY valid JSON.
Do not return markdown.
Do not return explanations.

Use exactly:

{{
    "project_name": "",
    "framework": "FastAPI",
    "database": "PostgreSQL",
    "authentication": "",
    "folder_structure": [],
    "modules": [],
    "entities": [],
    "apis": []
}}

Requirement Analysis:

{requirements}

Relevant SRD Context:

{context}
"""
)


# ============================================================
# MODELS
# ============================================================

model_prompt = PromptTemplate.from_template(
    """
You are a senior FastAPI backend developer.

Generate SQLAlchemy 2.0 models based on the blueprint
and relevant SRD context.

Requirements:

1. Use SQLAlchemy 2.x.
2. Create entities from the blueprint.
3. Add appropriate columns.
4. Add primary keys.
5. Add foreign keys where required.
6. Add relationships where required.
7. Include required imports.
8. Generate valid Python.
9. Do not generate schemas.
10. Do not generate CRUD.
11. Do not generate API routes.

Return ONLY valid JSON.

Return exactly:

{{
    "files": [
        {{
            "path": "app/models/example.py",
            "content": "python code"
        }}
    ]
}}

Backend Blueprint:

{blueprint}

Relevant SRD Context:

{context}
"""
)


# ============================================================
# SCHEMAS
# ============================================================

schema_prompt = PromptTemplate.from_template(
    """
You are a senior FastAPI developer.

Generate Pydantic v2 schemas using the generated models,
blueprint and relevant SRD context.

Requirements:

1. Use Pydantic v2.
2. Generate Create schemas.
3. Generate Update schemas.
4. Generate Response schemas.
5. Do not expose passwords in response schemas.
6. Use ConfigDict(from_attributes=True) where required.
7. Include required imports.
8. Generate valid Python.

Return ONLY valid JSON.

Return exactly:

{{
    "files": [
        {{
            "path": "app/schemas/example.py",
            "content": "python code"
        }}
    ]
}}

Backend Blueprint:

{blueprint}

Generated Models:

{models}

Relevant SRD Context:

{context}
"""
)


# ============================================================
# CRUD
# ============================================================

crud_prompt = PromptTemplate.from_template(
    """
You are a senior FastAPI backend developer.

Generate CRUD operations for all required entities.

Requirements:

1. One CRUD file per entity.
2. Use SQLAlchemy Session.
3. Use generated models.
4. Use generated schemas.
5. Implement create.
6. Implement get by id.
7. Implement get all.
8. Implement update.
9. Implement delete.
10. Handle not-found cases.
11. Do not generate API routes.
12. Do not generate database configuration.

Return ONLY valid JSON.

Return exactly:

{{
    "files": [
        {{
            "path": "app/crud/example.py",
            "content": "python code"
        }}
    ]
}}

Backend Blueprint:

{blueprint}

Generated Models:

{models}

Generated Schemas:

{schemas}

Relevant SRD Context:

{context}
"""
)


# ============================================================
# DATABASE
# ============================================================

database_prompt = PromptTemplate.from_template(
    """
You are a senior FastAPI backend developer.

Generate the database layer.

Requirements:

1. PostgreSQL.
2. SQLAlchemy 2.x.
3. Read DATABASE_URL from environment variables.
4. Never hardcode credentials.
5. Create SQLAlchemy engine.
6. Create SessionLocal.
7. Create get_db dependency.
8. Generate initialization code if required.
9. Do not generate models.
10. Do not generate CRUD.
11. Do not generate API routes.

Generate:

- app/database/__init__.py
- app/database/session.py

Return ONLY valid JSON.

Return exactly:

{{
    "files": [
        {{
            "path": "app/database/__init__.py",
            "content": ""
        }},
        {{
            "path": "app/database/session.py",
            "content": "python code"
        }}
    ]
}}

Backend Blueprint:

{blueprint}

Relevant SRD Context:

{context}
"""
)


# ============================================================
# API
# ============================================================

api_prompt = PromptTemplate.from_template(
    """
You are an expert FastAPI backend developer.

Generate API route files based on the blueprint,
models, schemas and relevant SRD context.

Requirements:

1. Use APIRouter.
2. Use correct HTTP methods.
3. Use correct API paths.
4. Use generated CRUD functions.
5. Use generated Pydantic schemas.
6. Use Depends for database access.
7. Handle appropriate HTTP errors.
8. Include required imports.
9. Generate valid Python.

Return ONLY valid JSON.

Every file must contain:
- path
- content

Return exactly:

{{
    "files": [
        {{
            "path": "app/api/example.py",
            "content": "python code"
        }}
    ]
}}

Blueprint:

{blueprint}

Models:

{models}

Schemas:

{schemas}

Relevant SRD Context:

{context}
"""
)


# ============================================================
# MAIN
# ============================================================

main_prompt = PromptTemplate.from_template(
    """
You are a senior FastAPI developer.

Generate the application entry point and Docker configuration
for the backend project.

Generate these files:

1. app/main.py
2. app/api/__init__.py
3. Dockerfile
4. docker-compose.yml
5. requirements.txt

Docker requirements:

- Use Python 3.12
- Run FastAPI using Uvicorn
- Expose port 8000
- Use 0.0.0.0 inside container
- Do not hardcode secrets
- Read environment variables from environment
- Include required Python dependencies
- Keep Docker configuration production-ready

Return ONLY valid JSON.

Return exactly:

{{
    "files": [
        {{
            "path": "app/main.py",
            "content": "python code"
        }},
        {{
            "path": "app/api/__init__.py",
            "content": "python code"
        }},
        {{
            "path": "Dockerfile",
            "content": "dockerfile code"
        }},
        {{
            "path": "docker-compose.yml",
            "content": "yaml code"
        }},
        {{
            "path": "requirements.txt",
            "content": "requirements"
        }}
    ]
}}

Backend Blueprint:

{blueprint}

Generated APIs:

{apis}

Relevant SRD Context:

{context}
"""
)