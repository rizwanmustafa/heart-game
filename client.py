import asyncio
import socketio
import socketio.exceptions

DEFAULT_SERVER_ADDRESS = 'http://localhost:8080'

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("Connection established!")
    
@sio.event
async def my_message(data):
    print("message recieved with ", data)
    await sio.emit('my response', { 'response': 'my response'})

@sio.event
async def connect_error(reason):
    if reason == sio.reason.CLIENT_DISCONNECT:
        print("The client disconnected!")
    elif reason == sio.reason.SERVER_DISCONNECT:
        print("The server disconnected!")
    else:
        print("Reason for disconnection:", reason)

@sio.event
async def disconnect():
    print("Disconnected from server!")

async def main():
    server_address = input("Enter server address: ")
    if server_address.strip() == "":
        print("No server address provided! Using the default one!")
        server_address = DEFAULT_SERVER_ADDRESS

    try:
        await sio.connect(server_address)
        await sio.wait()
    except socketio.exceptions.ConnectionError as e:
        print("ConnectionError:", e)
    except Exception as e:
        print("An error occurred:", e)
    
if __name__ == "__main__":
    asyncio.run(main())