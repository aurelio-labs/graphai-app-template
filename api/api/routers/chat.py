import asyncio

from fastapi import APIRouter, Body, Request
from graphai.callback import EventCallback
from starlette.responses import StreamingResponse

from api.schemas import Message

router = APIRouter()

async def gen(callback: EventCallback):
    async for token in callback.aiter():
        yield token

async def chat(request: Request, message: Message = Body(...)):
    # init new callback
    callback = EventCallback()
    graph = request.app.state.graph
    # add new user message to graph state events
    graph.update_state({
        "events": [
            *graph.state["events"],
            message.dict()
        ],
        "client": request.app.state.client
    })
    _ = asyncio.create_task(
        graph.execute(input={"input": {}}, callback=callback)
    )
    return StreamingResponse(
        gen(callback), media_type="text/event-stream"
    )

