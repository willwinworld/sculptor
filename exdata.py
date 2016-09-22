#! python2
# -*- coding: utf-8 -*-
from peewee import *


db = SqliteDatabase('exdata.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class Customers(BaseModel):
    cust_id = CharField(null=False, max_length=10, primary_key=True, verbose_name='唯一的顾客ID')  # 主键
    cust_name = CharField(null=False, max_length=50, verbose_name='顾客名')
    cust_address = CharField(null=True, max_length=50, verbose_name='顾客的地址')
    cust_city = CharField(null=True, max_length=50, verbose_name='顾客所在城市')
    cust_state = CharField(null=True, max_length=5, verbose_name='顾客所在州')
    cust_zip = CharField(null=True, max_length=10, verbose_name='顾客地址邮政编码')
    cust_country = CharField(null=True, max_length=50, verbose_name='顾客所在国家')
    cust_contact = CharField(null=True, max_length=50, verbose_name='顾客联系名')
    cust_email = CharField(null=True, max_length=255, verbose_name='顾客的电子邮件地址')


class Orders(BaseModel):
    order_num = IntegerField(null=False, primary_key=True, verbose_name='唯一的订单号')  # 主键
    order_date = DateTimeField(null=False, verbose_name='订单日期')
    cust_id = ForeignKeyField(Customers, related_name='orders', null=False, verbose_name='订单顾客ID')


class Vendors(BaseModel):
    vend_id = CharField(null=False, max_length=10, primary_key=True, verbose_name='唯一的供应商ID')  # 主键
    vend_name = CharField(null=False, max_length=50, verbose_name='供应商名')
    vend_address = CharField(null=True, max_length=50, verbose_name='供应商的地址')
    vend_city = CharField(null=True, max_length=50, verbose_name='供应商所在城市')
    vend_state = CharField(null=True, max_length=5, verbose_name='供应商所在州')
    vend_zip = CharField(null=True, max_length=10, verbose_name='供应商地址邮政编码')
    vend_country = CharField(null=True, max_length=50, verbose_name='供应商所在国家')


class Products(BaseModel):
    prod_id = CharField(null=False, max_length=10, primary_key=True, verbose_name='唯一的产品ID')  # 主键
    vend_id = ForeignKeyField(Vendors, related_name='products', null=False, verbose_name='产品供应商ID')
    prod_name = CharField(null=False, max_length=255, verbose_name='产品名')
    prod_price = DecimalField(null=False, max_digits=8, decimal_places=2, verbose_name='产品价格')
    prod_desc = TextField(null=True, verbose_name='产品描述')


class OrderItems(BaseModel):
    order_num = ForeignKeyField(Orders, related_name='items', null=False, verbose_name='订单号')  # 主键
    order_item = IntegerField(null=False, verbose_name='订单物品号')  # 主键
    prod_id = ForeignKeyField(Products, related_name='items', null=False, verbose_name='产品ID')
    quantity = IntegerField(null=False, verbose_name='物品数量')
    item_price = DecimalField(null=False, max_digits=8, decimal_places=2, verbose_name='物品价格')

    class Meta:
        primary_key = CompositeKey('order_num', 'order_item')


if __name__ == '__main__':
    Customers.create_table()
    OrderItems.create_table()
    Orders.create_table()
    Products.create_table()
    Vendors.create_table()
