import json
import base64

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

def execute_and_return(userid, sessionid, agent_name, system_prompt_params, fewshot_params, provider, model, image_base64=None):
    response = execute_agent(
        userid=userid,
        sessionid=sessionid,
        agent_name=agent_name,
        system_prompt_params=system_prompt_params,
        fewshot_params=fewshot_params,
        provider=provider,
        model=model,
        image_base64=None
    )
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

class TaskCorrectorBody(BaseRequestBody):
    app_list: dict
    image_base64: str

@app.post("/task_corrector")
async def task_corrector(body: TaskCorrectorBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_corrector",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "app_list": body.app_list},
        provider="anthropic",
        model="claude_haiku",
        image_base64=body.image_base64
    )

class TaskRefinerBody(BaseRequestBody):
    image_base64: str

@app.post("/task_refiner_stage_1")
async def task_refiner(body: TaskRefinerBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_refiner_stage_1",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task},
        provider="anthropic",
        model="claude_opus",
        image_base64=body.image_base64
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
        model="claude_opus"
    )

class HighLevelActionPlanCreationBody(BaseRequestBody):
    app: str
    image_base64: str

@app.post("/high_level_action_plan_creation")
async def high_level_action_plan_creation(body: HighLevelActionPlanCreationBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name=f"high_level_action_plan_creation_{body.app}",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task},
        provider="openai",
        model="gpt-4o",
        image_base64=body.image_base64
    )

class ActionPlanVerifierBody(BaseRequestBody):
    step_list: str
    image_base64: str

@app.post("/action_plan_verifier")
async def action_plan_verifier(body: ActionPlanVerifierBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="action_plan_verifier",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "step_list": body.step_list},
        provider="anthropic",
        model="claude_sonnet",
        image_base64=body.image_base64
    )

class ActionPlanRefinerBody(BaseRequestBody):
    action_plan: str
    image_base64: str

@app.post("/action_plan_refiner")
async def action_plan_refiner(body: ActionPlanRefinerBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="action_plan_refiner",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "action_plan": body.action_plan},
        provider="anthropic",
        model="claude_sonnet",
        image_base64=body.image_base64
    )

class TaskStepSummarizationBody(BaseRequestBody):
    step_list: str

@app.post("/task_step_summarization")
async def task_step_summarization(body: TaskStepSummarizationBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_step_summarization",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "step_list": body.step_list},
        provider="anthropic",
        model="claude_haiku"
    )

class LowLevelActionPlanCreationBody(BaseRequestBody):
    app: str
    tooling: str
    image_base64: str
    step: str

@app.post("/low_level_action_plan_creation")
async def low_level_action_plan_creation(body: LowLevelActionPlanCreationBody):
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name=f"low_level_action_plan_creation_{body.app}",
        system_prompt_params={"os": body.os, "tooling": body.tooling},
        fewshot_params={"task": body.step},
        provider="openai",
        model="gpt-4o",
        image_base64=body.image_base64
    )
