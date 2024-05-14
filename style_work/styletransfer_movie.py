import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 스타일 전이 모델 로드
style_transfer_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')


# 스타일 이미지 로드 함수
def load_style_image(image_path='./images/japan.jpg'):
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
    # intensity = 0.65
    # stylized_image = (stylized_image * intensity + frame * (1 - intensity))
    #

    stylized_image = np.array(stylized_image * 255, np.uint8)
    stylized_image = cv2.cvtColor(stylized_image[0], cv2.COLOR_RGB2BGR)
    return stylized_image


# 웹캠 캡처 객체 생성 및 설정
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    logger.error("웹캠을 열 수 없습니다.")
else:
    style_image = load_style_image()
    if style_image is None:
        logger.error("스타일 이미지 로드에 실패했습니다.")
    else:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("웹캠에서 프레임을 읽을 수 없습니다.")
                break

            # 스타일 전이 적용
            stylized_frame = apply_style_transfer(frame, style_image, style_transfer_model)

            # 결과 이미지 표시
            cv2.imshow('Stylized Frame', stylized_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# 자원 정리
cap.release()
cv2.destroyAllWindows()
