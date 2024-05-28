import cv2
import asyncio
import base64
import logging
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.websockets import WebSocketDisconnect 

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 스타일 전이 모델 로드
style_transfer_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

# 스타일 이미지 로드 함수
def load_style_image(image_path):
    img = cv2.imread(image_path)
    if img is not None:
        logger.info(f"스타일 이미지 로드 성공: {image_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
        return img
    else:
        logger.error(f"스타일 이미지 로드 실패: {image_path}")
        return None
    
# 스타일 전이 적용 함수
def apply_style_transfer(frame, style_image, model):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0
    outputs = model(tf.constant(frame), tf.constant(style_image))
    stylized_image = outputs[0]

    # 스타일 강도 조절
    intensity = 0.65
    stylized_image = (stylized_image * intensity + frame * (1 - intensity))

    stylized_image = np.array(stylized_image * 255, np.uint8)
    stylized_image = cv2.cvtColor(stylized_image[0], cv2.COLOR_RGB2BGR)
    return stylized_image

# 웹캠 캡처 객체 생성
cap = cv2.VideoCapture(1)

# 웹캠 해상도 및 FPS 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1440) 
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 15)  

# 초기 스타일 이미지 로드
style_images = {
    -1: None,
    0: load_style_image('styles/img.jpg'),
}

global current_style_index
current_style_index = -1

async def send_video(websocket: WebSocket):
    global current_style_index
    # 캡처 객체 초기화 확인
    if not cap.isOpened():
        logger.error("웹캠을 열 수 없습니다.")
        exit()

    while True:
        # 클라이언트로부터 메시지 수신
        index_str = await websocket.receive_text()
        index = int(index_str)
        logger.info(f"받은 인덱스: {index}")

        # 스타일 전이 적용 여부 확인
        if index != current_style_index:
            current_style_index = index
            if current_style_index == -1:
                logger.info("스타일 전이를 적용하지 않습니다.")
                style_image = None
            else:
                style_image = style_images.get(current_style_index)
                if style_image is None:
                    logger.error(f"인덱스 {current_style_index}에 해당하는 스타일 이미지가 없습니다.")
                    continue

        # 프레임 읽기
        ret, frame = cap.read()

        # 프레임 읽기가 실패한 경우 루프 탈출
        if not ret:
            logger.error("웹캠에서 프레임을 읽을 수 없습니다.")
            break
        
        # 스타일 전이 적용
        if style_image is not None:
            stylized_frame = apply_style_transfer(frame, style_image, style_transfer_model)
        else:
            stylized_frame = frame

        # 좌우로 뒤집기
        flipped_frame = cv2.flip(stylized_frame, 1)

        # JPEG 형식으로 인코딩
        _, buffer = cv2.imencode('.jpg', flipped_frame)

        # base64로 인코딩
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        try:
            # 클라이언트로 프레임 전송
            await websocket.send_text(frame_base64)
        except WebSocketDisconnect:
            logger.info("WebSocket 연결이 종료되었습니다.")
            break

        # 30ms 대기 후 다음 프레임 읽기
        await asyncio.sleep(0.03)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("WebSocket 연결이 성공적으로 수립되었습니다.")
    await websocket.accept()
    try:
        # send_video 코루틴 실행
        await send_video(websocket)
    except WebSocketDisconnect:
        logger.info("WebSocket 연결이 종료되었습니다.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
