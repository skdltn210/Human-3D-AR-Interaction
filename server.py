import cv2
import asyncio
import base64
import logging  # 로깅 모듈 추가
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 웹캠 캡처 객체 생성
cap = cv2.VideoCapture(1)  # 0은 기본 웹캠을 의미합니다. 여러 개의 카메라가 연결되어 있다면 0 대신 다른 숫자를 사용할 수 있습니다.

# 웹캠 해상도 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# 캡처 객체 초기화 확인
if not cap.isOpened():
    logger.error("웹캠을 열 수 없습니다.")
    exit()

async def send_video(websocket: WebSocket):
    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 프레임 읽기가 실패한 경우 루프 탈출
        if not ret:
            logger.error("웹캠에서 프레임을 읽을 수 없습니다.")
            break

        # 좌우로 뒤집기
        flipped_frame = cv2.flip(frame, 1)

        # JPEG 형식으로 인코딩
        _, buffer = cv2.imencode('.jpg', flipped_frame)

        # base64로 인코딩
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        # 클라이언트로 프레임 전송
        await websocket.send_text(frame_base64)

        # 30ms 대기 후 다음 프레임 읽기
        await asyncio.sleep(0.03)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("WebSocket 연결이 성공적으로 수립되었습니다.")
    await websocket.accept()
    await send_video(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
