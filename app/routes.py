import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from app.config import (
    UPLOAD_DIR,
    GENERATED_DIR
)

from app.logger import logger

from app.schemas import UploadResponse

from app.utils import (
    read_docx,
    create_project_structure,
    save_generated_files
)

from app.workflow import graph

from app.services.rag_service import RAGService


router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse
)
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    try:

        # ==========================================
        # 1. SAVE FILE
        # ==========================================

        logger.info(
            f"Uploading {file.filename}"
        )

        os.makedirs(
            UPLOAD_DIR,
            exist_ok=True
        )

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        logger.info(
            "File uploaded successfully"
        )

        # ==========================================
        # 2. READ SRD
        # ==========================================

        text = read_docx(
            file_path
        )

        logger.info(
            "SRD Read Successfully"
        )

        # ==========================================
        # 3. CREATE RAG RETRIEVER
        # ==========================================

        retriever = RAGService.create_retriever(
            text
        )

        logger.info(
            "RAG retriever created successfully"
        )

        # ==========================================
        # 4. RUN EXISTING LANGGRAPH
        # ==========================================

        result = graph.invoke(
            {
                "srd": text,
                "retriever": retriever,

                "analysis": {},
                "blueprint": {},
                "models": {},
                "schemas": {},
                "crud": {},
                "database": {},
                "apis": {},
                "main": {}
            }
        )

        # ==========================================
        # 5. PROJECT DETAILS
        # ==========================================

        blueprint = result["blueprint"]

        project_name = blueprint.get(
            "project_name",
            "generated_project"
        )

        project_name = project_name.replace(
            " ",
            "_"
        )

        project_path = os.path.join(
            GENERATED_DIR,
            project_name
        )

        # ==========================================
        # 6. CREATE STRUCTURE
        # ==========================================

        folders = blueprint.get(
            "folder_structure",
            []
        )

        create_project_structure(
            project_path,
            folders
        )

        # ==========================================
        # 7. SAVE GENERATED FILES
        # ==========================================

        save_generated_files(
            project_path,
            result["models"].get(
                "files",
                []
            )
        )

        save_generated_files(
            project_path,
            result["schemas"].get(
                "files",
                []
            )
        )

        save_generated_files(
            project_path,
            result["crud"].get(
                "files",
                []
            )
        )

        save_generated_files(
            project_path,
            result["database"].get(
                "files",
                []
            )
        )

        save_generated_files(
            project_path,
            result["apis"].get(
                "files",
                []
            )
        )

        save_generated_files(
            project_path,
            result["main"].get(
                "files",
                []
            )
        )

        logger.info(
            "Complete backend project generated successfully"
        )

        # ==========================================
        # 8. RESPONSE
        # ==========================================

        return UploadResponse(

            message=(
                "Backend generated successfully"
            ),

            filename=file.filename,

            content={
                "project_path": project_path,
                "analysis": result["analysis"],
                "blueprint": result["blueprint"],
                "models": result["models"],
                "schemas": result["schemas"],
                "crud": result["crud"],
                "database": result["database"],
                "apis": result["apis"],
                "main": result["main"]
            }
        )

    except Exception as e:

        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )