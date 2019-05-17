from flask_migrate import Migrate, MigrateCommand
from learn_migrate import app, db
from flask_script import Manager

migrate = Migrate(app, db)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    # https://www.cnblogs.com/terrycy/p/7357194.html
    # https://www.cnblogs.com/liuwei0824/p/8297067.html
    # http://www.pythondoc.com/flask-mega-tutorial/database.html

