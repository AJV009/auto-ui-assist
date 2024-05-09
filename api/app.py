from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents.query_corrector import query_corrector_agent
import json
import asyncio

app = FastAPI()

class PlanStage1Body(BaseModel):
    uuid: str
    query: str
    os_apps: dict
    os: str

@app.post("/plan_stage_1")
async def plan_stage_1(body: PlanStage1Body):
    async def event_generator():
        yield json.dumps({'success': 'Analyzing Query. Please wait!', 'action': "processing"}).encode() + b'\n'

        # Query Corrector Agent
        yield json.dumps({'success': 'Analyzing: Running Query Corrector Agent', 'action': "processing"}).encode() + b'\n'
        response = query_corrector_agent(body.uuid, body.query, body.os_apps, body.os)
        yield json.dumps({'success': response, 'action': "processing"}).encode() + b'\n'

    return StreamingResponse(event_generator())
