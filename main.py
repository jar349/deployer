import logging
import os
import validators

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import Optional

from deployer import Deployer
from deployer.formatters import SlackFormattedSubstring


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
            "- `.deploy PR_URL`: create a deployment on the PR at the given PR_URL\n" +
            "- `.deploy PR_URL to ENVIRONMENT`: (not impl) create a deployment with `ENVIRONMENT` in the payload\n")


@app.get("/ping", response_class=PlainTextResponse)
async def get_ping():
    return "pong"


@app.get("/metadata", response_class=JSONResponse)
async def get_metadata():
    return {"protocol_version": "1.0"}


@app.post("/handle", response_class=JSONResponse)
async def handle(request: Command):
    namespace = request.namespace
    command = request.command
    event = request.event
    print(f"Received namespace: {namespace}, command: {command}, event: {event}")

    if not command:
        return {"message": f":red_circle: No command provided.  Try `.{namespace} help`"}

    cmd_parts = command.split()
    # slack sends links surrounded by angle brackets (<, >) if it recognizes a URL, so we need to extract the URL
    substring = SlackFormattedSubstring(cmd_parts[0])
    handler_url = substring.get_content_or_none() if substring.is_url_link() else substring.get_raw()

    if not validators.url(handler_url):
        return {"message": (f":red_circle: `{handler_url}` does not seem to be a valid URL; see: " +
                            "https://validators.readthedocs.io/en/latest/index.html#module-validators.url")}

    deployer = Deployer(handler_url)

    if len(cmd_parts) > 1:
        if cmd_parts[1] == "to":
            if len(cmd_parts) == 3:
                deployer.set_environment(cmd_parts[2])
            else:
                return {"message": f":red_circle: I don't understand that command; try: `.{namespace} help`"}
        else:
            return {"message": f":red_circle: I don't understand that command; try: `.{namespace} help`"}
    elif len(cmd_parts) > 3:
        return {"message": f":red_circle: I don't understand that command; try: `.{namespace} help`"}

    return {"message": deployer.deploy()}
