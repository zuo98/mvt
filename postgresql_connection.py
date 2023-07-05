# 导入 psycopg2 模块和 Error 对象
import psycopg2
from psycopg2 import DatabaseError
from configparser import ConfigParser
from string import Template


def read_db_config(filename='dbconfig.ini', section='postgresql'):
    """ 读取数据库配置文件，返回一个字典对象
    """
    # 创建解析器，读取配置文件
    parser = ConfigParser()
    parser.read(filename)

    # 获取 postgresql 部分的配置
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('文件 {1} 中未找到 {0} 配置信息！'.format(section, filename))
    print(db)
    return db


def get_mvt(z, x, y):
    db_config = read_db_config()
    connection = None
    db_version = None

    try:
        # 使用 psycopg2.connect 方法连接 PostgreSQL 数据库
        connection = psycopg2.connect(**db_config)
        print(connection)
        # 创建一个游标
        cur = connection.cursor()

        sql = Template("select * from vector_tile_test(${z}, ${x}, ${y});")

        sql = sql.safe_substitute(z=z, x=x, y=y)

        print('sql:', sql)

        # 获取 PostgreSQL 版本号
        cur.execute(sql)
        print('cur', cur)
        db_version = cur.fetchone()[0].tobytes()

        # 输出 PostgreSQL 版本
        print("连接成功，PostgreSQL 服务器版本：", db_version)

        # 关闭游标
        cur.close()
    except (Exception, DatabaseError) as e:
        print("连接 PostgreSQL 失败：", e)
    finally:
        # 释放数据库连接
        if connection is not None:
            connection.close()
            print("PostgreSQL 数据库连接已关闭。")
        return db_version
