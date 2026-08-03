from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500", 
        "http://127.0.0.1:5500", 
        "http://localhost:8000",
        settings.FRONTEND_URL
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True, # Required for HttpOnly cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to SIH Matchmaker API"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

from api.v1 import admin, auth, invites, superadmin, teams, users

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["Teams"])
app.include_router(invites.router, prefix="/api/v1/invites", tags=["Invites"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(superadmin.router, prefix="/api/v1/superadmin", tags=["Super Admin"])
