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

# 로깅 기본 설정
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# 스트림 핸들러 생성 및 설정
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

# 로깅 테스트
logger.debug("디버그 로그 메시지")
logger.info("정보 로그 메시지")
logger.warning("경고 로그 메시지")
logger.error("오류 로그 메시지")
logger.critical("크리티컬 로그 메시지")

# 스타일 전이 모델 로드
style_transfer_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
# 스타일 이미지 로드 함수
# 스타일 이미지 로드


def load_style_image():
    style_image_path = './images/style1.jpg'
    img = cv2.imread(style_image_path)
    if img is not None:
        logger.info(f"스타일 이미지 로드 성공: {style_image_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
        logger.info(f"이미지 shape: {img.shape}")
        return img
    else:
        logger.error(f"스타일 이미지 로드 실패: {style_image_path}")
    return None

# 스타일 전이 적용 및 결과 저장 함수
def apply_and_save_style_transfer(frame, style_image, model, output_path="./output.jpg"):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0
    outputs = model(tf.constant(frame), tf.constant(style_image))
    stylized_image = outputs[0]
    stylized_image = np.array(stylized_image * 255, np.uint8)
    stylized_image = cv2.cvtColor(stylized_image[0], cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, stylized_image)

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


async def send_video(websocket: WebSocket):
    # 스타일 이미지 로드
    style_image = load_style_image()  # 이미 로드 함수가 구현되어 있음
    if style_image is None:
        logger.error("스타일 이미지를 로드할 수 없습니다.")
        return

    while True:
        # 웹캠에서 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            logger.error("웹캠에서 프레임을 읽을 수 없습니다.")
            break

        # 이미지 전처리: BGR에서 RGB로 변환, 배치 차원 추가, 정규화
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0

        # 스타일 전이 모델을 사용하여 스타일 적용
        try:
            outputs = style_transfer_model(tf.constant(frame), tf.constant(style_image))
            stylized_image = outputs[0]
            stylized_image = np.array(stylized_image * 255, np.uint8)
            stylized_image = cv2.cvtColor(stylized_image[0], cv2.COLOR_RGB2BGR)  # 결과를 다시 BGR로 변환
            frame = stylized_image
            logger.info("스타일 전이 성공")
        except Exception as e:
            logger.error(f"스타일 전이 중 오류 발생: {e}")
            continue  # 오류 발생 시 다음 프레임 처리로 넘어감

        # 인코딩 후 WebSocket을 통해 전송
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        await websocket.send_text(frame_base64)
        await asyncio.sleep(0.03)  # 프레임 속도 조절





@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    style_image = load_style_image()
    if style_image is None:
        await websocket.send_text("Error loading style image")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            await websocket.send_text("Error reading from webcam")
            break

        # 스타일 전이 적용 및 결과 이미지 저장
        apply_and_save_style_transfer(frame, style_image, style_transfer_model, "styled_frame.jpg")

        # 저장된 이미지를 WebSocket을 통해 전송 (옵션)
        with open("styled_frame.jpg", "rb") as img_file:
            img_bytes = img_file.read()
            img_b64 = base64.b64encode(img_bytes).decode('utf-8')
            await websocket.send_text(img_b64)

        await asyncio.sleep(1)  # 프레임 업데이트 간격 조절



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




