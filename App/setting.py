
class Config:
    #mysql
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123456'
    # SESSION_TYPE = 'redis'
    expire_on_commit = True

    # 邮箱设置
    MAIL_SERVER = 'smtp.aliyun.com'  # smtp服务器
    # MAIL_USE_TLS=True
    MAIL_PORT = 25  # 不加密的为25端口
    MAIL_USERNAME = 'xialab@aliyun.com'
    MAIL_PASSWORD = 'hello.c101'
    MAIL_DEFAULT_SENDER = ('C101', 'xialab@aliyun.com')  # 第一个为发件人名字，可自由设置，第二个为发件邮箱

def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE") or "sqlite"
    driver = dbinfo.get("DRIVER") or "sqlite"
    user = dbinfo.get("USER") or ""
    password = dbinfo.get("PASSWORD") or ""
    host = dbinfo.get("HOST") or ""
    post = dbinfo.get("POST") or ""
    name = dbinfo.get("NAME") or ""
    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, post, name)


class DevelopConfig(Config):
    DEBUG = True
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "mysqlconnector",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "POST": "3306",
        "NAME": "dbdsmv2.1"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestConfig(Config):
    TESTING = True
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "mysqlconnector",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "POST": "3306",
        "NAME": "dbdsmv2.1"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "mysqlconnector",
        "USER": "root",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "POST": "3306",
        "NAME": "dbdsmv2.1"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "mysqlconnector",
        "USER": "root",
        "PASSWORD": "123456",
        "NAME": "dbdsmv2.1",
        "HOST": "localhost",
        "POST": "3306"
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}
