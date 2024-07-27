############### Importing Builtin ###################
import gc
import uuid

############### Importing libraries ###################
import torch
import uvicorn
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile

############### Importing Our classes ###################
from src.llm_inference import TextInference
from src.database_connector import DatabaseAgent
from src.prompt_formatter import PromptFormatterV1
from src.db_models import DatabaseConnection, GetResult
from src.utils import SQLExtractor, get_data_from_query, extract_and_correct_sql
from src.session_logger import log_connection_details, fetch_connection_details

############### Importing Routers ###################
from routers.speech_router import router as speech_router

# defining the fastapi and routers.
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


# @app.get("/database/details/{session_id}")
# async def get_database_details(session_id: str):
#     try:
#         connection_details = fetch_connection_details(session_id)
#     except HTTPException as e:
#         raise e

#     return connection_details


@app.post("/database/execute_query/")
async def generate_and_execute(data: GetResult):
    # get the session id
    session_id = data.session_id

    # get the question
    question = data.question

    # get the max sequence parameter
    max_seq = data.max_seq_len

    try:
        connection_details = fetch_connection_details(session_id)
    except HTTPException as e:
        raise e

    # create the sql agent
    sql_agent = DatabaseAgent(**connection_details)

    # get the tables
    tables = sql_agent.grab_table_names()

    # get the tables and schema
    schemas = sql_agent.grab_table_schema(tables=tables)

    # format the prompt
    formatter = PromptFormatterV1(
        tables=schemas, db_type=connection_details["database_type"]
    )

    # TODO: write proper config file to load static infos.
    prompt = formatter(question=question)

    # define the inference llm
    inference_llm = TextInference()

    # pass the prompt through the llm
    output = inference_llm.generate_text(input_text=prompt, max_length=max_seq)

    # delete the inference object
    del inference_llm

    ############ If using cuda free the GPU memory for other model ###########
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        gc.collect()

    print(output)
    # extract the sql
    # extractor = SQLExtractor(text=output)
    # sql = extractor.extract_select_commands()[-1]
    try:
        sql = extract_and_correct_sql(text=output)
        # execute the sql
        result_df = get_data_from_query(
            query=sql,
            db_url=sql_agent.conn_str,  # get the connection string from sql agent.
        )
    except:

        sql = extract_and_correct_sql(text=output, correct=True)
        # execute the sql
        result_df = get_data_from_query(
            query=sql,
            db_url=sql_agent.conn_str,  # get the connection string from sql agent.
        )

    # convert the dataframe to a json
    result_df = result_df.to_dict(orient="records")

    # delete all the objects
    del sql_agent
    del formatter
    # del extractor

    return {"status_code": 200, "sql": sql, "dataframe": result_df}


if __name__ == "__main__":

    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=9999)
