import cv2
import numpy as np
import tensorflow as tf
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# TensorFlow Lite 모델 경로
style_predict_path = tf.keras.utils.get_file(
    'style_predict.tflite',
    'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/prediction/1?lite-format=tflite'
)
style_transform_path = tf.keras.utils.get_file(
    'style_transform.tflite',
    'https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/int8/transfer/1?lite-format=tflite'
)

# TensorFlow Lite 인터프리터 로드
style_predict_interpreter = tf.lite.Interpreter(model_path=style_predict_path)
style_transform_interpreter = tf.lite.Interpreter(model_path=style_transform_path)
style_predict_interpreter.allocate_tensors()
style_transform_interpreter.allocate_tensors()

# 스타일 이미지 로드 및 전처리
def load_and_preprocess_style_image(image_path='./images/japanese.jpg'):
    img = cv2.imread(image_path)
    if img is None:
        logger.error(f"스타일 이미지 로드 실패: {image_path}")
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.expand_dims(img, axis=0).astype(np.float32) / 255.0
    img = tf.image.resize(img, (256, 256))  # 스타일 이미지 크기 조정
    return img

# 스타일 전이 적용 함수
def run_style_transform(style_image, frame):
    # 프레임 전처리
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.expand_dims(frame, axis=0).astype(np.float32) / 255.0
    frame = tf.image.resize(frame, (384, 384))  # 콘텐츠 이미지 크기 조정

    # 스타일 추출 실행
    style_predict_interpreter.set_tensor(style_predict_interpreter.get_input_details()[0]['index'], style_image)
    style_predict_interpreter.invoke()
    style_bottleneck = style_predict_interpreter.get_tensor(style_predict_interpreter.get_output_details()[0]['index'])

    # 스타일 변환 실행
    style_transform_interpreter.set_tensor(style_transform_interpreter.get_input_details()[0]['index'], frame)
    style_transform_interpreter.set_tensor(style_transform_interpreter.get_input_details()[1]['index'], style_bottleneck)
    style_transform_interpreter.invoke()
    stylized_image = style_transform_interpreter.get_tensor(style_transform_interpreter.get_output_details()[0]['index'])

    stylized_image = np.squeeze(stylized_image)  # 배치 차원 제거
    stylized_image = np.clip(stylized_image * 255, 0, 255).astype(np.uint8)
    stylized_image = cv2.cvtColor(stylized_image, cv2.COLOR_RGB2BGR)
    return stylized_image

# 웹캠 캡처 설정
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    logger.error("웹캠을 열 수 없습니다.")
else:
    style_image = load_and_preprocess_style_image()
    if style_image is None:
        logger.error("스타일 이미지 로드에 실패했습니다.")
    else:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("웹캠에서 프레임을 읽을 수 없습니다.")
                break

            # 스타일 전이 적용
            stylized_frame = run_style_transform(style_image, frame)

            # 결과 이미지 표시
            cv2.imshow('Stylized Frame', stylized_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# 자원 정리
cap.release()
cv2.destroyAllWindows()
