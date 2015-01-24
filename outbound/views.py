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
from big_house.models import ProductDetails, ShipmentDetails, Shipment
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
    if message.get('details') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'details\'] can not be none.'})
    if len(message.get('details')) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'details\'] can not be empty.'})
    if message.get('creator') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'creator\'] can not be none.'})
    if message.get('updater') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        data={'error': 'Attribute[\'updater\'] can not be none.'})
    try:
        query_list = ProductDetails.objects.extra(
            select={'product_level': 't_product.product_level'},
            tables=['t_product'],
            where=['t_product_details.product_code=t_product.product_code and t_product.package_code=%s'],
            params=[message.get('package_code')])
        goods_dict = dict()
        for item in query_list:
            LOG.debug('Item of query result is %s' % item)
            if item.product_level in goods_dict:
                entry = goods_dict.get(item.product_level)
                entry[item.goods_code] = item
            else:
                entry = dict()
                entry[item.goods_code] = item
                goods_dict[item.product_level] = entry
        LOG.debug('Current goods_dict is %s' % goods_dict)
        strptime = time.strptime(message.get('effective_date'), '%Y-%m-%d')
        effective_month = strptime.tm_mon
        now_time = datetime.now()
        shipments = []
        if effective_month in (9, 10, 11):
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 12:
            first = [goods_dict.pop(1), goods_dict.pop(2)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 1:
            first = [goods_dict.pop(1), goods_dict.pop(2), goods_dict.pop(3)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_dict in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for level, goods_entry in goods_dict.items():
                    LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 2:
            first = [goods_dict.pop(1), goods_dict.pop(2), goods_dict.pop(3), goods_dict.pop(4)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 3:
            first = [goods_dict.pop(1), goods_dict.pop(2), goods_dict.pop(3), 
                     goods_dict.pop(4), goods_dict.pop(5)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 4:
            first = [goods_dict.pop(1), goods_dict.pop(2), goods_dict.pop(3), 
                     goods_dict.pop(4), goods_dict.pop(5), goods_dict.pop(6)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 5:
            first = [goods_dict.pop(1), goods_dict.pop(2), goods_dict.pop(3),
                     goods_dict.pop(4), goods_dict.pop(5), goods_dict.pop(6), 
                     goods_dict.pop(7)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 6:
            first = [goods_dict.pop(1), goods_dict.pop(2), goods_dict.pop(3),
                     goods_dict.pop(4), goods_dict.pop(5), goods_dict.pop(6),
                     goods_dict.pop(7), goods_dict.pop(8)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.get('qty'),
                        status=0
                    )
                    total_qty += goods_detail.get('qty')
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        elif effective_month == 7:
            first = [goods_dict.pop(1), goods_dict.pop(2), goods_dict.pop(3),
                     goods_dict.pop(4), goods_dict.pop(5), goods_dict.pop(6),
                     goods_dict.pop(7), goods_dict.pop(8), goods_dict.pop(9)]
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
            for level, goods_entry in goods_dict.items():
                LOG.debug('Current level is %s' % level)
                shipment_no = uuid.uuid4()
                total_qty = 0
                for goods_code, goods_detail in goods_entry.items():
                    rid = '%s%s' % (shipment_no, goods_code)
                    detail = ShipmentDetails(
                        id=rid,
                        shipment_no=shipment_no,
                        code=goods_code,
                        type=1,
                        qty=goods_detail.qty,
                        status=0
                    )
                    total_qty += goods_detail.qty
                    detail.save()
                shipment = Shipment(
                    shipment_no=shipment_no,
                    orders_no=message.get('orders_no'),
                    customer_no=message.get('customer_no'),
                    customer_name=message.get('customer_name'),
                    address=message.get('address'),
                    customer_tel=message.get('customer_tel'),
                    has_invoie=message.get('has_invoice'),
                    amount=message.get('amount'),
                    shipped_qty=total_qty,
                    express_code='',
                    express_orders_no='',
                    express_name='',
                    express_cost='',
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
        else:
            first = goods_dict.values()
            first_dict = dict()
            for item in first:
                if item.goods_code in first_dict:
                    first_dict.get(item.goods_code).qty += item.qty
                else:
                    first_dict[item.goods_code] = item
            LOG.debug('Current first shipment is %s' % first_dict)
            total_qty = 0
            shipment_no = uuid.uuid4()
            for goods_code, goods_detail in first_dict.items():
                rid = '%s%s' % (shipment_no, goods_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=goods_code,
                    type=1,
                    qty=goods_detail.get('qty'),
                    status=0
                )
                total_qty += goods_detail.get('qty')
                detail.save()
            shipment = Shipment(
                shipment_no=shipment_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_no'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoie=message.get('has_invoice'),
                amount=message.get('amount'),
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost='',
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
        transaction.commit()
    except Exception as e:
        LOG.error('Orders split error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Orders split error.'})
    return Response(status=status.HTTP_200_OK, data=shipments, content_type='application/json;charset-utf-8')
