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
        await websocket.send_text(f"攻撃開始: {url}")
        # 攻撃実行
        results = await start_attack(url, count=100)
        # 結果をログに返す
        for res in results:
            await websocket.send_text(res)
