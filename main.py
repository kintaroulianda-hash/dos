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
        try:
            url = await websocket.receive_text()
            await websocket.send_text(f"Initiating attack on: {url}")
            
            # 攻撃をバックグラウンドタスクとして非同期に実行
            # ※攻撃実行関数（start_attack）がasyncである必要がある
            asyncio.create_task(run_attack_process(websocket, url))
            
        except Exception as e:
            print(f"WS Error: {e}")
            break

async def run_attack_process(websocket, url):
    # start_attackの結果を逐次的に送信する構造に書き換えていく
    results = await start_attack(url, count=50)
    for res in results:
        await websocket.send_text(res)

    
