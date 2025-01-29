from aiohttp import web 
import socketio
import socketio.exceptions

MAX_PLAYER_COUNT = 4

# TODO: Print a graceful message of failure to accomodate > 4 players


sio  = socketio.AsyncServer()
app = web.Application()

sio.attach(app)


active_users = 0

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
def connect(sid, environ):
    global active_users
    if active_users >= MAX_PLAYER_COUNT:
        return False

    active_users += 1
    print("connect ", sid)

@sio.event
async def chat_message(sid, data):
    print("message ", data)
    
@sio.event
def disconnect(sid):
    global active_users
    active_users -= 1
    print("disconnect ", sid)

# app.router.add_static('/static', 'static')
app.router.add_get('/', index)


if __name__ == "__main__":
    web.run_app(app)