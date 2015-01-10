from rest_framework import serializers
from big_house.models import Product, ProductDetails, Warehouse, StorageRecords, Receipt, ReceiptDetails, \
    WarehouseGoodsDetails, WarehouseProductDetails, Goods

__author__ = 'pluto'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product


class ProductDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDetails


class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Warehouse


class StorageRecordsSerializer(serializers.ModelSerializer):

    warehouse_name = serializers.CharField(max_length=255)
    goods_name = serializers.CharField(max_length=255)

    class Meta:
        model = StorageRecords


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt


class ReceiptDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptDetails


class WarehouseGoodsDetailsSerializer(serializers.ModelSerializer):
    
    warehouse_name = serializers.CharField(max_length=255)
    goods_name = serializers.CharField(max_length=255)

    class Meta:
        model = WarehouseGoodsDetails


class WarehouseProductDetailsSerializer(serializers.ModelSerializer):

    warehouse_name = serializers.CharField(max_length=255)
    product_name = serializers.CharField(max_length=255)
    
    class Meta:
        model = WarehouseProductDetails


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods