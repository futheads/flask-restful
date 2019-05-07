from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_api.app import app

from flask_api.config import CERT_CRT_PATH, CERT_KEY_PATH


if CERT_KEY_PATH and CERT_CRT_PATH:
    http_server = HTTPServer(WSGIContainer(app), ssl_options={
        "certfile": CERT_CRT_PATH,
        "keyfile": CERT_KEY_PATH,
    })
    http_server.listen(443)  # flask默认的端口
else:
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)  # flask默认的端口
    IOLoop.instance().start()

