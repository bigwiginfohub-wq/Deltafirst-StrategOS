from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import uvicorn

app = FastAPI()

# Allow all CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mode 3 passphrase hash (DeltaMode3)
CORRECT_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

class VerifyRequest(BaseModel):
    passphrase: str

@app.get("/")
def root():
    return {"message": "Mode 3 Verification API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/verify")
def verify(request: VerifyRequest):
    try:
        input_hash = hashlib.sha256(request.passphrase.encode()).hexdigest()
        if input_hash == CORRECT_HASH:
            return {"status": "VERIFIED", "message": "Access granted"}
        else:
            return {"status": "DENIED", "message": "Wrong passphrase"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
