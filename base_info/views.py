from datetime import datetime
import logging
from django.core.paginator import Paginator
from django.db import transaction

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from big_house.models import Goods, Product, ProductDetails, Warehouse, ProductPackage, ProductPackageDetails, \
    GoodsGroup
from big_house.serializers import GoodsSerializer, ProductDetailsSerializer, ProductSerializer, WarehouseSerializer, \
    ProductPackageDetailsSerializer, ProductPackageSerializer, GoodsGroupSerializer
from commons.exceptions import ValueIsNoneException
from uudragon_wms.local.settings import DEFAULT_PAGE_SIZE, YN_YES

LOG = logging.getLogger(__name__)


@api_view(['POST'])
def define_goods(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    if message.get('goods_name') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'goods_name\'] can not be none.'})
    if message.get('goods_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'goods_code\'] can not be none.'})
    if message.get('creator') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'creator\'] can not be none.'})
    if message.get('updater') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'updater\'] can not be none.'})

    try:
        queryCount = Goods.objects.filter(goods_code=message.get('goods_code')).count()
        if queryCount == 0:
            """
                if query result is none
                    this is a new record. Create it to db.
                else
                    Update it exclude goods_code.
            """
            nowTime = datetime.now()
            goods = Goods(
                goods_code=message.get('goods_code'),
                goods_type=message.get('goods_type'),
                goods_name=message.get('goods_name'),
                goods_price=message.get('goods_price'),
                goods_group=message.get('goods_group'),
                goods_unit=message.get('goods_unit'),
                barcode=message.get('barcode'),
                isbn=message.get('isbn'),
                product_date=message.get('product_date'),
                yn=message.get('yn'),
                create_time=nowTime,
                update_time=nowTime,
                creator=message.get('creator'),
                updater=message.get('updater'),
                goods_desc=message.get('goods_desc'),
            )
        else:
            goods = Goods.objects.get(goods_code=message.get('goods_code'))
            goods.goods_type = message.get('goods_type')
            goods.goods_name = message.get('goods_name')
            goods.goods_price = message.get('goods_price')
            goods.goods_group = message.get('goods_group')
            goods.goods_unit = message.get('goods_unit')
            goods.barcode = message.get('barcode')
            goods.isbn = message.get('isbn')
            goods.product_date = message.get('product_date')
            goods.yn = message.get('yn')
            goods.update_time = datetime.now()
            goods.updater = message.get('updater')
            goods.goods_desc = message.get('goods_desc')
        goods.save()
    except Exception as e:
        LOG.error('Goods Information saved error.\n [ERROR]:%s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Goods Information saved error.'})

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@transaction.commit_manually
def define_product(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    if message.get('product_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'product_code\'] can not be none.'})
    product_code = message.get('product_code')
    details = message.get('details')
    if details is None or len(details) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'details\'] must be a non-empty array.'})

    try:
        querycount = Product.objects.filter(product_code=product_code).count()
        if querycount > 0:
            ProductDetails.objects.filter(product_code=product_code).delete()
            product = Product.objects.get(product_code=product_code)
            product.product_name = message.get('product_name')
            product.product_code = message.get('product_code')
            product.product_desc = message.get('product_desc')
            product.product_level = message.get('product_level')
            product.updater = message.get('updater')
            product.update_time = datetime.now()
            product.yn = message.get('yn')
        else:
            nowTime = datetime.now()
            product = Product(
                product_name=message.get('product_name'),
                product_code=message.get('product_code'),
                product_level=message.get('product_level'),
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
                id='%s%s' % (product_code, detail.get('goods_code')),
                goods_code=detail.get('goods_code'),
                product_code=product_code,
                goods_name=detail.get('goods_name'),
                qty=detail.get('qty'),
                is_gift=detail.get('is_gift'),
            )
            product_detail.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Product Information saved error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Product Information saved error.'})

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def query_goods(request, goods_code):
    code = goods_code

    LOG.debug('Current received goods_code is %s' % code)

    try:
        goods = Goods.objects.get(goods_code=code)
        LOG.debug('Query goods information is %s' % goods)
        goodsSeria = GoodsSerializer(goods)
        message = goodsSeria.data
    except Exception as e:
        LOG.error('Query goods information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query goods [%s] information error' % code},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset=utf-8')


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
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset=utf-8')


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
            seria_data = goods_seria.data
            resp_array.append(seria_data)
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
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


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
        query_list = Product.objects.filter(**message).filter(yn=1)
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
            seria_data = product_seria.data
            resp_array.append(seria_data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query product information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query product information error'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


@api_view(['POST'])
def save_warehouse(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    if message.get('warehouse_name') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'warehouse_name\'] can not be none.'})
    if message.get('warehouse_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'warehouse_code\'] can not be none.'})
    if message.get('creator') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'creator\'] can not be none.'})
    if message.get('updater') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'updater\'] can not be none.'})
    now_time = datetime.now()
    try:
        warehouse = Warehouse.objects.filter(warehouse_code=message.get('warehouse_code')).first()
        if warehouse is None:
            warehouse = Warehouse(
                warehouse_code=message.get('warehouse_code'),
                warehouse_name=message.get('warehouse_name'),
                address=message.get('address'),
                type=message.get('type'),
                create_time=now_time,
                creator=message.get('creator'),
                updater=message.get('updater'),
                update_time=now_time,
                yn=YN_YES
            )
        else:
            warehouse.warehouse_name = message.get('warehouse_name')
            warehouse.address = message.get('address')
            warehouse.type = message.get('type')
            warehouse.updater = message.get('updater')
            warehouse.update_time = now_time
            warehouse.yn = message.get('yn')
        warehouse.save()
    except Exception as e:
        LOG.error('Warehouse saved error.\n [ERROR]:%s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Warehouse saved error.'})
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def query_warehouse(request, warehouse_code):
    code = warehouse_code

    LOG.debug('Current received warehouse_code is %s' % code)

    try:
        warehouse = Warehouse.objects.get(warehouse_code=code)
        warehouse_seria = WarehouseSerializer(warehouse)
        message = warehouse_seria.data
    except Exception as e:
        LOG.error('Query warehouse information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query warehouse [%s] information error' % code},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset=utf-8')


@api_view(['POST'])
def query_warehouse_list(request):
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
        query_list = Warehouse.objects.filter(**message)
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
            warehouse_seria = WarehouseSerializer(item)
            seria_data = warehouse_seria.data
            resp_array.append(seria_data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query warehouses information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query warehouses information error'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


@api_view(['GET'])
def query_packages_all(request):
    resp_array = []
    try:
        query_list = ProductPackage.objects.all()

        for item in query_list:
            package_seria = ProductPackageSerializer(item)
            seria_data = package_seria.data
            resp_array.append(seria_data)
    except Exception as e:
        LOG.error('Query package information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    data={'error': 'Query package information error'},
                    content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_array, content_type='application/json;charset=utf-8')


@api_view(['POST'])
def query_packages(request):
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
        query_list = ProductPackage.objects.filter(**message).filter(yn=1)
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
            package_seria = ProductPackageSerializer(item)
            seria_data = package_seria.data
            resp_array.append(seria_data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query package information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query package information error'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


@api_view(['GET'])
def query_package(request, package_code):
    code = package_code

    LOG.debug('Current received package_code is %s' % code)

    try:
        details = ProductPackageDetails.objects.extra(
            select={'product_name': 't_product.product_name'},
            tables=['t_product'],
            where=['t_product_package_details.product_code=t_product.product_code']
        ).filter(package_code=code)

        details_array = []
        for detail in details:
            detailSeria = ProductPackageDetailsSerializer(detail)
            details_array.append(detailSeria.data)
        package = ProductPackage.objects.get(package_code=code)
        packageSeria = ProductPackageSerializer(package)
        message = packageSeria.data
        message['details'] = details_array
    except Exception as e:
        LOG.error('Query product information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query product [%s] information error' % code},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset=utf-8')
    


@api_view(['POST'])
@transaction.commit_manually
def save_package(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    if message.get('package_code') is None:
        LOG.error('Attribute[\'package_code\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'package_code\'] can not be none.'})
    package_code = message.get('package_code')
    details = message.get('details')
    if details is None or len(details) == 0:
        LOG.error('Attribute[\'details\'] must be a non-empty array.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'details\'] must be a non-empty array.'})

    try:
        package = ProductPackage.objects.filter(package_code=package_code).first()
        if package is not None:
            ProductPackageDetails.objects.filter(package_code=package_code).delete()
            package.package_name = message.get('package_name')
            package.package_code = message.get('package_code')
            package.package_desc = message.get('package_desc')
            package.updater = message.get('updater')
            package.update_time = datetime.now()
            package.yn = message.get('yn')
        else:
            nowTime = datetime.now()
            package = ProductPackage(
                package_name=message.get('package_name'),
                package_code=message.get('package_code'),
                package_desc=message.get('package_desc'),
                creator=message.get('creator'),
                create_time=nowTime,
                updater=message.get('updater'),
                update_time=nowTime,
                yn=message.get('yn'),
            )
        package.save()
        for detail in details:
            if detail.get('product_code') is None:
                raise ValueIsNoneException('The product code can not be none.')
            package_detail = ProductPackageDetails(
                id='%s%s' % (package_code, detail.get('product_code')),
                product_code=detail.get('product_code'),
                package_code=package_code,
                qty=detail.get('qty')
            )
            package_detail.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Package Information saved error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Package Information saved error.'})

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.commit_manually
def goods_group_save(request):
    message = request.DATA

    LOG.debug('Current received message is %s' % message)

    if message.get('group_name') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'group_name\'] can not be none.'})
    if message.get('group_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'group_code\'] can not be none.'})
    if message.get('creator') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'creator\'] can not be none.'})
    if message.get('updater') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'updater\'] can not be none.'})

    try:
        group = GoodsGroup.objects.select_for_update().filter(group_code=message.get('group_code')).first()
        nowTime = datetime.now()
        if group is None:
            group = GoodsGroup(
                group_code=message.get('group_code'),
                group_name=message.get('group_name'),
                group_desc=message.get('group_desc'),
                yn=message.get('yn'),
                create_time=nowTime,
                update_time=nowTime,
                creator=message.get('creator'),
                updater=message.get('updater'),
            )
        else:
            group.group_name = message.get('group_name')
            group.group_desc = message.get('group_desc')
            group.yn = message.get('yn')
            group.update_time = nowTime
            group.updater = message.get('updater')
        group.save()
        transaction.commit()
    except Exception as e:
        LOG.error('GoodsGroup Information saved error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'GoodsGroup Information saved error.'})

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def query_goods_group(request, group_code):
    code = group_code

    LOG.debug('Current received group_code is %s' % code)

    try:
        group = GoodsGroup.objects.filter(group_code=code).first()
        LOG.debug('Query goods information is %s' % group)
        groupSeria = GoodsGroupSerializer(group)
        message = groupSeria.data
    except Exception as e:
        LOG.error('Query goods group information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query goods group [%s] information error' % code},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=message, content_type='application/json;charset=utf-8')


@api_view(['POST'])
def query_goods_group_list(request):
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
        query_list = GoodsGroup.objects.filter(**message).filter(yn=1)
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
            group_seria = GoodsGroupSerializer(item)
            seria_data = group_seria.data
            resp_array.append(seria_data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
        LOG.info('Current response message is %s' % resp_message)
        #resp_data = renderer.render(resp_message)
    except Exception as e:
        LOG.error('Query goods groups information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query goods groups information error'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


@api_view(['GET'])
def query_agency_package(request):
    LOG.info('Current method is [query_agency_package]')

    resp_array = []
    try:
        packages = ProductPackage.objects.filter(package_type=2).values('package_code,package_name')
        for package in packages:
            seria = ProductPackageSerializer(package)
            resp_array.append(seria)
    except Exception as e:
        LOG.error('Query agency packages error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query agency packages error.'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_array, content_type='application/json;charset=utf-8')


@api_view(['GET'])
def query_site_package(request):
    LOG.info('Current method is [query_site_package]')

    resp_array = []
    try:
        packages = ProductPackage.objects.filter(package_type=1).values('package_code,package_name')
        for package in packages:
            seria = ProductPackageSerializer(package)
            resp_array.append(seria)
    except Exception as e:
        LOG.error('Query site packages error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query site packages error.'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_array, content_type='application/json;charset=utf-8')