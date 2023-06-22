from fastapi import FastAPI
import uvicorn
import LoginController
import UserController

app=FastAPI(
    title="User Management System !"
)

app.include_router(UserController.router)
app.include_router(LoginController.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

    