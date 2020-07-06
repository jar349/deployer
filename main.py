import logging

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional


log = logging.getLogger(__name__)
app = FastAPI()


class Command(BaseModel):
    namespace: str
    command: str
    event: Optional[dict] = None


@app.get("/", response_class=HTMLResponse)
async def homepage():
    return "<html><body><h2>There's nothing here</h2><p>You might try <a href='/help'>/help</a></body></html>"


@app.get("/help", response_class=PlainTextResponse)
async def basic_help():
    return ("The deploy chatop can create deployments on your github repos and PRs:\n\n" +
            "  `.deploy PR_URL` will create a deployment on the PR at the given PR_URL\n")


@app.get("/ping", response_class=PlainTextResponse)
async def get_ping():
    return "pong"


@app.post("/handle", response_class=JSONResponse)
async def handle(request: Command):
    namespace = request.namespace
    command = request.command
    event = request.event
    log.debug(f"Received namespace: {namespace}, command: {command}, event: {event}")

