# Create your views here.
from datetime import datetime
import logging
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from big_house.models import StorageRecords, WarehouseGoodsDetails, WarehouseProductDetails, Warehouse, ProductDetails
from big_house.serializers import StorageRecordsSerializer, WarehouseGoodsDetailsSerializer, \
    WarehouseProductDetailsSerializer
from uudragon_wms.local.settings import DEFAULT_PAGE_SIZE


LOG = logging.getLogger(__name__)


@api_view(['POST'])
@transaction.commit_manually
def picking_statistic(request, warehouse_code):
    message = request.DATA
    LOG.info('Current warehouse_code is %s, received message is %s' % (warehouse_code, message))

    product_code = message.get('product_code')
    if product_code is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'product_code\'] can not be none.'})
    try:
        product_detail = ProductDetails.objects.filter(product_code=product_code)
        resp_message = {'picking_qty': 0}
        if product_detail is not None and len(product_detail) > 0:
            goods_dict = dict()
            goods_codes = []
            for item in product_detail:
                goods_dict[item.goods_code] = item.qty
                goods_codes.append(item.goods_code)
            goods_list = WarehouseGoodsDetails.objects.filter(goods_code__in=goods_codes).filter(
                warehouse=warehouse_code).select_for_update()
            LOG.debug('WarehouseGoodsDetails list is %s' % goods_list)
            qtys = []
            for goods in goods_list:
                if goods.goods_code in goods_dict:
                    picking_qty = (goods.not_picking_qty / goods_dict.get(goods.goods_code)) \
                        if (goods_dict.get(goods.goods_code) is not None
                            and goods_dict.get(goods.goods_code) != 0) else 0
                    qtys.append(picking_qty)
                else:
                    qtys.append(0)

            LOG.debug('Current picking qty list is %s' % qtys)

            if len(qtys) > 1:
                picking_qty = min(*qtys)
            elif len(qtys) == 0:
                picking_qty = 0
            else:
                picking_qty = qtys[0]

            LOG.debug('Current count of product can be picked is %s' % picking_qty)
        transaction.commit()
        resp_message['picking_qty'] = picking_qty
    except Exception as e:
        LOG.error('Picking operation error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Picking operation error. reason:%s' % str(e)})
    return Response(status=status.HTTP_200_OK, data=resp_message)


@api_view(['POST'])
@transaction.commit_manually
def picking(request, warehouse_code):
    message = request.DATA
    LOG.info('Current warehouse_code is %s, received message is %s' % (warehouse_code, message))

    product_code = message.get('product_code')
    if product_code is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'product_code\'] can not be none.'})
    try:
        product_detail = ProductDetails.objects.filter(product_code=product_code)
        resp_message = {'picking_qty': 0}
        if product_detail is not None and len(product_detail) > 0:
            goods_dict = dict()
            goods_codes = []
            for item in product_detail:
                goods_dict[item.goods_code] = item.qty
                goods_codes.append(item.goods_code)
            goods_list = WarehouseGoodsDetails.objects.filter(goods_code__in=goods_codes).filter(
                warehouse=warehouse_code).select_for_update()
            LOG.debug('WarehouseGoodsDetails list is %s' % goods_list)
            qtys = []
            for goods in goods_list:
                if goods.goods_code in goods_dict:
                    picking_qty = (goods.not_picking_qty / goods_dict.get(goods.goods_code)) \
                        if (goods_dict.get(goods.goods_code) is not None
                            and goods_dict.get(goods.goods_code) != 0) else 0
                    qtys.append(picking_qty)
                else:
                    qtys.append(0)
            
            LOG.debug('Current picking qty list is %s' % qtys)

            if len(qtys) > 1:
                picking_qty = min(*qtys)
            elif len(qtys) == 0:
                picking_qty = 0
            else:
                picking_qty = qtys[0]

            picking_count = message.get('picking_count')
            if picking_count > picking_qty:
                raise Exception('The picking_count is error, valid is %s, but now is %s' % (picking_qty, picking_count))
                
            LOG.debug('Current count of product can be picked is %s' % picking_qty)
                
            if picking_count != 0:
                now_time = datetime.now()
                for goods in goods_list:
                    goods.not_picking_qty -= picking_count * goods_dict.get(goods.goods_code)
                    goods.picking_qty += goods.picking_qty + picking_count * goods_dict.get(goods.goods_code)
                    goods.updater = message.get('updater')
                    goods.update_time = now_time
                    goods.save()
                product_detail = WarehouseProductDetails.objects.filter(
                    product_code=product_code).select_for_update().first()
                if product_detail is not None:
                    product_detail.qty += picking_qty
                    product_detail.updater = message.get('updater')
                    product_detail.update_time = now_time
                else:
                    product_detail = WarehouseProductDetails(product_code=product_code, 
                                        warehouse=warehouse_code,
                                        qty=picking_count,
                                        create_time=now_time,
                                        creator=message.get('updater'),
                                        update_time=now_time,
                                        updater=message.get('updater'))
                product_detail.save()
            transaction.commit()
            resp_message['picking_qty'] = picking_qty
    except Exception as e:
        LOG.error('Picking operation error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Picking operation error. reason:%s' % str(e)})
    return Response(status=status.HTTP_200_OK, data=resp_message)


@api_view(['POST'])
def query_records(request, warehouse_code):
    warehouse = warehouse_code
    
    message = request.DATA
    
    LOG.info('Current query warehouse is %s, received message is %s' % (warehouse, message))

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
        query_list = StorageRecords.objects.extra(
            select={'warehouse_name': 't_warehouse.name', 'goods_name': 't_goods.goods_name'}, 
            tables=['t_warehouse', 't_goods'], 
            where=['t_storage_record.warehouse=t_warehouse.code', 
                   't_storage_record.goods_code=t_goods.goods_code']).filter(**message).filter(warehouse=warehouse)
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
            record_seria = StorageRecordsSerializer(item)
            resp_array.append(record_seria.data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query storage records information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query storage records information error'},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset-utf-8')


@api_view(['POST'])
def query_goods(request, warehouse_code):
    warehouse = warehouse_code

    message = request.DATA

    LOG.info('Current query warehouse is %s, received message is %s' % (warehouse, message))

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
        query_list = WarehouseGoodsDetails.objects.extra(
            select={'warehouse_name': 't_warehouse.name', 'goods_name': 't_goods.goods_name'},
            tables=['t_warehouse', 't_goods'],
            where=['t_w_goods_details.warehouse=t_warehouse.code',
                   't_w_goods_details.goods_code=t_goods.goods_code']).filter(**message).filter(warehouse=warehouse)
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
            record_seria = WarehouseGoodsDetailsSerializer(item)
            resp_array.append(record_seria.data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query inner goods information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query inner goods information error'},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset-utf-8')
    


@api_view(['POST'])
def query_products(request, warehouse_code):
    warehouse = warehouse_code

    message = request.DATA

    LOG.info('Current query warehouse is %s, received message is %s' % (warehouse, message))

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
        query_list = WarehouseProductDetails.objects.extra(
            select={'warehouse_name': 't_warehouse.name', 'product_name': 't_product.product_name'},
            tables=['t_warehouse', 't_product'],
            where=['t_w_product_details.warehouse=t_warehouse.code',
                   't_w_product_details.product_code=t_product.product_code']).filter(**message).filter(
            warehouse=warehouse)
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
            record_seria = WarehouseProductDetailsSerializer(item)
            resp_array.append(record_seria.data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query inner products information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query inner products information error'},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset-utf-8')