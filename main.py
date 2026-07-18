from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import subprocess

app = FastAPI()

async def send_request(url):
   
    cmd = f"proxychains4 -q curl -I -L --max-time 2 {url}"
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return f"Status: {process.returncode} | Output: {stdout.decode()[:50]}..."

@app.get("/")
async def get():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text() 
        
        for _ in range(10): 
            result = await send_request(data)
            await websocket.send_text(result)
            await asyncio.sleep(0.5)
