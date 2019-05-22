# flask-restful
## 写在前面
机缘巧合，这段时间刚好有空，所以整合了一个restful风格的开发框架，包括swagger文档，ORM，数据库迁移，热发布，服务监控，日志和异常的统一处理，一键部署到服务器（支持多台）及一些常用功能，使用redis存储token鉴权，天然支持分布式，通过大量的整合扩展库来减少了代码量，提高了开发效率。  
目标是一个人能hold住一个中型项目
## Quick start
### 初始化
```
git clone git@github.com:futheads/flask-restful.git
cd flask-restful
pip install -r requirements.txt
python tornado_server.py
```
浏览器访问API文档页面 [http://localhost:5000/api/](http://localhost:5000/api/)
## web核心框架
web框架使用的是Flask的升级版：[Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/)，以下是Flask-RESTPlus的官方说明
>Flask-RESTPlus是Flask的扩展，增加了对快速构建REST API的支持。Flask-RESTPlus鼓励以最少的设置进行最佳实践。如果你熟悉Flask，Flask-RESTPlus应该很容易上手。它提供了一个连贯的装饰器和工具集合来描述您的API并通过swagger来公开文档
## ORM
使用了Flask的插件[Flask-SQLAlchemy](http://www.pythondoc.com/flask-sqlalchemy/quickstart.html)，Flask-SQLAlchemy在SQLAlchemy的基础上，提供了一些常用的工具，并预设了一些默认值,对于基本应用十分容易使用，并且对大型项目易于扩展。
## 数据库迁移
使用了Flaks的插件[Flask-Migrate和Flask-Script](https://flask-migrate.readthedocs.io/en/latest/)。实际使用过程中发现有个小坑，在第一次执行  
`python manage.py db init`  
生成sqlite数据库，修改migrations/env.py文件，在context.configure中添加render_as_batch=True，否则再删除和修改列时会报错
```buildoutcfg
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            render_as_batch=True,
            **current_app.extensions['migrate'].configure_args
        )
```
常用命令：  
* 初始化： `python manage.py db init`
* 创建一个版本： `python manage.py db migrate -m "some comments"`
* 更新版本到数据库： `python manage.py db upgrade`
* 退回到上个版本： `python manage.py db downgrade`
* 查看历史版本： `python manage.py db history`
* 跳转到指定版本：`python manage.py db downgrade 指定版本号`  
## 配置文件
使用Python源代码来实现配置，有两个配置文件： config_default.py 和 config_override.py，config_default配置默认值和本地开发环境，需要更改时只要把要修改的变量加入到config_override文件中就行，系统会自动覆盖  
eg. 
```buildoutcfg
from flask_api.config import configs

access_key = configs["qiniu"]["access_key"]
secret_key = configs["qiniu"]["secret_key"]
```
## 热发布
开发过程中可以运行hot_deploy.py文件，该脚本使用watchdog对当前目录下所有后缀为.py的文件进行监控，只要有变化，就会重启tornado_server.py，省去了开发过程中无休止的重启操作，参考廖雪峰的[Day 13 - 提升开发效率](https://www.liaoxuefeng.com/wiki/1016959663602400/1018491156860224)
## 日志
使用logging，通过文件[logging.ini配置](https://docs.python.org/3/library/logging.config.html)，目前支持console、file及mail三种处理方式
## 部署
### 集成tornado服务器
使用tornado作为服务器，可以直接运行tornado_server.py启动项目，如果配置了证书，则默认启动https服务，否则启动http服务
## 服务监控
使用supervisor，配置写在supervisord.ini，具体参考[使用 supervisor 管理进程](http://liyangliang.me/posts/2015/06/using-supervisor/)
### fabric: 自动部署
使用[fabric3](http://www.fabfile.org/)自动打包发布项目，并支持回滚
常用操作（不指定脚本文件默认执行fabfile.py）：  
* 打包：fab build
* 部署：fab deploy
* 回滚：fab rollback
## 单元测试
这里直接使用[requests](https://2.python-requests.org//zh_CN/latest/)对api接口测试
## 一些常用功能
### 异常统一处理
在flask_api/api/errors.py文件定义各种异常，在合适的地方直接用raise抛出即可
### 登录及鉴权
用户登录成功后生成token并存入redis，在调用需要鉴权的接口时以header参数传入。  
登录成功后会将当前用户信息绑定到flask的g上，方便业务层使用  
鉴权使用了decorators模式，在需要权限的接口定义上加@login_check即可。  
eg.
```buildoutcfg
@ns.route("/user")
class UserInfo(Resource):

    @login_check
    def get(self):
        pass
```
在swagger页面调试token鉴权，点击Authorized填入token，实现参考flask_api/api/restplus.py
```buildoutcfg
authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "token"
    },
}

api = Api(security="Bearer Auth", authorizations=authorizations, version="1.0", title="Micro Blog API",
          description="A simple demonstration of a Flask RestPlus powered API")
```
不需要鉴权的接口需要添加@api.doc(security=None)  
eg.
```buildoutcfg
@ns.route("/login")
class UserLogin(Resource):

    @api.doc(security=None)
    def post(self):
        pass
```
### 多线程实现异步
使用了decorators模式，在需要异步执行的方法上加@async注解即可，具体代码可以参考flask_api/api/restplus.py和flask_api/api/utils.py  
eg.
```buildoutcfg
@async
def send_async_email(_app, msg):
    with _app.app_context():
        mail.send(msg)
```
### 文件管理
如果外网的话可以考虑用七牛，采用后端提供授权，前端拿到授权直接传到七牛云并将返回的文件地址再传给后端。具体代码可以参考flask_api/api/utils.py  
如果是内网，建议用异步吧
### 请求日志记录
使用了decorators模式，在需要记录请求参数及响应数据的方法定义上加@log_record即可  
eg.
```buildoutcfg
@ns.route("/user")
class UserInfo(Resource):

    @log_record
    def get(self):
        pass
```
### 邮件
使用了Flask的插件[Flask-Mail](https://pythonhosted.org/Flask-Mail/)，Flask-Mail提供了一个简单的接口来集成SMTP与Flask应用程序并发送邮件，具体实现参考app.py和flask_api/api/utils.py  
### 短信验证码
没有接入第三方的短信平台，但实现了短信验证的逻辑，具体参考flask_api/api/commons/endpoints/common.py
## 参考文档
* [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/)
* [Flask-SQLAlchemy](http://www.pythondoc.com/flask-sqlalchemy/quickstart.html)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Logging configuration](https://docs.python.org/3/library/logging.config.html)
* [Flask-Mail](https://pythonhosted.org/Flask-Mail/)
* [fabric3](http://www.fabfile.org/)
* [廖雪峰Python教程：实战](https://www.liaoxuefeng.com/wiki/1016959663602400/1018138095494592)
* [Flask大型教程项目](http://www.pythondoc.com/flask-mega-tutorial/index.html)
* [描述怎样通过flask+redis+sqlalchemy等工具，开发restful api](https://www.cnblogs.com/ExMan/p/9510019.html)
* [使用 supervisor 管理进程](http://liyangliang.me/posts/2015/06/using-supervisor/)
## 关于作者
futhead，2013年6月毕业于某二流大学核化工与核燃料工程专业，后在某IDC机房做网管，期间自学编程，依次从事过Android，PHP，JavaWeb，前端，测试，运维，GIS，大数据等相关开发工作，如无意外，下份工作应该是Python全栈，侧重NLP方向。
## 参与贡献
1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request