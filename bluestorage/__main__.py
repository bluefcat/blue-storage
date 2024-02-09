import asyncio
from uvicorn import Config, Server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bluestorage.api.auth import auth_router
from bluestorage.api.api import api_router

from bluestorage.setting import setting

app: FastAPI = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(api_router)

async def main():
    config: Config = Config(**setting["server"])
    server: Server = Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
