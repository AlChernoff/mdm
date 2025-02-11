
import json

from fastapi import WebSocket, WebSocketDisconnect

connected_clients: list[WebSocket] = []

async def connect_websocket(websocket: WebSocket):
    """
    Accepts a new WebSocket connection and saves it in connected_clients.
    """
    await websocket.accept()
    connected_clients.append(websocket)

async def disconnect_websocket(websocket: WebSocket):
    """
    Removes a WebSocket connection from connected_clients.
    """
    connected_clients.remove(websocket)

async def handle_websocket_messages(websocket: WebSocket):
    """
    Continuously listens for messages from the client.
    In this example, we don't do anything with them.
    """
    try:
        while True:
            await websocket.receive_text()  # or receive_json()
    except WebSocketDisconnect:
        await disconnect_websocket(websocket)

async def notify_device_change(device_id: int, change_type: str):
    """
    Broadcasts a device change notification to all connected clients.
    Args:
        device_id   : The ID of the changed device.
        change_type : A string describing the change (e.g., 'created', 'updated', 'deleted').
    """
    message = {
        "device_id": device_id,
        "change_type": change_type
    }
    message_str = json.dumps(message)

    # Send the message to every connected client
    for client in connected_clients:
        try:
            await client.send_text(message_str)
        except Exception:
            # Handle client sending failures if needed
            pass