from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import PHOTOS_DIR
from app.routers import chat, dashboard, properties, schema, issues

app = FastAPI(title="Property Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=PHOTOS_DIR), name="static")

app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(properties.router)
app.include_router(schema.router)
app.include_router(issues.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
