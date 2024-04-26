import cv2
import mediapipe as mp

# Mediapipe의 Face Mesh 모듈을 초기화합니다.
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

# 웹캠을 켭니다.
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("웹캠에서 프레임을 읽을 수 없습니다.")
        break

    # 프레임을 RGB로 변환합니다.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Mediapipe에 프레임을 전달하여 얼굴에 mesh를 적용합니다.
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 얼굴 landmark를 연결하여 mesh를 그립니다.
            mp.solutions.drawing_utils.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, landmark_drawing_spec=drawing_spec)

    # 결과를 화면에 표시합니다.
    cv2.imshow('Face Mesh', frame)

    # 'esc' 키를 누르면 종료합니다.
    if cv2.waitKey(1) == 27:  # 27은 'esc' 키의 ASCII 코드입니다.
        break

# 자원을 정리하고 창을 닫습니다.
cap.release()
cv2.destroyAllWindows()
