# !/usr/bin/env python
# -*- coding: utf-8 -*-


from peewee import *
from scratch.utils import Setting
from datetime import datetime

try:
    import psycopg2
    from playhouse.pool import PooledPostgresqlExtDatabase

    db = PooledPostgresqlExtDatabase(
        Setting.pg_database,
        max_connections=8,
        stale_timeout=300,
        user=Setting.pg_user,
        host=Setting.pg_host,
        password=Setting.pg_passwd,
        autorollback=True,
        register_hstore=False)
except ImportError:
    db = SqliteDatabase('tm.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class TMseries(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='商品系列id')
    brand = CharField(max_length=50, null=True, verbose_name='品牌')
    series = CharField(max_length=50, null=False, verbose_name='系列')


class TMshop(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='商店id')
    name = CharField(max_length=50, null=False, unique=True, verbose_name='店名')

    good_score = FloatField(null=True, verbose_name='商品评分')
    service_score = FloatField(null=True, verbose_name='服务评分')
    logistics_score = FloatField(null=True, verbose_name='物流评分')
    good_compare = CharField(max_length=10, null=True, verbose_name='商品相比行业')
    service_compare = CharField(max_length=10, null=True, verbose_name='服务相比行业')
    logistics_compare = CharField(max_length=10, null=True, verbose_name='物流相比行业')
    is_hk = BooleanField(default=False, verbose_name='是否天猫国际')


class TMproduct(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='商品id')
    shop = ForeignKeyField(TMshop, related_name='products', verbose_name='商店')
    name = CharField(max_length=500, null=False, verbose_name='商品名称')
    symbol = CharField(max_length=1, default=u'￥', verbose_name='价格符号')
    price = FloatField(null=False, verbose_name='价格')
    func = CharField(max_length=20, null=True, verbose_name='功效')
    made_in = CharField(max_length=20, null=True, verbose_name='产地')
    net_vol = CharField(max_length=20, null=True, verbose_name='净含量')
    variety_model = CharField(max_length=20, null=True, verbose_name='规格')
    colors = CharField(max_length=500, null=True, verbose_name='所有颜色分类')
    month_sell = IntegerField(default=0, verbose_name='月销量')
    sum_sell = IntegerField(default=0, verbose_name='产品总销量')
    series = ForeignKeyField(TMseries, related_name='products', verbose_name='系列id')
    is_hk = BooleanField(default=False, verbose_name='是否天猫国际')

    created_time = DateTimeField(default=datetime.now, verbose_name='创建时间')


class TMcolor(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='颜色分类id')
    product = ForeignKeyField(TMproduct, related_name='choosecolor', verbose_name='产品id')
    color = CharField(max_length=20, null=False, verbose_name='颜色')


class TMreview(BaseModel):
    product = ForeignKeyField(TMproduct, primary_key=True, related_name='reviews', verbose_name='商品id')
    commtags = CharField(max_length=500, null=True, verbose_name='买家印象')
    score = FloatField(null=True, verbose_name='商品评分')
    count = IntegerField(default=0, verbose_name='评论数')
    collect = IntegerField(default=0, verbose_name='收藏数')
    pic = TextField(null=True, verbose_name='年龄分布图')


class TMuser(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='用户')
    name = CharField(max_length=20, null=False, verbose_name='用户名')
    is_anonym = BooleanField(default=True, verbose_name='是否匿名')
    level = CharField(max_length=10, null=True, verbose_name='用户等级')


class TMtag(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='买家印象id')
    product = ForeignKeyField(TMproduct, related_name='tags', verbose_name='商品id')
    tag = CharField(max_length=10, null=False, verbose_name='买家印象')

    class Meta:
        indexes = ((('id', 'product'), True),)


class TMage(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='年龄id')
    age = CharField(null=False, verbose_name='年龄段')


class TMcomment(BaseModel):
    id = BigIntegerField(null=False, primary_key=True, verbose_name='评论')
    product = ForeignKeyField(TMproduct, related_name='comments', verbose_name='商品id')
    shop = ForeignKeyField(TMshop, related_name='comments', verbose_name='商店')
    series = ForeignKeyField(TMseries, related_name='comments', verbose_name='系列id')
    choose = ForeignKeyField(TMcolor, related_name='comments', verbose_name='颜色分类id')
    age = ForeignKeyField(TMage, null=True, related_name='comments', verbose_name='年龄分段')

    content = TextField(null=True, verbose_name='内容')
    user = ForeignKeyField(TMuser, null=True, related_name='comments', verbose_name='用户名')
    date = DateField(null=True, verbose_name='评论日期')

    created_time = DateTimeField(default=datetime.now, verbose_name='创建时间')


class TMcommenttag(BaseModel):
    comment = ForeignKeyField(TMcomment, related_name='comment_tags', verbose_name='comment id')
    tag = ForeignKeyField(TMtag, related_name='comment_tags', verbose_name='tag id')
    highlight = CharField(max_length=1000, null=True, verbose_name='红字')

    class Meta:
        primary_key = CompositeKey('comment', 'tag')


class TMhistory(BaseModel):
    id = PrimaryKeyField(null=False, verbose_name=u'历史id')
    product = BigIntegerField(null=False, verbose_name='商品id')
    month_sell = IntegerField(default=0, verbose_name='月销量')
    sum_sell = IntegerField(default=0, verbose_name='产品总销量')
    comment_num = IntegerField(default=0, verbose_name='评论数')

    created_time = DateTimeField(default=datetime.now, verbose_name='创建时间')


if __name__ == '__main__':
    try:
        from fnvhash import fnv1a_32

        TMhistory.create_table()
        TMseries.create_table()
        TMshop.create_table()
        TMproduct.create_table()
        TMcolor.create_table()
        TMreview.create_table()
        TMuser.create_table()
        TMage.create_table()
        TMtag.create_table()
        TMcomment.create_table()
        TMcommenttag.create_table()
        for i in [u'全部年龄', u'18岁以下', u'18-24', u'25-29', u'30-40', u'40岁以上']:
            TMage.create(id=fnv1a_32(repr(i)), age=i)
    except Exception, err:
        print err