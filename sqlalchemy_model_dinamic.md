from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

engine = create_engine('mysql+mysqlconnector://root:mysql@localhost:3306/pydb')

Base = automap_base()
Base.prepare(engine, reflect=True)
print('开始')
print(Base.classes)
print([i for i in Base.classes])
# 反射得到orm
News = Base.classes.news
Macd = Base.classes.macd_info

# 通信
session = Session(bind=engine)


# 插入数据
def insert():
    h = News(name="vcr", age=67, sex=1, create_time=datetime.now())
    session.add(h)
    #session.add_all([x,y])
    session.commit()

# 修改数据
def update():
    h_obj = session.query(News).filter_by(name="vcr").first()
    h_obj.name = "vccrr"
    session.add(h_obj)
    session.commit()

# 删除数据
def delete():
    h_obj = session.query(News).filter_by(name="vccrr").first()
    session.delete(h_obj)
    session.commit()

# 查询数据
def select():
    # res = session.query(News).filter(News.Id > 7)
    res = session.query(Macd).filter(Macd.index > 1000)
    print([i for i in res])
    return res


if __name__ == "__main__":
    select()
    
    
# 生成Model方式
使用包sqlacodegen
安装pip install sqlacodegen
使用命令：sqlacodegen mysql://root:root@127.0.0.1:3306/mydb > models.py即可在当前目录生成models.py文件 
