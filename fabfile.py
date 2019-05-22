import os, re

from datetime import datetime
from fabric.api import *
from functools import cmp_to_key

env.hosts = "localhost"
env.user = "futhead"
env.password = "futhead"
env.sudo_user = "root"

_TAR_FILE = "dist-webapp.tar.gz"

_REMOTE_TMP_TAR = "/tmp/%s" % _TAR_FILE

_REMOTE_BASE_DIR = "/home/futhead"


def _now():
    return datetime.now().strftime("%y-%m-%d_%H.%M.%S")


def _current_path():
    return os.path.abspath(".")


def build():
    """
    Build dist package.
    """
    includes = ["flask_api", "requirements.txt", "tornado_server.py"]
    excludes = [".pytest_cache", "__pycache__"]
    local("rm -f dist/%s" % _TAR_FILE)
    with lcd(os.path.join(_current_path())):
        cmd = ["tar", "--dereference", "-czvf", "dist/%s" % _TAR_FILE]
        cmd.extend(["--exclude=\"%s\"" % ex for ex in excludes])
        cmd.extend(includes)
        local(" ".join(cmd))


def deploy():
    newdir = "www-%s" % _now()
    run("rm -f %s" % _REMOTE_TMP_TAR)
    put("dist/%s" % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo("mkdir %s" % newdir)
    with cd("%s/%s" % (_REMOTE_BASE_DIR, newdir)):
        sudo("tar -xzvf %s" % _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo("rm -f www")
        sudo("ln -s %s www" % newdir)
        sudo("chown futhead:futhead www")
        sudo("chown -R futhead:futhead %s" % newdir)
    with settings(warn_only=True):
        sudo("supervisorctl stop tornado_server")
        sudo("supervisorctl start tornado_server")


RE_FILES = re.compile("\r?\n")


def rollback():
    """
    rollback to previous version
    """
    with cd(_REMOTE_BASE_DIR):
        r = run("ls -p -1")
        files = [s[:-1] for s in RE_FILES.split(r) if s.startswith("www-") and s.endswith("/")]
        files.sort(key=cmp_to_key(lambda s1, s2: 1 if s1 < s2 else -1))
        r = run("ls -l www")
        ss = r.split(" -> ")
        if len(ss) != 2:
            print("ERROR: \"www\" is not a symbol link.")
            return
        current = ss[1]
        print("Found current symbol link points to: %s\n" % current)
        try:
            index = files.index(current)
        except ValueError:
            print("ERROR: symbol link is invalid.")
            return
        if len(files) == index + 1:
            print("ERROR: already the oldest version.")
        old = files[index + 1]
        print("==================================================")
        for f in files:
            if f == current:
                print("      Current ---> %s" % current)
            elif f == old:
                print("  Rollback to ---> %s" % old)
            else:
                print("                   %s" % f)
        print("==================================================")
        print("")
        yn = input("continue? y/N ")
        if yn != "y" and yn != "Y":
            print("Rollback cancelled.")
            return
        print("Start rollback...")
        sudo("rm -f www")
        sudo("ln -s %s www" % old)
        sudo("chown futhead:futhead www")
        with settings(warn_only=True):
            sudo("supervisorctl stop tornado_server")
            sudo("supervisorctl start tornado_server")
        print("ROLLBACKED OK.")
