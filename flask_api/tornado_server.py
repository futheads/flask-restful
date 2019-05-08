from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask_api.app import app

from flask_api.config import configs


if configs["cert"]["cert_key_path"] and configs["cert"]["cert_crt_path"]:
    http_server = HTTPServer(WSGIContainer(app), ssl_options={
        "certfile": configs["cert"]["cert_key_path"],
        "keyfile": configs["cert"]["cert_crt_path"],
    })
    http_server.listen(443)  # flask默认的端口
else:
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)  # flask默认的端口
    IOLoop.instance().start()

