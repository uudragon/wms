from rest_framework import serializers
from big_house.models import Product, ProductDetails, Warehouse, StorageRecord, Receipt, ReceiptDetails, \
    WarehouseDetails, Goods

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


class WarehouseDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WarehouseDetails


class GoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods