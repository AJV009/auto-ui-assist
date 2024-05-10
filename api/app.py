from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agents.task_corrector import task_corrector_agent

app = FastAPI()

class PlanStage1Body(BaseModel):
    userid: str
    sessionid: str
    task: str
    app_list: dict
    os: str
    refinement: str

@app.post("/plan_stage_1")
async def plan_stage_1(body: PlanStage1Body):
    response = task_corrector_agent(
        userid=body.userid,
        sessionid=body.sessionid,
        task=body.task,
        app_list=body.app_list,
        os=body.os,
        refinement=body.refinement
    )
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)
