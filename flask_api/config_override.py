"""
Override configurations.
"""

configs = {
    "flask_debug": False,
    "flask_server_name": "localhost:5000",
    "qiniu": {
        "access_key": "",
        "secret_key": "",
        "bucket_name": ""
    },
    "db": {
        "redis_url": "redis://redis:6379/1"
    }
}
