from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI()

# Simple in-memory verification
CORRECT_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"

class VerifyRequest(BaseModel):
    passphrase: str

@app.get("/")
def root():
    return {"status": "alive", "message": "Mode 3 API is running"}

@app.post("/verify")
def verify(request: VerifyRequest):
    input_hash = hashlib.sha256(request.passphrase.encode()).hexdigest()
    print(f"Received passphrase: {request.passphrase}")
    print(f"Computed hash: {input_hash}")
    print(f"Expected hash: {CORRECT_HASH}")
    
    if input_hash == CORRECT_HASH:
        return {"status": "VERIFIED", "message": "Access granted"}
    else:
        return {"status": "DENIED", "message": "Wrong passphrase"}