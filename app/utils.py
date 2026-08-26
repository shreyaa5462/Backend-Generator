import json
import os

from docx import Document


def read_docx(file_path: str) -> str:

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            paragraphs.append(
                paragraph.text.strip()
            )

    return "\n".join(paragraphs)


def parse_json(content: str) -> dict:

    if not content:

        raise ValueError(
            "LLM returned empty response"
        )

    content = content.strip()

    # Remove markdown fences
    if content.startswith("```json"):

        content = content[7:].strip()

    elif content.startswith("```"):

        content = content[3:].strip()

    if content.endswith("```"):

        content = content[:-3].strip()

    try:

        return json.loads(content)

    except json.JSONDecodeError as error:

        print("\n========== INVALID JSON ==========")
        print(content)
        print("==================================\n")

        raise ValueError(
            f"LLM returned invalid JSON: {error}"
        ) from error


def create_project_structure(
    project_path: str,
    folders: list
):

    os.makedirs(
        project_path,
        exist_ok=True
    )

    for folder in folders:

        if not folder:
            continue

        folder_path = os.path.join(
            project_path,
            folder
        )

        # Ignore file paths here
        if "." in os.path.basename(folder_path):
            continue

        os.makedirs(
            folder_path,
            exist_ok=True
        )


def save_generated_files(
    project_path: str,
    files: list
):

    for file in files:

        file_path = os.path.join(
            project_path,
            file["path"]
        )

        parent_directory = os.path.dirname(
            file_path
        )

        os.makedirs(
            parent_directory,
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as output_file:

            output_file.write(
                file.get("content", "")
            )