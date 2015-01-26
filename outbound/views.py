# Create your views here.
from datetime import datetime
import logging
import uuid
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time
from big_house.models import ProductDetails, ShipmentDetails, Shipment, ProductPackageDetails
from big_house.serializers import ShipmentDetailsSerializer, ShipmentSerializer
from uudragon_wms.local.settings import DEFAULT_PAGE_SIZE


LOG = logging.getLogger(__name__)


@api_view(['POST'])
@transaction.commit_manually
def save_shipment(request):
    message = request.DATA
    
    LOG.info('Current received message is %s.' % message)
    
    try:
        shipment = Shipment.objects.filter(shipment_no=message.get('shipment_no')).first()
        if shipment is not None:
            detail_dict = dict()
            shipment_details = ShipmentDetails.objects.filter(shipment_no=message.get('shipment_no'))
            now_time = datetime.now()
            for shipment_detail in shipment_details:
                detail_dict[shipment_detail.get('goods_code')] = shipment_detail
            rece_details = message.get('details')
            for rece_detail in rece_details:
                if rece_detail.get('goods_code') in detail_dict:
                    shipment_detail = detail_dict.get(rece_detail.get('goods_code'))
                    shipment_detail.is_gift = rece_detail.get('is_gift')
                    shipment_detail.qty = rece_detail.get('qty')
                    shipment_detail.status = rece_detail.get('status')
                    shipment_detail.updater = message.get('updater')
                    shipment_detail.update_time = now_time
                else:
                    shipment_detail = ShipmentDetails(
                        id='%s%s' % (rece_detail.get('shipment_no'), rece_detail.get('goods_code')),
                        shipment_no=rece_detail.get('shipment_no'),
                        goods_code=rece_detail.get('goods_code'),
                        is_gift=rece_detail.get('is_gift'),
                        qty=rece_detail.get('qty'),
                        status=rece_detail.get('status'),
                        creator=message.get('updater'),
                        updater=message.get('updater'),
                        create_time=now_time,
                        update_time=now_time
                    )
                shipment_detail.save()
            shipment.express_code = message.get('express_code')
            shipment.express_orders_no = message.get('express_orders_no')
            shipment.express_name = message.get('express_name')
            shipment.express_cost = message.get('express_cost')
            shipment.sent_date = message.get('sent_date')
            shipment.courier = message.get('courier')
            shipment.courier_tel = message.get('courier_tel')
            shipment.updater = message.get('updater')
            shipment.update_time = now_time
            shipment.save()
            transaction.commit()
    except Exception as e:
        LOG.error('Save shipment information error. [ERROR] %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Save shipment information error'},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def query_shipments(request):
    message = request.DATA

    LOG.info('Current received message is %s' % message)

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
        query_list = Shipment.objects.filter(**message).order_by()
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
            record_seria = ShipmentSerializer(item)
            resp_array.append(record_seria.data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query shipment information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query shipment information error'},
                        content_type='application/json;charset-utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset-utf-8')


@api_view(['GET'])
def query_shipment(request, shipment_no):
    shipment_no = shipment_no

    LOG.info('Current received shipment_no is %s' % shipment_no)

    if shipment_no is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'shipment_no\'] can not be none.'})

    shipment = Shipment.objects.get(shipment_no=shipment_no)
    shipment_seria = ShipmentSerializer(shipment).data
    LOG.debut('Current shipment serialized is %s' % shipment_seria)
    shipment_details = ShipmentDetails.objects.extra(
        select={'goods_name': 't_goods.goods_name'},
        tables=['t_shipment_details', 't_goods'],
        where=['t_shipment_details.goods_code=t_goods.goods_code']
    ).filter(shipment_no=shipment_no)
    details_seria = []
    for detail in shipment_details:
        seria = ShipmentDetailsSerializer(detail)
        details_seria.append(seria.data)
    shipment_seria['details'] = details_seria
    return Response(status=status.HTTP_200_OK, data=shipment_seria, content_type='application/json;charset-utf-8')


@api_view(['POST'])
@transaction.commit_manually
def split(request):
    message = request.DATA
    
    LOG.info('Current received message is %s' % message)

    if message.get('orders_no') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'orders_code\'] can not be none.'})
    if message.get('status') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'status\'] can not be none.'})
    if message.get('status') != 5:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'The value of Attribute[\'status\'] is error, expect 5 but actual %s'
                                       % message.get('status')})
    if message.get('customer_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'customer_code\'] can not be none.'})
    if message.get('customer_name') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'customer_name\'] can not be none.'})
    if message.get('effective_date') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'effective_date\'] can not be none.'})
    if message.get('address') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'address\'] can not be none.'})
    if message.get('customer_tel') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'customer_tel\'] can not be none.'})
    if message.get('package_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'package_code\'] can not be none.'})
    if message.get('creator') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'creator\'] can not be none.'})
    if message.get('updater') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'updater\'] can not be none.'})
    try:
        package_details = ProductPackageDetails.objects.extra(
            select={'product_level': 't_product.product_level'},
            tables=['t_product'],
            where=['t_product_package_details.product_code=t_product.product_code'],
        ).filter(message('package_code'))
        products_dict = dict()
        for package_detail in package_details:
            if package_detail.product_level in products_dict:
                entry = products_dict.get(package_detail.product_level)
                LOG.debug('The product_code is %s, package_code is %s' % (package_detail.product_code, 
                                                                          package_detail.package_code))
                entry[package_detail.product_code] = package_detail
            else:
                entry = dict()
                entry[package_detail.product_code] = package_detail
                products_dict[package_detail.product_level] = entry
        LOG.debug('Current count of the products_dict is %s' % len(products_dict))
        strptime = time.strptime(message.get('effective_date'), '%Y-%m-%d')
        effective_month = strptime.tm_mon
        if effective_month in (9, 10, 11):
            in_one_list = []
        elif effective_month == 12:
            in_one_list = [products_dict.pop(1), products_dict.pop(2)]
        elif effective_month == 1:
            in_one_list = [products_dict.pop(1), products_dict.pop(2), products_dict.pop(3)]
        elif effective_month == 2:
            in_one_list = [products_dict.pop(1), products_dict.pop(2), products_dict.pop(3), products_dict.pop(4)]
        elif effective_month == 3:
            in_one_list = [products_dict.pop(1), products_dict.pop(2), products_dict.pop(3), 
                     products_dict.pop(4), products_dict.pop(5)]
        elif effective_month == 4:
            in_one_list = [products_dict.pop(1), products_dict.pop(2), products_dict.pop(3), 
                     products_dict.pop(4), products_dict.pop(5), products_dict.pop(6)]
        elif effective_month == 5:
            in_one_list = [products_dict.pop(1), products_dict.pop(2), products_dict.pop(3),
                     products_dict.pop(4), products_dict.pop(5), products_dict.pop(6), 
                     products_dict.pop(7)]
        elif effective_month == 6:
            in_one_list = [products_dict.pop(1), products_dict.pop(2), products_dict.pop(3),
                     products_dict.pop(4), products_dict.pop(5), products_dict.pop(6),
                     products_dict.pop(7), products_dict.pop(8)]
        elif effective_month == 7:
            in_one_list = [products_dict.pop(1), products_dict.pop(2), products_dict.pop(3),
                     products_dict.pop(4), products_dict.pop(5), products_dict.pop(6),
                     products_dict.pop(7), products_dict.pop(8), products_dict.pop(9)]
        else:
            in_one_list = products_dict.values()
            products_dict.clear()
        shipments = assemble_shipments(in_one_list, products_dict, message)
        transaction.commit()
    except Exception as e:
        LOG.error('Orders split error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Orders split error.'})
    return Response(status=status.HTTP_200_OK, data=shipments, content_type='application/json;charset-utf-8')


@transaction.commit_manually
def assemble_shipments(in_one_list=[], products_dict={}, message={}):
    in_one_dict = dict()
    for item in in_one_list:
        if item.product_code in in_one_dict:
            in_one_dict.get(item.goods_code).qty += item.qty
        else:
            in_one_dict[item.goods_code] = item
    LOG.debug('Current first shipment is %s' % in_one_dict)
    shipment_no = uuid.uuid4()
    now_time = datetime.now()
    total_qty = 0
    shipments = []
    if len(in_one_list) == 0:
        for product_code, product in in_one_dict.items():
            rid = '%s%s' % (shipment_no, product_code)
            detail = ShipmentDetails(
                id=rid,
                shipment_no=shipment_no,
                product_code=product_code,
                qty=product.qty,
                is_product=1,
                is_gift=0,
                create_time=now_time,
                creator=message.get('creator'),
                update_time=now_time,
                updater=message.get('updater'),
                status=0
            )
            total_qty += product.qty
            detail.save()
        shipment = Shipment(
            shipment_no=shipment_no,
            orders_no=message.get('orders_no'),
            customer_no=message.get('customer_code'),
            customer_name=message.get('customer_name'),
            address=message.get('address'),
            customer_tel=message.get('customer_tel'),
            has_invoice=int(message.get('has_invoice')),
            amount=message.get('amount'),
            shipped_qty=total_qty,
            express_code='',
            express_orders_no='',
            express_name='',
            express_cost=0.00,
            courier='',
            courier_tel='',
            create_time=now_time,
            creator=message.get('creator'),
            update_time=now_time,
            updater=message.get('updater'),
            status=0
        )
        shipment.save()
        shipment_seria = ShipmentSerializer(shipment).data
        shipments.append(shipment_seria)
    for level, package_detail in products_dict.items():
        LOG.debug('Current level is %s' % level)
        shipment_no = uuid.uuid4()
        total_qty = 0
        for product_code, product in package_detail.items():
            rid = '%s%s' % (shipment_no, product_code)
            detail = ShipmentDetails(
                id=rid,
                shipment_no=shipment_no,
                product_code=product_code,
                qty=product.qty,
                is_product=1,
                is_gift=0,
                create_time=now_time,
                creator=message.get('creator'),
                update_time=now_time,
                updater=message.get('updater'),
                status=0
            )
            total_qty += product.qty
            detail.save()
        shipment = Shipment(
            shipment_no=shipment_no,
            orders_no=message.get('orders_no'),
            customer_no=message.get('customer_code'),
            customer_name=message.get('customer_name'),
            address=message.get('address'),
            customer_tel=message.get('customer_tel'),
            has_invoice=int(message.get('has_invoice')),
            amount=message.get('amount'),
            shipped_qty=total_qty,
            express_code='',
            express_orders_no='',
            express_name='',
            express_cost=0.00,
            courier='',
            courier_tel='',
            create_time=now_time,
            creator=message.get('creator'),
            update_time=now_time,
            updater=message.get('updater'),
            status=0
        )
        shipment.save()
        shipment_seria = ShipmentSerializer(shipment).data
        shipments.append(shipment_seria)
    return shipments
