from typing import TypedDict, Any

from langgraph.graph import (
    StateGraph,
    END
)

from app.services.llm_service import LLMService

from app.services.rag_service import RAGService


class GraphState(TypedDict):

    srd: str

    retriever: Any

    analysis: dict

    blueprint: dict

    models: dict

    schemas: dict

    crud: dict

    database: dict

    apis: dict

    main: dict


# ============================================================
# REQUIREMENT
# ============================================================

def requirement_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find the project requirements,
        modules, entities, database tables,
        authentication requirements and APIs.
        """
    )

    analysis = LLMService.analyze_srd(
        context
    )

    return {
        **state,
        "analysis": analysis
    }


# ============================================================
# BLUEPRINT
# ============================================================

def blueprint_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find information about system architecture,
        modules, technologies, database,
        authentication and backend structure.
        """
    )

    blueprint = LLMService.generate_blueprint(
        state["analysis"],
        context
    )

    return {
        **state,
        "blueprint": blueprint
    }


# ============================================================
# MODELS
# ============================================================

def model_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find database entities,
        table fields,
        relationships,
        primary keys and foreign keys.
        """
    )

    models = LLMService.generate_models(
        state["blueprint"],
        context
    )

    return {
        **state,
        "models": models
    }


# ============================================================
# SCHEMAS
# ============================================================

def schema_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find request fields,
        response fields,
        validation requirements
        and user input requirements.
        """
    )

    schemas = LLMService.generate_schemas(
        state["blueprint"],
        state["models"],
        context
    )

    return {
        **state,
        "schemas": schemas
    }


# ============================================================
# CRUD
# ============================================================

def crud_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find business operations,
        create, update, delete,
        borrow, return and search behavior.
        """
    )

    crud = LLMService.generate_crud(
        state["blueprint"],
        state["models"],
        state["schemas"],
        context
    )

    return {
        **state,
        "crud": crud
    }


# ============================================================
# DATABASE
# ============================================================

def database_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find database requirements,
        PostgreSQL requirements,
        tables and persistence requirements.
        """
    )

    database = LLMService.generate_database(
        state["blueprint"],
        context
    )

    return {
        **state,
        "database": database
    }


# ============================================================
# API
# ============================================================

def api_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find API endpoints,
        HTTP methods,
        request parameters,
        responses,
        search and business operations.
        """
    )

    apis = LLMService.generate_apis(
        state["blueprint"],
        state["models"],
        state["schemas"],
        context
    )

    return {
        **state,
        "apis": apis
    }


# ============================================================
# MAIN
# ============================================================

def main_node(
    state: GraphState
):

    context = RAGService.get_context(
        state["retriever"],
        """
        Find API modules and application
        entry-point requirements.
        """
    )

    main = LLMService.generate_main(
        state["blueprint"],
        state["apis"],
        context
    )

    return {
        **state,
        "main": main
    }


# ============================================================
# LANGGRAPH
# ============================================================

workflow = StateGraph(
    GraphState
)


workflow.add_node(
    "requirement",
    requirement_node
)

workflow.add_node(
    "blueprint",
    blueprint_node
)

workflow.add_node(
    "models",
    model_node
)

workflow.add_node(
    "schema",
    schema_node
)

workflow.add_node(
    "crud",
    crud_node
)

workflow.add_node(
    "database",
    database_node
)

workflow.add_node(
    "api",
    api_node
)

workflow.add_node(
    "main",
    main_node
)


workflow.set_entry_point(
    "requirement"
)


workflow.add_edge(
    "requirement",
    "blueprint"
)

workflow.add_edge(
    "blueprint",
    "models"
)

workflow.add_edge(
    "models",
    "schema"
)

workflow.add_edge(
    "schema",
    "crud"
)

workflow.add_edge(
    "crud",
    "database"
)

workflow.add_edge(
    "database",
    "api"
)

workflow.add_edge(
    "api",
    "main"
)

workflow.add_edge(
    "main",
    END
)


graph = workflow.compile()