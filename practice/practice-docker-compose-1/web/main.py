from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
def read_root():
    port = os.getenv("PORT", "8000")
    mode = os.getenv("APP_MODE", "development")
    return {
        "service": "web",
        "message": "Hello from web service",
        "port": port,
        "mode": mode,
    }
