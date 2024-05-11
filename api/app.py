from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agents.task_util_agents import execute_agent

app = FastAPI()

class TaskCorrectorBody(BaseModel):
    userid: str
    sessionid: str
    os: str
    task: str
    app_list: dict

@app.post("/task_corrector")
async def task_corrector(body: TaskCorrectorBody):
    provider = "anthropic"
    model = "claude_sonnet"
    system_prompt_params = {"os": body.os}
    fewshot_params = {"task": body.task, "app_list": body.app_list}
    response = execute_agent(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_corrector",
        system_prompt_params=system_prompt_params,
        fewshot_params=fewshot_params,
        provider=provider,
        model=model
    )
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

class TaskRefinerBody(BaseModel):
    userid: str
    sessionid: str
    os: str
    task: str

@app.post("/task_refiner")
async def task_refiner(body: TaskRefinerBody):
    provider = "anthropic"
    model = "claude_haiku"
    system_prompt_params = {"os": body.os}
    fewshot_params = {"task": body.task}
    response = execute_agent(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_refiner",
        system_prompt_params=system_prompt_params,
        fewshot_params=fewshot_params,
        provider=provider,
        model=model
    )
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

class TaskRefinerStage2Body(BaseModel):
    userid: str
    sessionid: str
    os: str
    task: str

@app.post("/task_refiner_stage_2")
async def task_refiner_stage_2(body: TaskRefinerStage2Body):
    provider = "anthropic"
    model = "claude_haiku"
    system_prompt_params = {"os": body.os}
    fewshot_params = {"task": body.task}
    response = execute_agent(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_refiner_stage_2",
        system_prompt_params=system_prompt_params,
        fewshot_params=fewshot_params,
        provider=provider,
        model=model
    )
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)
