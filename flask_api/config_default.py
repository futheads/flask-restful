"""
Default configurations.
"""
configs = {
    "flask_debug": True,
    "flask_server_name": "127.0.0.1:5000",
    "db": {
        "sqlalchemy_database_uri": "sqlite:///db.sqlite",
        "sqlalchemy_track_modifications": False,
        "redis_url": "redis://localhost:6379/1"
    },
    "flaskplus": {
        "restplus_swagger_ui_doc_expansion": "list",
        "restplus_validate": True,
        "restplus_mask_swagger": False,
        "restplus_error_404_help": False
    },
    "cert": {
        "cert_crt_path": "",
        "cert_key_path": ""
    },
    "qiniu": {
        "access_key": "",
        "secret_key": "",
        "bucket_name": ""
    },
    "mail": {
        "server": "localhost",
        "port": 25,
        "username": None,
        "password": None
    }
}
