import time

from fastapi import APIRouter, Header, Depends, WebSocket, Response
from starlette.responses import JSONResponse
from starlette.websockets import WebSocketClose

from globalData.data import connList
from checker.checker import limit_conn

car_router = APIRouter()

@car_router.websocket("/{id}")
@limit_conn(limit=1, rate='5s')
async def read_root(id: str, websocket: WebSocket):
    try:
        if not id:
            print('Request not allowed to continue')
            # await websocket.accept()
            # time.sleep(0.1)
            # await websocket.close(1000)
            return

        else:
            await websocket.accept()
            await websocket.send_text('Connecting to socket!')
            await websocket.send_json({'connectionList': connList.conn})

            # await websocket.close()
            while True:
                data = await websocket.receive_text()

    except Exception as err:
        print(f'ERROR: {str(err)}')
        await websocket.send_text('Disconnecting to socket!')
        time.sleep(2)
        await websocket.close()
