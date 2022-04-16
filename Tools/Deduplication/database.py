#coding=utf-8

import pymysql
import sqlalchemy
from sqlalchemy import Column, Integer, BigInteger, String, VARCHAR, TEXT, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

__engine = None

__Base = declarative_base()

class Repository(__Base):
    __tablename__ = 'repository'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(1024), nullable=False)

    def to_dict(self):
        model = dict(self.__dict__)
        del model['_sa_instance_state']
        return model

class Image(__Base):
    __tablename__ = 'image'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tag = Column(String(256), nullable=False)
    digest = Column(String(128), nullable=False, comment='manifest sha256 (ID)')
    repo_digest = Column(String(128), nullable=False, comment='repository digest')
    size = Column(BigInteger, nullable=False, comment='Byte')
    layer_num = Column(Integer, nullable=False)
    repo_id = Column(BigInteger, ForeignKey('repository.id'), nullable=False)

    def to_dict(self):
        model = dict(self.__dict__)
        del model['_sa_instance_state']
        return model

class Layer(__Base):
    __tablename__ = 'layer'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    digest = Column(String(128), nullable=False, comment='compressed sha256')
    diff_id = Column(String(128), nullable=False, comment='uncompressed sha256')
    chain_id = Column(String(128), nullable=False)
    cache_id = Column(String(128), nullable=False)
    level = Column(Integer, nullable=False)
    abs_path = Column(TEXT, nullable=False)
    compressed_size = Column(BigInteger, nullable=False, comment='Byte')
    uncompressed_size = Column(BigInteger, nullable=False, comment='Byte')
    repo_id = Column(BigInteger, ForeignKey('repository.id'), nullable=False)
    image_id = Column(BigInteger, ForeignKey('image.id'), nullable=False)

    def to_dict(self):
        model = dict(self.__dict__)
        del model['_sa_instance_state']
        return model

class File(__Base):
    __tablename__ = 'file'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    abs_path = Column(TEXT, nullable=False,\
        comment='absolute path within the local storage, with file name included')
    root_path = Column(TEXT, nullable=False,\
        comment='absolute path within the image, with file name included')
    md5 = Column(String(64), nullable=False)
    size = Column(BigInteger, nullable=False, comment='Byte')
    repo_id = Column(BigInteger, ForeignKey('repository.id'), nullable=False)
    image_id = Column(BigInteger, ForeignKey('image.id'), nullable=False)
    layer_id = Column(BigInteger, ForeignKey('layer.id'), nullable=False)

    def to_dict(self):
        model = dict(self.__dict__)
        del model['_sa_instance_state']
        return model

def init(user: str, psw: str, database: str):
    __set_charset(user, psw, database)
    global __engine
    __engine = sqlalchemy.create_engine("mysql+pymysql://%s:%s@%s:3306/%s?charset=utf8" %(user, psw, database, database))

def __set_charset(user: str, psw: str, database: str):
    conn = pymysql.connect(host=database ,user=user, passwd=psw, port=3306, db='mysql', charset='utf8')
    cur = conn.cursor()
    cur.execute('use mysql')
    cur.execute('set global character_set_database=utf8')
    cur.execute('set global character_set_database=utf8')
    cur.execute('create database if not exists %s' %database)
    cur.close()
    conn.close()

def create_all_tables():
    __Base.metadata.create_all(__engine)

def drop_all_and_create_all_tables():
    __Base.metadata.drop_all(__engine)
    create_all_tables()

def Session():
    if __engine is None:
        raise ValueError("None error, sqlalchemy engine has not been or failed to be created")
    return sessionmaker(bind=__engine)
