import logging
from django.db import transaction

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from big_house.models import Goods, Product, ProductDetails
from big_house.serializers import GoodsSerializer, ProductDetailsSerializer, ProductSerializer
from commons.exceptions import ValueIsNoneException

LOG = logging.getLogger(__name__)


@api_view(['POST'])
def define_goods(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    if message.get('goods_name') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'goods_name\'] can not be none.'})
    if message.get('goods_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'goods_code\'] can not be none.'})
    if message.get('creator') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'creator\'] can not be none.'})
    if message.get('updater') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'updater\'] can not be none.'})

    try:
        goods = Goods(
            goodsCode=message.get('goods_code'),
            goodsType=message.get('goods_type'),
            goodsName=message.get('goods_name'),
            goodsPrice=message.get('goods_price'),
            goodsUnit=message.get('goods_unit'),
            barcode=message.get('barcode'),
            isbn=message.get('isbn'),
            productDate=message.get('product_date'),
            yn=message.get('yn'),
            createTime=message.get('create_time'),
            updateTime=message.get('update_time'),
            creator=message.get('creator'),
            updater=message.get('updater'),
            goodsDesc=message.get('goods_desc'),
            )
        goods.save()
    except Exception as e:
        LOG.error('Goods Information saved error.\n [ERROR]:%s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Goods Information saved error.'})

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@transaction.commit_manually
def define_product(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    if message.get('product_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'product_code\'] can not be none.'})
    product_code = message.get('product_code')
    details = message.get('details')
    if details is None or len(details) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'details\'] must be a non-empty array.'})

    try:
        for detail in details:
            if detail.get('goods_code') is None:
                raise ValueIsNoneException('The goods code can not be none.')
            product_detail = ProductDetails(
                goods_code=detail.get('goods_code'),
                product_code=product_code,
                goods_qty=detail.get('qty'),
                is_gift=detail.get('is_gift'),
            )
            product_detail.save()
        product = Product(
            product_name=message.get('product_name'),
            product_code=message.get('product_code'),
            product_desc=message.get('product_desc'),
            creator=message.get('creator'),
            create_time=message.get('create_time'),
            updater=message.get('updater'),
            update_time=message.get('update_time'),
            yn=message.get('yn'),
        )
        product.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Product Information saved error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Product Information saved error.'})

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def query_goods(request, goods_code):
    code = goods_code

    LOG.debug('Current received goods_code is %s' % code)

    try:
        goods = Goods.objects.get(goodsCode=code)
        LOG.debug('Query goods information is %s' % goods)
        goodsSeria = GoodsSerializer(goods)
        message = JSONRenderer().render(goodsSeria.data)
    except Exception as e:
        LOG.error('Query goods information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query goods [%s] information error' % code},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset-utf-8')


@api_view(['GET'])
def query_product(request, product_code):
    code = product_code

    LOG.debug('Current received product_code is %s' % code)

    try:
        details = ProductDetails.objects.filter(product_code=code)

        details_array = []
        renderer = JSONRenderer()
        for detail in details:
            detailSeria = ProductDetailsSerializer(detail)
            details_array.append(renderer.render(detailSeria.data))
        product = Product.objects.get(product_code=code)
        productSeria = ProductSerializer(product)
        message = renderer.render(productSeria.data)
        message['details'] = details_array
    except Exception as e:
        LOG.error('Query product information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query product [%s] information error' % code},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset-utf-8')