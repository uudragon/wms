from time import timezone
from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=32, unique=True)
    product_name = models.CharField(db_column='PRODUCT_NAME', null=False, max_length=200)
    product_desc = models.CharField(db_column='PRODUCT_DESC', null=True, max_length=500)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True, default=timezone.now)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True, default=timezone.now)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)

    class Meta:
        db_table = 'T_PRODUCT'


class ProductDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=32)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=32)
    goods_qty = models.IntegerField(db_column='GOODS_QTY', null=False, default=1)
    is_gift = models.SmallIntegerField(db_column='IS_GIFT', null=False, default=0)

    class Meta:
        db_table = 'T_PRODUCT_DETAILS'


class Warehouse(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    code = models.CharField(db_column='CODE', null=False, max_length=99, unqiue=True)
    name = models.CharField(db_column='NAME', null=False, max_length=255, unqiue=True)
    address = models.CharField(db_column='ADDRESS', null=False, max_length=255)
    type = models.SmallIntegerField(db_column='TYPE', null=False, default=1)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True, default=timezone.now)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True, default=timezone.now)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)

    class Meta:
        db_table = 'T_WAREHOUSE'


class StorageRecord(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=32)
    goods_qty = models.IntegerField(db_column='GOODS_QTY', null=False, default=1)
    code = models.CharField(db_column='CODE', null=False, max_length=50)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, max_length=99)
    type = models.SmallIntegerField(db_column='TYPE', null=False, default=1)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True, default=timezone.now)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True, default=timezone.now)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)

    class Meta:
        db_table = 'T_STORAGE_RECORD'


class Receipt(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    code = models.CharField(db_column='CODE', null=False, max_length=50, unique=True)
    receipt_date = models.DateTimeField(db_column='RECEIPT_DATE', null=False)
    receipt_desc = models.CharField(db_column='RECEIPT_DESC', null=True, max_length=255)
    receipt_stat = models.SmallIntegerField(db_column='RECEIPT_STAT', null=True, default=0)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, default=32)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True, default=timezone.now)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True, default=timezone.now)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)

    class Meta:
        db_table = 'T_RECEIPT'


class ReceiptDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=32)
    goods_qty = models.IntegerField(db_column='GOODS_QTY', null=False, default=1)
    code = models.CharField(db_column='CODE', null=False, max_length=50)
    status = models.SmallIntegerField(db_column='STATUS', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True, default=timezone.now)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True, default=timezone.now)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_RECEIPT_DETAILS'


class WarehouseDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    warehouse_code = models.CharField(db_column='WAREHOUS_CODE', null=False, max_length=50)
    goods_code = models.CharField(db_column='QOODS_CODE', null=False, max_length=32)
    qty = models.IntegerField(db_column='QTY', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True, default=timezone.now)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True, default=timezone.now)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_WAREHOUSE_DETAILS'


class Goods(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goodsType = models.IntegerField(db_column='GOODS_TYPE', max_length=4, null=False, default=1)
    goodsCode = models.CharField(db_column='GOODS_CODE', max_length=32, null=False)
    goodsName = models.CharField(db_column='GOODS_NAME', max_length=200, null=False)
    goodsPrice = models.DecimalField(db_column='GOODS_PRICE', max_digits=10, decimal_places=2)
    goodsBulk = models.DecimalField(db_column='GOODS_BULK', max_digits=20, decimal_places=2)
    goodsWeight = models.DecimalField(db_column='GOODS_WEIGHT', max_digits=20, decimal_places=2)
    goodsUnit = models.CharField(db_column='GOODS_UNIT', max_length=200)
    barcode = models.CharField(db_column='BARCODE', max_length=50)
    isbn = models.CharField(db_column='ISBN', max_length=50)
    productDate = models.DateTimeField(db_column='PRODUCT_DATE')
    goodsDesc = models.CharField(db_column='GOODS_DESC', max_length=200)
    createTime = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=32)
    updateTime = models.DateTimeField(db_column='UPDATE_TIME', null=False, auto_now_add=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=32)
    yn = models.BooleanField(db_column='YN', null=False, default=0)

    class Meta:
        db_table = 'T_GOODS'