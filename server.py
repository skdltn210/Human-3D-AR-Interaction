import cv2
from fastapi import FastAPI

app = FastAPI()

def show_webcam():
    # 웹캠 캡처 객체 생성
    cap = cv2.VideoCapture(0)

    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)

        # 프레임 표시
        cv2.imshow('Webcam', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 종료 시 캡처 객체 해제 및 창 닫기
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    import uvicorn
    show_webcam()
    uvicorn.run(app, host="127.0.0.1", port=8000)
