from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.background import BackgroundTask
import asyncio

app = FastAPI()


@app.get("/liveness")
async def root():
    print('liveness')
    return {"message": "Liveness"}

@app.get("/readiness")
async def root():
    print('readiness')
    return {"message": "Readiness"}

@app.get("/startup")
async def root():
    print('startup')
    return {"message": "Startup"}

@app.get("/hello")
async def root():
    print('hello')
    return {"message": "Hello World!"}

@app.on_event('shutdown')
def shutdown_event():
    print('Shutting down...!')

async def exit_app():
    loop = asyncio.get_running_loop()
    loop.stop()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    task = BackgroundTask(exit_app)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code, background=task)

@app.get("/break")
async def root():
    raise HTTPException(status_code=500, detail='Something went wrong')
    print('break')
    return {"message": "Break"}