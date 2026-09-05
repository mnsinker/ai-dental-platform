from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.wecom import router as wecom_router
from api.routes.followups import router as followups_router

# 1. fastapi app
app = FastAPI()


# 2. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 3. route
# app.include_router(wecom_router)
app.include_router(followups_router)





@app.get("/health")
def health():
    return {"status": "ok"}

