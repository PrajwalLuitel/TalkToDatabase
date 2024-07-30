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
    audio_file: UploadFile = File(...), session_id: str = None
):
    try:
        if not fetch_connection_details(session_id):
            raise HTTPException(status_code=404, detail="Session ID not found")

        Path(save_pth).mkdir(parents=True, exist_ok=True)

        if audio_file.filename.endswith(".mp3") or audio_file.filename.endswith(".wav"):
            file_location = f"{save_pth}/{session_id}_{audio_file.filename}"
            with open(file_location, "wb") as f:
                f.write(await audio_file.read())
            return {"success": True, "message": "File uploaded successfully"}
        else:
            raise HTTPException(status_code=400, detail=f"{audio_file.filename} is not an audio file.")
    except Exception as e:
        import traceback
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        print(f"Exception occurred: {e}\nTraceback: {traceback_str}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")


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
