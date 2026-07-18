from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
from attack import start_attack

app = FastAPI()

@app.get("/")
async def get():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        url = await websocket.receive_text()
        await websocket.send_text(f"Initiating attack on: {url}")
        
        
        results = await start_attack(url, count=50)
        for res in results:
            await websocket.send_text(res)
