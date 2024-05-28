import cv2
import asyncio
import base64
import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.websockets import WebSocketDisconnect
import tensorflow_hub as hub
import numpy as np
import tensorflow as tf
import functools
import os

# 스타일 전이 모델 로드
style_transfer_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
# 스타일 이미지 로드 함수
def load_style_image(index):
    style_images = [
        './images/style1.jpg',  # 인덱스 0에 해당하는 스타일 이미지
        './images/style2.jpg',  # 인덱스 1에 해당하는 스타일 이미지
        './images/style3.jpg',  # 인덱스 2에 해당하는 스타일 이미지
        './images/style4.jpg',  # 인덱스 3에 해당하는 스타일 이미지
        './images/style5.jpg',  # 인덱스 4에 해당하는 스타일 이미지
    ]
    if 0 <= index < len(style_images):
        img = cv2.imread(style_images[index])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
        return img
    return None



app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 웹캠 캡처 객체 생성
cap = cv2.VideoCapture(1)

# 웹캠 해상도 및 FPS 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 15)  

# 캡처 객체 초기화 확인
if not cap.isOpened():
    logger.error("웹캠을 열 수 없습니다.")
    exit()

async def send_video(websocket: WebSocket, style_index=-1):
    while True:
        ret, frame = cap.read()
        if not ret:
            logger.error("웹캠에서 프레임을 읽을 수 없습니다.")
            break

        # 스타일 이미지가 유효하면 스타일 전이 수행
        if style_index >= 0:
            style_image = load_style_image(style_index)
            if style_image is not None:
                # 웹캠 프레임을 적절한 형태로 전처리
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0

                # 스타일 전이 모델 호출
                try:
                    outputs = style_transfer_model(tf.constant(frame), tf.constant(style_image))
                    stylized_image = outputs[0]

                    # 스타일이 적용된 이미지를 원래 형식으로 변환
                    stylized_image = np.array(stylized_image * 255, np.uint8)
                    stylized_image = cv2.cvtColor(stylized_image[0], cv2.COLOR_RGB2BGR)
                    frame = stylized_image
                except Exception as e:
                    logger.error(f"스타일 전이 중 오류 발생: {e}")
                    # 오류가 발생했을 경우 원본 프레임을 계속 사용
            else:
                logger.warning(f"유효한 스타일 이미지가 없습니다. 인덱스: {style_index}")
        else:
            logger.info("스타일 인덱스가 유효하지 않습니다. 원본 이미지 사용")

        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        await websocket.send_text(frame_base64)
        await asyncio.sleep(0.03)




@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("WebSocket 연결이 성공적으로 수립되었습니다.")
    await websocket.accept()
    style_index = -1  # 기본 스타일 인덱스
    try:
        while True:
            try:
                index_str = await websocket.receive_text()
                if index_str.isdigit() or index_str == "-1":
                    style_index = int(index_str)
            except WebSocketDisconnect:
                logger.info("WebSocket 연결이 종료되었습니다.")
                break
            await send_video(websocket, style_index)
    except WebSocketDisconnect:
        logger.info("WebSocket 연결이 종료되었습니다.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
