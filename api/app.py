# Auto UI Assist API Endpoints
# This file defines the FastAPI endpoints for the Auto UI Assist application.

import json
import base64

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agents.task_util_agents import execute_agent

# Initialize FastAPI application
app = FastAPI()

# 1. Base Request Model
class BaseRequestBody(BaseModel):
    """
    Base model for all API request bodies.
    """
    userid: str
    sessionid: str
    os: str
    task: str

# 2. Utility Function
def execute_and_return(userid, sessionid, agent_name, system_prompt_params, fewshot_params, provider, model, image_base64=None):
    """
    Execute an agent and return the response as a JSONResponse.

    Args:
        userid (str): User ID
        sessionid (str): Session ID
        agent_name (str): Name of the agent to execute
        system_prompt_params (dict): Parameters for the system prompt
        fewshot_params (dict): Parameters for few-shot learning
        provider (str): AI provider (e.g., "openai", "anthropic")
        model (str): AI model to use
        image_base64 (str, optional): Base64 encoded image data

    Returns:
        JSONResponse: The response from the agent execution
    """
    response = execute_agent(
        userid=userid,
        sessionid=sessionid,
        agent_name=agent_name,
        system_prompt_params=system_prompt_params,
        fewshot_params=fewshot_params,
        provider=provider,
        model=model,
        image_base64=image_base64
    )
    json_compatible_item_data = jsonable_encoder(response)
    return JSONResponse(content=json_compatible_item_data)

# 3. Task Corrector Endpoint
class TaskCorrectorBody(BaseRequestBody):
    """
    Request body model for the task corrector endpoint.
    """
    app_list: dict
    image_base64: str

@app.post("/task_corrector")
async def task_corrector(body: TaskCorrectorBody):
    """
    Endpoint to correct and refine the initial task.

    Args:
        body (TaskCorrectorBody): The request body containing task details

    Returns:
        JSONResponse: Corrected task information
    """
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_corrector",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "app_list": body.app_list},
        provider="openai",
        model="gpt-4o-mini",
        image_base64=body.image_base64
    )

# 4. Task Refiner Stage 1 Endpoint
class TaskRefinerBody(BaseRequestBody):
    """
    Request body model for the task refiner stage 1 endpoint.
    """
    image_base64: str

@app.post("/task_refiner_stage_1")
async def task_refiner(body: TaskRefinerBody):
    """
    Endpoint for the first stage of task refinement.

    Args:
        body (TaskRefinerBody): The request body containing task details

    Returns:
        JSONResponse: Refined task information or clarification questions
    """
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_refiner_stage_1",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task},
        provider="anthropic",
        model="claude_sonnet",
        image_base64=body.image_base64
    )

# 5. Task Refiner Stage 2 Endpoint
class TaskRefinerStage2Body(BaseRequestBody):
    """
    Request body model for the task refiner stage 2 endpoint.
    """
    refinement_data: str

@app.post("/task_refiner_stage_2")
async def task_refiner_stage_2(body: TaskRefinerStage2Body):
    """
    Endpoint for the second stage of task refinement.

    Args:
        body (TaskRefinerStage2Body): The request body containing task details and refinement data

    Returns:
        JSONResponse: Final refined task
    """
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_refiner_stage_2",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "refinement_data": body.refinement_data},
        provider="openai",
        model="gpt-4o-mini"
    )

# 6. High Level Action Plan Creation Endpoint
class HighLevelActionPlanCreationBody(BaseRequestBody):
    """
    Request body model for the high level action plan creation endpoint.
    """
    app: str
    image_base64: str

@app.post("/high_level_action_plan_creation")
async def high_level_action_plan_creation(body: HighLevelActionPlanCreationBody):
    """
    Endpoint to create a high-level action plan for the task.

    Args:
        body (HighLevelActionPlanCreationBody): The request body containing task and app details

    Returns:
        JSONResponse: High-level action plan
    """
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

# 7. Action Plan Verifier Endpoint
class ActionPlanVerifierBody(BaseRequestBody):
    """
    Request body model for the action plan verifier endpoint.
    """
    step_list: str
    image_base64: str

@app.post("/action_plan_verifier")
async def action_plan_verifier(body: ActionPlanVerifierBody):
    """
    Endpoint to verify the created action plan.

    Args:
        body (ActionPlanVerifierBody): The request body containing the action plan steps

    Returns:
        JSONResponse: Verification result of the action plan
    """
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="action_plan_verifier",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "step_list": body.step_list},
        provider="openai",
        model="gpt-4o-mini",
        image_base64=body.image_base64
    )

# 8. Action Plan Refiner Endpoint
class ActionPlanRefinerBody(BaseRequestBody):
    """
    Request body model for the action plan refiner endpoint.
    """
    action_plan: str
    image_base64: str

@app.post("/action_plan_refiner")
async def action_plan_refiner(body: ActionPlanRefinerBody):
    """
    Endpoint to refine the action plan based on feedback or verification results.

    Args:
        body (ActionPlanRefinerBody): The request body containing the action plan and feedback

    Returns:
        JSONResponse: Refined action plan
    """
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

# 9. Task Step Summarization Endpoint
class TaskStepSummarizationBody(BaseRequestBody):
    """
    Request body model for the task step summarization endpoint.
    """
    step_list: str

@app.post("/task_step_summarization")
async def task_step_summarization(body: TaskStepSummarizationBody):
    """
    Endpoint to summarize the steps of a task.

    Args:
        body (TaskStepSummarizationBody): The request body containing the list of task steps

    Returns:
        JSONResponse: Summarized task steps
    """
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name="task_step_summarization",
        system_prompt_params={"os": body.os},
        fewshot_params={"task": body.task, "step_list": body.step_list},
        provider="openai",
        model="gpt-4o-mini"
    )

# 10. Low Level Action Plan Creation Endpoint
class LowLevelActionPlanCreationBody(BaseRequestBody):
    """
    Request body model for the low level action plan creation endpoint.
    """
    app: str
    tooling: str
    image_base64: str
    step: str
    previous_execution_data: str

@app.post("/low_level_action_plan_creation")
async def low_level_action_plan_creation(body: LowLevelActionPlanCreationBody):
    """
    Endpoint to create a low-level action plan for a specific step.

    Args:
        body (LowLevelActionPlanCreationBody): The request body containing step details and tooling information

    Returns:
        JSONResponse: Low-level action plan for the specific step
    """
    return execute_and_return(
        userid=body.userid,
        sessionid=body.sessionid,
        agent_name=f"low_level_action_plan_creation_{body.app}",
        system_prompt_params={"os": body.os, "tooling": body.tooling},
        fewshot_params={"task": body.step, "previous_execution_data": body.previous_execution_data},
        provider="anthropic",
        model="claude_sonnet",
        image_base64=body.image_base64
    )

# API Structure Overview:
# 1. BaseRequestBody: Defines common fields for all requests
# 2. execute_and_return: Utility function to execute agents and format responses
# 3. Task Corrector: Refines the initial task
# 4. Task Refiner Stage 1: Generates clarification questions if needed
# 5. Task Refiner Stage 2: Finalizes the refined task based on clarifications
# 6. High Level Action Plan Creation: Generates a high-level plan for the task
# 7. Action Plan Verifier: Checks the validity of the action plan
# 8. Action Plan Refiner: Modifies the action plan based on feedback
# 9. Task Step Summarization: Provides a summary of the task steps
# 10. Low Level Action Plan Creation: Generates detailed steps for each high-level action

# This API structure allows for a step-by-step refinement and execution of user tasks,
# utilizing different AI models (OpenAI and Anthropic) for various stages of the process.
