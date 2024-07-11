from fastapi import APIRouter

router = APIRouter(tags=["speech router"])


@router.post("/upload/audio/")
def upload_audio_file():
    return ""
