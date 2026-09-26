from textual_serve.server import Server

server = Server(
    "python main.py",
    host="127.0.0.1",
    port=8000
)
server.serve()