from rest_framework import serializers
from big_house.models import Product, ProductDetails, Warehouse, StorageRecords, Receipt, ReceiptDetails, \
    WarehouseGoodsDetails, WarehouseProductDetails, Goods, Shipment, ShipmentDetails, ProductPackage, \
    ProductPackageDetails, GoodsGroup, ProductPackageGifts

__author__ = 'pluto'


class ProductPackageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductPackage


class ProductPackageDetailsSerializer(serializers.ModelSerializer):
    
    product_name = serializers.CharField(max_length=100)

    class Meta:
        model = ProductPackageDetails


class ProductPackageGiftsSerializer(serializers.ModelChoiceIterator):
    
    goods_name = serializers.CharField(max_length=255)
    
    class Meta:
        model = ProductPackageGifts


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
    
    warehouse_name = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Receipt


class ReceiptDetailsSerializer(serializers.ModelSerializer):

    goods_name = serializers.CharField(max_length=255, read_only=True)

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


class GoodsGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GoodsGroup


class ShipmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Shipment


class ShipmentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShipmentDetails