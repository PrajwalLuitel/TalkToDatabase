import gc
from pathlib import Path
from typing import List


import torch
from fastapi import APIRouter, UploadFile, File, HTTPException

from src.utils import search_files
from src.db_models import ConvertAudio
from src.speech2text import SpeechToText
from src.session_logger import fetch_connection_details

# get root dir path
root_dir = str(Path(__file__).parent.parent)
# audio save pth
save_pth = str(Path(root_dir).joinpath("uploads"))

router = APIRouter()


@router.post("/audio/upload/")
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


@router.post("/audio/convert/")
async def convert_audio(data: ConvertAudio):

    # get the session id
    session_id = data.session_id

    # find the audio file in the saved folders
    file_path = search_files(directory=save_pth, search_string=session_id)

    if not file_path:
        raise HTTPException(status_code=404, detail="Audio file is not found.")

    # initialize the object
    speech_converter = SpeechToText(whisper_model_size="small")

    # grab the text
    text = speech_converter(file_path)

    ############ If using cuda free the GPU memory for other model ###########
    del speech_converter
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

    return {"timestamp": text, "text": "".join([v for k, v in text.items()])}
