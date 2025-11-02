"""Endpoints exposing the smart real estate assistant."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ...services import query_smart_agent


router = APIRouter(prefix="/ai")


class AgentQuery(BaseModel):
    prompt: str = Field(..., description="User natural language property query")


@router.post("/query")
async def query_agent(body: AgentQuery) -> dict[str, str]:
    """Forward the prompt to the AI agent and return the response."""

    if not body.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    result = await query_smart_agent(body.prompt)
    return {"response": result["response"], "model": result["model"]}
