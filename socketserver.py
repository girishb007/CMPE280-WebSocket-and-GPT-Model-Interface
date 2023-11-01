#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import websockets
from random import randint

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send('[' + str(randint(1, 10)) + '] ' + message)

async def main():
    server = await websockets.serve(echo, "localhost", 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
