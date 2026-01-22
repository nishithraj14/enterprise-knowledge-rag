from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.bootstrap.preload import preload_resume

app = FastAPI(
    title="Enterprise Knowledge RAG System",
    version="1.0.0"
)

# CORS (UI may be hosted separately later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    preload_resume()

app.include_router(router)

# Serve UI locally
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
