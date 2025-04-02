from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Dravin: AI Dialogue Engine - FastAPI"}