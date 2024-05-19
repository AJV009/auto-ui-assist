from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agents.task_util_agents import execute_agent

app = FastAPI()

class BaseRequestBody(BaseModel):
    userid: str
    sessionid: str
    os: str
    task: str

def execute_and_return(userid, sessionid, agent_name, system_prompt_params, fewshot_params, provider, model):
    response = execute_agent(
        userid=userid,
        sessionid=sessionid,
        agent_name=agent_name,
        system_prompt_params=system_prompt_params,
        fewshot_params=fewshot_params,
        provider=provider,
        model=model
    )
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

class TaskCorrectorBody(BaseRequestBody):
    app_list: dict

@app.post("/task_corrector")
async def task_corrector(body: TaskCorrectorBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_corrector",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "app_list": body.app_list},
        provider="anthropic",
        model="claude_haiku"
    )

@app.post("/task_refiner_stage_1")
async def task_refiner(body: BaseRequestBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_refiner_stage_1",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task},
        provider="anthropic",
        model="claude_haiku"
    )

class TaskRefinerStage2Body(BaseRequestBody):
    refinement_data: str

@app.post("/task_refiner_stage_2")
async def task_refiner_stage_2(body: TaskRefinerStage2Body):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_refiner_stage_2",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "refinement_data": body.refinement_data},
        provider="anthropic",
        model="claude_haiku"
    )

@app.post("/step_creation_stage_1")
async def step_creation_stage_1(body: BaseRequestBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="step_creation_stage_1",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task},
        provider="anthropic",
        model="claude_haiku"
    )

class TaskStepSummarizationBody(BaseRequestBody):
    step_list: list

@app.post("/task_step_summarization")
async def step_creation_stage_1(body: TaskStepSummarizationBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_step_summarization",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "step_list": body.step_list},
        provider="anthropic",
        model="claude_haiku"
    )
