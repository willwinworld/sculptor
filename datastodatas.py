#! python2
# -*- coding: utf-8 -*-
from peewee import *


db = SqliteDatabase('dstods.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class News(BaseModel):
    news_id = IntegerField(null=False, primary_key=True, verbose_name='新闻ID')  # 主键
    title = CharField(null=False, max_length=100, verbose_name='新闻标题')
    content = TextField(null=False, verbose_name='新闻内容')
    comment = TextField(null=True, verbose_name='新闻评论')
    publish_date = DateTimeField(null=False, verbose_name='出版日期')


class Category(BaseModel):
    category_id = IntegerField(null=False, primary_key=True, verbose_name='新闻种类ID')  # 主键
    name = CharField(null=False, max_length=100, verbose_name='新闻种类名')


class Category_News(BaseModel):  # 中间表, 多对多关系
    id = PrimaryKeyField(null=False, primary_key=True, verbose_name='自增主键')  # 自增主键
    news_id = ForeignKeyField(News, related_name='news')
    category_id = ForeignKeyField(Category, related_name='categories')


if __name__ == '__main__':
    News.create_table()
    Category.create_table()
    Category_News.create_table()
