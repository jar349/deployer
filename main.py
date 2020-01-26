from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse

app = Starlette()


@app.route("/")
async def homepage(request):
    return HTMLResponse(
        "<html><body><h2>There's nothing here</h2><p>You might try <a href='/help'>/help</a></body></html>"
    )


@app.route("/help")
async def basic_help(request):
    return PlainTextResponse(
        "The deploy chatop can create deployments on your github repos and PRs:\n\n" +
        "  `.deploy PR_URL will create a deployment on the PR at the given PR_URL`\n"
    )
