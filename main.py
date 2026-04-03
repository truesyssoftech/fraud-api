# app/main.py

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()
app.include_router(router)

# 👇 ADD THIS BLOCK
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)