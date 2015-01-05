from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=32, unique=True)
    product_name = models.CharField(db_column='PRODUCT_NAME', null=False, max_length=200)
    product_desc = models.CharField(db_column='PRODUCT_DESC', null=True, max_length=500)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)

    class Meta:
        db_table = 'T_PRODUCT'


class ProductDetails(models.Model):
    id = models.CharField(db_column='id', primary_key=True, max_length=72)
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=32)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=32)
    goods_name = models.CharField(db_column='GOODS_NAME', max_length=200, null=False)
    qty = models.IntegerField(db_column='GOODS_QTY', null=False, default=1)
    is_gift = models.SmallIntegerField(db_column='IS_GIFT', null=False, default=0)

    class Meta:
        db_table = 'T_PRODUCT_DETAILS'


class Warehouse(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    code = models.CharField(db_column='CODE', null=False, max_length=99, unique=True)
    name = models.CharField(db_column='NAME', null=False, max_length=255, unique=True)
    address = models.CharField(db_column='ADDRESS', null=False, max_length=255)
    type = models.SmallIntegerField(db_column='TYPE', null=False, default=1)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
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
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_STORAGE_RECORD'


class Receipt(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    receipt_code = models.CharField(db_column='CODE', null=False, max_length=50, unique=True)
    receipt_date = models.DateTimeField(db_column='RECEIPT_DATE', null=False)
    receipt_desc = models.CharField(db_column='RECEIPT_DESC', null=True, max_length=255)
    receipt_stat = models.SmallIntegerField(db_column='RECEIPT_STAT', null=True, default=0)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, max_length=32)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)

    class Meta:
        db_table = 'T_RECEIPT'


class ReceiptDetails(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, null=False, max_length=100)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=32)
    qty = models.IntegerField(db_column='GOODS_QTY', null=False, default=0)
    actual_qty = models.IntegerField(db_column='ACTUAL_QTY', null=False, default=0)
    receipt_code = models.CharField(db_column='CODE', null=False, max_length=50)
    status = models.SmallIntegerField(db_column='STATUS', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_RECEIPT_DETAILS'


class WarehouseGoodsDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, max_length=50)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=32)
    qty = models.IntegerField(db_column='QTY', null=False, default=0)
    picking_qty = models.IntegerField(db_column='PICKING_QTY', null=False, default=0)
    not_picking_qty = models.IntegerField(db_column='NOT_PICKING_QTY', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_W_GOODS_DETAILS'


class WarehouseProductDetails(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, max_length=50)
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=50)
    effective_qty = models.IntegerField(db_column='EFFECTIVE_QTY', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_W_PRODUCT_DETAILS'


class Goods(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goods_type = models.IntegerField(db_column='GOODS_TYPE', max_length=4, null=False, default=1)
    goods_code = models.CharField(db_column='GOODS_CODE', max_length=32, null=False)
    goods_name = models.CharField(db_column='GOODS_NAME', max_length=200, null=False)
    goods_price = models.DecimalField(db_column='GOODS_PRICE', max_digits=10, decimal_places=2)
    goods_bulk = models.DecimalField(db_column='GOODS_BULK', max_digits=20, decimal_places=2, default=0.00)
    goods_weight = models.DecimalField(db_column='GOODS_WEIGHT', max_digits=20, decimal_places=2, default=0.00)
    goods_unit = models.CharField(db_column='GOODS_UNIT', max_length=200)
    barcode = models.CharField(db_column='BARCODE', max_length=50)
    isbn = models.CharField(db_column='ISBN', max_length=50)
    product_date = models.DateField(db_column='PRODUCT_DATE')
    goods_desc = models.CharField(db_column='GOODS_DESC', max_length=200)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=32)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', null=False, auto_now_add=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=32)
    yn = models.SmallIntegerField(db_column='YN', null=False, default=1, max_length=1)

    class Meta:
        db_table = 'T_GOODS'