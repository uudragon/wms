from datetime import datetime
import logging
from django.core.paginator import Paginator
from django.db import transaction

# Create your views here.
import math
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from big_house.models import Goods, Product, ProductDetails
from big_house.serializers import GoodsSerializer, ProductDetailsSerializer, ProductSerializer
from commons.exceptions import ValueIsNoneException
from uudragon_wms.local.settings import DEFAULT_PAGE_SIZE

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
        queryCount = Goods.objects.filter(goodsCode=message.get('goods_code')).count()
        if queryCount == 0:
            """
                if query result is none
                    this is a new record. Create it to db.
                else
                    Update it exclude goods_code.
            """
            nowTime = datetime.now()
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
                createTime=nowTime,
                updateTime=nowTime,
                creator=message.get('creator'),
                updater=message.get('updater'),
                goodsDesc=message.get('goods_desc'),
            )
        else:
            goods = Goods.objects.get(goodsCode=message.get('goods_code'))
            goods.goodsType = message.get('goods_type'),
            goods.goodsName = message.get('goods_name'),
            goods.goodsPrice = message.get('goods_price'),
            goods.goodsUnit = message.get('goods_unit'),
            goods.barcode = message.get('barcode'),
            goods.isbn = message.get('isbn'),
            goods.productDate = message.get('product_date'),
            goods.yn = message.get('yn'),
            goods.updateTime = datetime.now(),
            goods.updater = message.get('updater'),
            goods.goodsDesc = message.get('goods_desc'),
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
        querycount = Product.objects.filter(product_code=product_code).count()
        if querycount != 0:
            ProductDetails.objects.filter(product_code=product_code).delete()
            product = Product.objects.get(product_code=product_code)
            product.product_name = message.get('product_name'),
            product.product_code = message.get('product_code'),
            product.product_desc = message.get('product_desc'),
            product.updater = message.get('updater'),
            product.update_time = datetime.now(),
            product.yn = message.get('yn'),
        else:
            nowTime = datetime.now()
            product = Product(
                product_name=message.get('product_name'),
                product_code=message.get('product_code'),
                product_desc=message.get('product_desc'),
                creator=message.get('creator'),
                create_time=nowTime,
                updater=message.get('updater'),
                update_time=nowTime,
                yn=message.get('yn'),
            )
        product.save()
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
        message = goodsSeria.data
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
        for detail in details:
            detailSeria = ProductDetailsSerializer(detail)
            details_array.append(detailSeria.data)
        product = Product.objects.get(product_code=code)
        productSeria = ProductSerializer(product)
        message = productSeria.data
        message['details'] = details_array
    except Exception as e:
        LOG.error('Query product information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query product [%s] information error' % code},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset-utf-8')


@api_view(['POST'])
def query_goods_list(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)
    
    pageSize = message.pop('pageSize')
    if pageSize is None or pageSize == 0:
        pageSize = DEFAULT_PAGE_SIZE
    pageNo = message.pop('pageNo')
    if pageNo is None or pageNo == 0:
        pageNo = 1
    
    resp_message = dict()
    try:
        for key in message.iterkeys():
            key += '__contains'
            LOG.debug('Condition of query is %s' % message)
        query_list = Goods.objects.filter(**message)
        paginator = Paginator(query_list, pageSize, orphans=0, allow_empty_first_page=True)
        total_page_count = paginator.num_pages
        if pageNo > total_page_count:
            pageNo = total_page_count
        elif pageNo < 1:
            pageNo = 1
        cur_page = paginator.page(pageNo)
        page_records = cur_page.object_list
        resp_array = []
        for item in page_records:
            goods_seria = GoodsSerializer(item)
            #goods_json = renderer.render(goods_seria.data)
            resp_array.append(goods_seria.data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
        LOG.info('Current response message is %s' % resp_message)
        #resp_data = renderer.render(resp_message)
    except Exception as e:
        LOG.error('Query goods information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query goods information error'},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset-utf-8')


@api_view(['POST'])
def query_product_list(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    pageSize = message.pop('pageSize')
    if pageSize is None or pageSize == 0:
        pageSize = DEFAULT_PAGE_SIZE
    pageNo = message.pop('pageNo')
    if pageNo is None or pageNo == 0:
        pageNo = 1

    resp_message = dict()
    try:
        for key in message.iterkeys():
            key += '__contains'
            LOG.debug('Condition of query is %s' % message)
        query_list = Product.objects.filter(**message)
        paginator = Paginator(query_list, pageSize, orphans=0, allow_empty_first_page=True)
        total_page_count = paginator.num_pages
        if pageNo > total_page_count:
            pageNo = total_page_count
        elif pageNo < 1:
            pageNo = 1
        cur_page = paginator.page(pageNo)
        page_records = cur_page.object_list
        resp_array = []
        for item in page_records:
            product_seria = ProductSerializer(item)
            resp_array.append(product_seria.data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query product information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query product information error'},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset-utf-8')
