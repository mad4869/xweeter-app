from . import app
from .extensions import socket

if __name__ == "__main__":
    socket.run(app)
