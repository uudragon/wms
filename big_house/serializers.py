from rest_framework import serializers
from big_house.models import Product, ProductDetails, Warehouse, StorageRecord, Receipt, ReceiptDetails, \
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


class StorageRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = StorageRecord


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt


class ReceiptDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptDetails


class WarehouseGoodsDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseGoodsDetails


class WarehouseProductDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WarehouseProductDetails


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods