import os
import uuid
from fastapi import UploadFile
from shutil import copyfileobj

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
UPLOADS_DIR = os.path.join(BASE_DIR, "data", "uploads")


class FileStore:
    def __init__(self) -> None:
        os.makedirs(UPLOADS_DIR, exist_ok=True)

    async def save_upload(self, file: UploadFile) -> str:
        assignment_id = str(uuid.uuid4())
        folder = os.path.join(UPLOADS_DIR, assignment_id)
        os.makedirs(folder, exist_ok=True)

        raw_path = os.path.join(folder, file.filename)

        with open(raw_path, "wb") as buffer:
            await file.seek(0)
            copyfileobj(file.file, buffer)

        print(f"📁 Saved file at: {raw_path}")
        return assignment_id

    def get_assignment_dir(self, assignment_id: str) -> str:
        return os.path.join(UPLOADS_DIR, assignment_id)
