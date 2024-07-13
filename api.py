import uuid

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile


from src.db_models import DatabaseConnection
from src.database_connector import DatabaseAgent
from src.session_logger import log_connection_details, fetch_connection_details

# importing router.
from routers.speech_router import router as speech_router

app = FastAPI()

app.include_router(speech_router, tags=["Speech Routers / Upload to Process"])


@app.post("/database/connect/")
async def connect_to_database(data: DatabaseConnection):

    # initialize the database connector
    try:
        db_connector = DatabaseAgent(
            **dict(data)
        )  # converting pydantic-> dict -> kwargs

        # if connection successful, generate unique id for session
        session_id = str(uuid.uuid4())

        # log the connection details
        log_connection_details(session_id, dict(data))

        return {"status_code": 200, "session_id": session_id}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Cannot connect to the database : {e}"
        )


@app.get("/database/details/{session_id}")
async def get_database_details(session_id: str):
    try:
        connection_details = fetch_connection_details(session_id)
    except HTTPException as e:
        raise e

    return connection_details


if __name__ == "__main__":

    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=9999)
