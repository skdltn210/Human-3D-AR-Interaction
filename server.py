from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

app = FastAPI()

# CORS 설정
origins = [
    "http://localhost:8000",  # 클라이언트 URL
    "http://localhost:3000",  # 클라이언트 URL
    "null"
    # 추가적인 허용 URL 입력
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3D 모델 파일 경로
MODEL_FILE_PATH = "public/japanese_mask1.glb"

# 이미지 파일 경로
IMAGE_FILE_PATH = "public/japanese_mask.png"

# 3D 모델 GET 요청 처리
@app.get("/get_3d_model")
async def get_3d_model():
    try:
        # 3D 모델 파일 경로 반환
        return {"model_path": MODEL_FILE_PATH}
    
    except FileNotFoundError:
        # 파일을 찾을 수 없는 경우 에러 메시지 반환
        return {"error": "3D 모델 파일을 찾을 수 없습니다."}
    
    except Exception as e:
        # 기타 예외 처리
        return {"error": str(e)}

# 이미지 파일 GET 요청 처리
@app.get("/get_image")
async def get_image():
    try:
        # 이미지 파일 읽기
        return FileResponse(IMAGE_FILE_PATH)
    
    except FileNotFoundError:
        # 파일을 찾을 수 없는 경우 에러 메시지 반환
        return {"error": "이미지 파일을 찾을 수 없습니다."}
    
    except Exception as e:
        # 기타 예외 처리
        return {"error": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
