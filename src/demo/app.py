import uvicorn
from fastapi import FastAPI

from .routes.auth import router as auth_router
from .routes.users import router as users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)


if __name__ == "__main__":
    # local development
    uvicorn.run(app, host="127.0.0.1", port=8000)
else:
    # production use, for running using command
    # $ uvicorn main:app
    pass
