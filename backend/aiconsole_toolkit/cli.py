import argparse
import asyncio
from aiconsole.api.websockets.client_messages import OpenChatClientMessage, ProcessChatClientMessage
from aiconsole.app import app
from fastapi.testclient import TestClient
import os

#
# This is a playground for building a CLI for the backend.
#


async def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="AI Console")

    os.environ["CORS_ORIGIN"] = "http://localhost:3000"

    # Add any command line arguments you need
    parser.add_argument("--input", help="Who are you?")

    # Parse the command line arguments
    args = parser.parse_args()

    # Call the app function to get the FastAPI app
    fastapi_app = app()

    with TestClient(fastapi_app) as client:
        response = client.post("/api/projects/choose", json={"directory": "../test"})

        # Print the response content
        print(response)
        print(response.content)

        with client.websocket_connect("/ws") as websocket:
            data = websocket.receive_json()
            print(data)

            chat_info = client.get("/api/chats").json()[0]

            print(chat_info["name"])

            chat = client.get(f"/api/chats/{chat_info['id']}").json()

            await OpenChatClientMessage(chat_id=chat_info["id"]).send(websocket)

            request_id = "test"
            await ProcessChatClientMessage(chat_id=chat_info["id"], request_id=request_id).send(websocket)

            while True:
                data = websocket.receive_json()
                print(data)
                if data["type"] == "LockReleasedServerMessage" and data["request_id"] == "test":
                    break


if __name__ == "__main__":
    asyncio.run(main())
