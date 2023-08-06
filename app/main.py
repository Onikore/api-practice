import asyncio

import uvicorn

from app.fastapi_main import fastapi_app
from app.rocketry_worker import rocketry_app


class Server(uvicorn.Server):
    """Customized uvicorn.Server

    Uvicorn server overrides signals, and we need to include
    Rocketry to the signals."""

    def handle_exit(self, sig: int, frame) -> None:
        rocketry_app.session.shut_down()
        return super().handle_exit(sig, frame)


async def main():
    """Run scheduler and the API"""
    server = Server(config=uvicorn.Config(
        fastapi_app,
        host='127.0.0.1',
        port=5000,
        reload=True))

    api = asyncio.create_task(server.serve())
    schedule = asyncio.create_task(rocketry_app.serve())

    await asyncio.wait([schedule, api])


if __name__ == "__main__":
    asyncio.run(main())
