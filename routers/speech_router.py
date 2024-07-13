from pathlib import Path
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException

from src.session_logger import fetch_connection_details

# get root dir path
root_dir = str(Path(__file__).parent.parent)
# audio save pth
save_pth = str(Path(root_dir).joinpath("uploads"))

router = APIRouter()


@router.post("/upload/audio/")
async def upload_audio_file(
    audio_file: List[UploadFile] = File(...), session_id: str = None
):
    try:
        if not fetch_connection_details(session_id):
            raise HTTPException(status_code=404, detail="Session ID not found")

        for file in audio_file:
            # if audio file check save location exists or not, if save else create
            Path(save_pth).mkdir(parents=True, exist_ok=True)

            # check for file type : only mp3 and wav, if save else raise exception.
            if (file.filename.endswith(".mp3")) or (file.filename.endswith(".wav")):

                file_location = f"{save_pth}/{session_id}_{file.filename}"
                with open(file_location, "wb") as f:
                    f.write(await file.read())

            else:
                raise HTTPException(
                    status_code=400, detail=f"{file.filename} is not a audio file."
                )

        return {"success": True, "message": "Files uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {e}")
