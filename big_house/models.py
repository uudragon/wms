from django.db import models

# Create your models here.


class Contact(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=72)
    name = models.CharField(db_column='name', null=False, max_length=255)
    prov = models.CharField(db_column='prov', null=False, max_length=64)
    city = models.CharField(db_column='city', null=False, max_length=64)
    address = models.CharField(db_column='address', null=False, max_length=255)
    post = models.CharField(db_column='post', null=False, max_length=20)
    tel = models.CharField(db_column='tel', null=False, max_length=20)

    class Meta:
        db_table = 'T_CONTACT'


class GoodsGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    group_code = models.CharField(db_column='GROUP_CODE', null=False, max_length=36, unique=True)
    group_name = models.CharField(db_column='GROUP_NAME', null=False, max_length=255, unique=True)
    group_desc = models.CharField(db_column='GROUP_DESC', null=True, max_length=255)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)
    
    class Meta:
        db_table = 'T_GOODS_GROUP'


class ProductPackage(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    package_code = models.CharField(db_column='PACKAGE_CODE', null=False, max_length=36, unique=True)
    package_name = models.CharField(db_column='PACKAGE_NAME', null=False, max_length=100)
    package_desc = models.CharField(db_column='PACKAGE_DESC', null=False, max_length=255)
    package_price = models.DecimalField(db_column='PACKAGE_PRICE', null=False, default=0.00,
                                        decimal_places=2, max_digits=20)
    package_type = models.IntegerField(db_column='PACKAGE_TYPE', null=False, max_length=4, default=1)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)
    
    class Meta:
        db_table = 'T_PRODUCT_PACKAGE'
        
        
class ProductPackageDetails(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=72)
    package_code = models.CharField(db_column='PACKAGE_CODE', null=False, max_length=36)
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=36)
    qty = models.IntegerField(db_column='QTY', null=False, max_length=11, default=1)
    
    class Meta:
        db_table = 'T_PRODUCT_PACKAGE_DETAILS'


class ProductPackageGifts(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=72)
    package_code = models.CharField(db_column='PACKAGE_CODE', null=False, max_length=36)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=36)
    qty = models.IntegerField(db_column='QTY', null=False, max_length=11, default=1)

    class Meta:
        db_table = 'T_PRODUCT_PACKAGE_GIFTS'


class Product(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=36, unique=True)
    product_name = models.CharField(db_column='PRODUCT_NAME', null=False, max_length=200)
    product_level = models.IntegerField(db_column='PRODUCT_LEVEL', null=False, default=1)
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
    product_code = models.CharField(db_column='PRODUCT_CODE', null=False, max_length=36)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=36)
    qty = models.IntegerField(db_column='GOODS_QTY', null=False, default=1)
    is_gift = models.SmallIntegerField(db_column='IS_GIFT', null=False, default=0)

    class Meta:
        db_table = 'T_PRODUCT_DETAILS'


class Warehouse(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    warehouse_code = models.CharField(db_column='CODE', null=False, max_length=99, unique=True)
    warehouse_name = models.CharField(db_column='NAME', null=False, max_length=255, unique=True)
    address = models.CharField(db_column='ADDRESS', null=False, max_length=255)
    type = models.SmallIntegerField(db_column='TYPE', null=False, default=1)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', max_length=4, default=0)

    class Meta:
        db_table = 'T_WAREHOUSE'


class StorageRecords(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=36)
    goods_qty = models.IntegerField(db_column='GOODS_QTY', null=False, default=1)
    code = models.CharField(db_column='CODE', null=False, max_length=50)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, max_length=99)
    type = models.SmallIntegerField(db_column='TYPE', null=False, default=1)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    status = models.IntegerField(db_column='STATUS', null=False, max_length=4, default=1)

    class Meta:
        db_table = 'T_STORAGE_RECORD'


class Receipt(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    receipt_code = models.CharField(db_column='CODE', null=False, max_length=36, unique=True)
    receipt_date = models.DateTimeField(db_column='RECEIPT_DATE', null=False)
    receipt_desc = models.CharField(db_column='RECEIPT_DESC', null=True, max_length=255)
    status = models.SmallIntegerField(db_column='STATUS', null=True, default=0)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, max_length=32)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_RECEIPT'


class ReceiptDetails(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, null=False, max_length=100)
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=36)
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
    goods_code = models.CharField(db_column='GOODS_CODE', null=False, max_length=36)
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
    qty = models.IntegerField(db_column='EFFECTIVE_QTY', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', auto_now=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)

    class Meta:
        db_table = 'T_W_PRODUCT_DETAILS'


class Goods(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goods_type = models.IntegerField(db_column='GOODS_TYPE', max_length=4, null=False, default=1)
    goods_code = models.CharField(db_column='GOODS_CODE', max_length=36, null=False)
    goods_name = models.CharField(db_column='GOODS_NAME', max_length=200, null=False)
    goods_group = models.CharField(db_column='GOODS_GROUP', max_length=36, null=False)
    goods_price = models.DecimalField(db_column='GOODS_PRICE', max_digits=10, decimal_places=2)
    goods_bulk = models.DecimalField(db_column='GOODS_BULK', max_digits=20, decimal_places=2, default=0.00)
    goods_weight = models.DecimalField(db_column='GOODS_WEIGHT', max_digits=20, decimal_places=2, default=0.00)
    goods_unit = models.CharField(db_column='GOODS_UNIT', max_length=200)
    barcode = models.CharField(db_column='BARCODE', max_length=50)
    isbn = models.CharField(db_column='ISBN', max_length=50)
    product_date = models.DateField(db_column='PRODUCT_DATE')
    goods_desc = models.CharField(db_column='GOODS_DESC', max_length=200)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', null=False, auto_now_add=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    yn = models.SmallIntegerField(db_column='YN', null=False, default=1, max_length=1)

    class Meta:
        db_table = 'T_GOODS'


class Shipment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    orders_no = models.CharField(db_column='ORDERS_NO', null=False, max_length=36)
    shipment_no = models.CharField(db_column='SHIPMENT_NO', null=False, unique=True, max_length=36)
    picking_no = models.CharField(db_column='PICKING_NO', null=True, max_length=36)
    source = models.IntegerField(db_column='SOURCE', null=False, max_length=4, default=1)
    agent_code = models.CharField(db_column='AGENT_CODE', null=True, max_length=50)
    warehouse = models.CharField(db_column='WAREHOUSE', null=False, unique=True, max_length=36)
    customer_no = models.CharField(db_column='CUSTOMER_NO', null=False, max_length=36)
    customer_name = models.CharField(db_column='CUSTOMER_NAME', null=False, max_length=100)
    prov = models.CharField(db_column='PROVINCE', null=True, max_length=255)
    city = models.CharField(db_column='CITY', null=True, max_length=255)
    district = models.CharField(db_column='DISTRICT', null=True, max_length=50)
    customer_phone = models.CharField(db_column='CUSTOMER_PHONE', null=True, max_length=20)
    post = models.CharField(db_column='POST', null=True, max_length=20)
    address = models.CharField(db_column='ADDRESS', null=False, max_length=255)
    customer_tel = models.CharField(db_column='CUSTOMER_TEL', null=False, max_length=50)
    has_invoice = models.IntegerField(db_column='HAS_INVOICE', null=False, default=0)
    amount = models.DecimalField(db_column='AMOUNT', null=False, default=0.00, max_digits=20, decimal_places=2)
    shipped_qty = models.IntegerField(db_column='SHIPPED_QTY', null=False, default=0)
    express_code = models.CharField(db_column='EXPRESS_CODE', null=True, max_length=50)
    express_orders_no = models.CharField(db_column='EXPRESS_ORDERS_NO', null=True, max_length=100, unique=True)
    express_name = models.CharField(db_column='EXPRESS_NAME', null=True, max_length=255)
    express_cost = models.DecimalField(db_column='EXPRESS_COST', null=True, max_digits=20,
                                       decimal_places=2, default=0.00)
    big_pen = models.CharField(db_column='BIG_PEN', null=True, max_length=100)
    sent_date = models.DateField(db_column='SENT_DATE', null=True)
    courier = models.CharField(db_column='COURIER', null=True, max_length=100)
    courier_tel = models.CharField(db_column='COURIER_TEL', null=True, max_length=32)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', null=False, auto_now_add=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    status = models.IntegerField(db_column='STATUS', null=False, default=0)

    class Meta:
        db_table = 'T_SHIPMENT'


class ShipmentDetails(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=72)
    shipment_no = models.CharField(db_column='SHIPMENT_NO', null=False, max_length=36)
    code = models.CharField(db_column='CODE', null=False, max_length=36)
    is_product = models.IntegerField(db_column='IS_PRODUCT', null=False, max_length=4, default=1)
    is_gift = models.IntegerField(db_column='IS_GIFT', null=False, max_length=4, default=0)
    qty = models.IntegerField(db_column='QTY', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', null=False, auto_now_add=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    status = models.IntegerField(db_column='STATUS', null=False, default=0)

    class Meta:
        db_table = 'T_SHIPMENT_DETAILS'


class PickingOrders(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    picking_no = models.CharField(db_column='PICKING_NO', null=False, unique=True, max_length=36)
    picking_qty = models.IntegerField(db_column='PICKING_QTY', null=False, default=0)
    status = models.IntegerField(db_column='STATUS', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', null=False, auto_now_add=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    
    class Meta:
        db_table = 'T_PICKING_ORDERS'


class PickingOrdersDetails(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=72)
    picking_no = models.CharField(db_column='PICKING_NO', null=False, max_length=36)
    code = models.CharField(db_column='CODE', null=False, max_length=36)
    is_product = models.IntegerField(db_column='IS_PRODUCT', null=False, max_length=4, default=1)
    is_gift = models.IntegerField(db_column='IS_GIFT', null=False, max_length=4, default=0)
    qty = models.IntegerField(db_column='QTY', null=False, default=0)
    create_time = models.DateTimeField(db_column='CREATE_TIME', null=False, auto_now_add=True)
    creator = models.CharField(db_column='CREATOR', null=False, max_length=50)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', null=False, auto_now_add=True)
    updater = models.CharField(db_column='UPDATER', null=False, max_length=50)
    
    class Meta:
        db_table = 'T_PICKING_ORDERS_DETAILS'