from fastapi import APIRouter
from app.agent.llm_agent import route_query

router = APIRouter()

@router.get("/ask")
def ask(query: str):
    return route_query(query)