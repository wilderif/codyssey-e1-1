from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"service": "helper", "message": "Hello from helper service"}
