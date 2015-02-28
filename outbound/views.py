# Create your views here.
from calendar import monthrange
from datetime import datetime
import datetime as dtime
import logging
import uuid
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from big_house.models import ProductDetails, ShipmentDetails, Shipment, ProductPackageDetails, Product, Goods, \
    WarehouseGoodsDetails, WarehouseProductDetails, StorageRecords, PickingOrdersDetails, PickingOrders, Warehouse
from big_house.serializers import ShipmentDetailsSerializer, ShipmentSerializer, PickingOrdersSerializer, \
    PickingOrdersDetailsSerializer
from uudragon_wms.local.settings import DEFAULT_PAGE_SIZE, STORAGE_RECORD_TYPE_OUTPUT


LOG = logging.getLogger(__name__)


@api_view(['POST'])
def save_shipment(request):
    message = request.DATA

    LOG.info('Current received message is %s.' % message)

    try:
        shipment = Shipment.objects.filter(shipment_no=message.get('shipment_no')).first()
        now_time = datetime.now()
        if shipment is not None:
            if shipment.status != 0:
                return Response(status=status.HTTP_200_OK)
            ShipmentDetails.objects.filter(shipment_no=message.get('shipment_no')).delete()
            shipment.sent_date = message.get('sent_date')
            shipment.updater = message.get('updater')
            shipment.update_time = now_time
        else:
            shipment = Shipment(
                shipment_no=message.get('shipment_no'),
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_code'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoice=int(message.get('has_invoice')),
                sent_date=datetime.strptime(message.get('sent_date'), '%Y-%m-%d'),
                amount=message.get('amount'),
                create_time=now_time,
                creator=message.get('creator'),
                update_time=now_time,
                updater=message.get('updater'),
                status=0
            )
        rece_details = message.get('details')
        total_qty = 0
        for rece_detail in rece_details:
            shipment_detail = ShipmentDetails(
                id='%s%s' % (message.get('shipment_no'), rece_detail.get('code')),
                shipment_no=message.get('shipment_no'),
                code=rece_detail.get('code'),
                is_product=rece_detail.get('is_product'),
                is_gift=rece_detail.get('is_gift'),
                qty=rece_detail.get('qty'),
                status=0,
                creator=message.get('updater'),
                updater=message.get('updater'),
                create_time=now_time,
                update_time=now_time
            )
            shipment_detail.save()
            total_qty += shipment_detail.qty
        shipment.shipped_qty = total_qty
        shipment.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Save shipment information error. [ERROR] %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Save shipment information error'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.commit_manually
def check(request):
    message = request.DATA
    
    LOG.info('Current received message is %s.' % message)
    
    try:
        shipment = Shipment.objects.select_for_update().filter(shipment_no=message.get('shipment_no')).first()
        if shipment is not None:
            ShipmentDetails.objects.filter(shipment_no=message.get('shipment_no')).delete()
            now_time = datetime.now()
            rece_details = message.get('details')
            total_qty = 0
            for rece_detail in rece_details:
                shipment_detail = ShipmentDetails(
                    id='%s%s' % (message.get('shipment_no'), rece_detail.get('code')),
                    shipment_no=message.get('shipment_no'),
                    code=rece_detail.get('code'),
                    is_product=rece_detail.get('is_product'),
                    is_gift=rece_detail.get('is_gift'),
                    qty=int(rece_detail.get('qty')),
                    status=0,
                    creator=message.get('updater'),
                    updater=message.get('updater'),
                    create_time=now_time,
                    update_time=now_time
                )
                LOG.debug(type(shipment_detail.qty))
                total_qty += shipment_detail.qty
                shipment_detail.save()
            shipment.shipped_qty = total_qty
            shipment.warehouse = message.get('warehouse')
            shipment.sent_date = datetime.strptime(message.get('sent_date'), '%Y-%m-%d')
            shipment.updater = message.get('updater')
            shipment.update_time = now_time
            shipment.status = 1
            shipment.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Check error. message is %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Check error'},
                        content_type='application/json;charset=utf-8')
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
    
    now_time = datetime.now()
    try:
        query_month = int(message.get('month')) if message.get('month') is not None else now_time.month
        query_list = Shipment.objects.filter(
            sent_date__month=query_month, sent_date__year=now_time.year, status=0).order_by('sent_date').order_by(
            'update_time')
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
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


@api_view(['GET'])
def query_shipment(request, shipment_no):
    shipment_no = shipment_no

    LOG.info('Current received shipment_no is %s' % shipment_no)

    if shipment_no is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'shipment_no\'] can not be none.'})

    try:
        shipment = Shipment.objects.get(shipment_no=shipment_no)
        shipment_seria = ShipmentSerializer(shipment).data
        LOG.debug('Current shipment serialized is %s' % shipment_seria)
        # shipment_details = ShipmentDetails.objects.extra(
        #     select={'goods_name': 't_goods.goods_name'},
        #     tables=['t_shipment_details', 't_goods'],
        #     where=['t_shipment_details.goods_code=t_goods.goods_code']
        # ).filter(shipment_no=shipment_no)
        shipment_details = ShipmentDetails.objects.filter(shipment_no=shipment_no)
        details_seria = []
        for detail in shipment_details:
            seria = ShipmentDetailsSerializer(detail).data
            if detail.is_product:
                product = Product.objects.filter(product_code=detail.code).first()
                seria['name'] = product.product_name
            elif detail.is_gift:
                goods = Goods.objects.filter(goods_code=detail.code).first()
                seria['name'] = goods.goods_name
            details_seria.append(seria)
        shipment_seria['details'] = details_seria
    except Exception as e:
        LOG.error('Query shipment information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query shipment information error'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=shipment_seria, content_type='application/json;charset=utf-8')


@api_view(['GET'])
def query_by_ordersno(request, orders_no):
    orders_no = orders_no

    LOG.info('Current received orders_no is %s' % orders_no)

    if orders_no is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'orders_no\'] can not be none.'})
    shipments_seria = []
    try:
        shipments = Shipment.objects.filter(orders_no=orders_no)
        LOG.debug('Current count of shipments is %s' % len(shipments))
        
        for shipment in shipments:
            seria = ShipmentSerializer(shipment)
            shipments_seria.append(seria.data)
    except Exception as e:
        LOG.error('Query shipment by orders_no error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query shipment by orders_no error.'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=shipments_seria, content_type='application/json;charset=utf-8')


@api_view(['POST'])
def split(request):
    message = request.DATA
    
    LOG.info('Current received message is %s' % message)

    if message.get('orders_no') is None:
        LOG.error('Attribute[\'orders_no\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'orders_no\'] can not be none.'})
    if message.get('status') is None:
        LOG.error('Attribute[\'status\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'status\'] can not be none.'})
    if message.get('status') != 5:
        LOG.error('The value of Attribute[\'status\'] is error, expect 5 but actual %s'
                  % message.get('status'))
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'The value of Attribute[\'status\'] is error, expect 5 but actual %s'
                                       % message.get('status')})
    if message.get('customer_code') is None:
        LOG.error('Attribute[\'customer_code\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'customer_code\'] can not be none.'})
    if message.get('customer_name') is None:
        LOG.error('Attribute[\'customer_name\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'customer_name\'] can not be none.'})
    if message.get('effective_date') is None:
        LOG.error('Attribute[\'effective_date\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'effective_date\'] can not be none.'})
    if message.get('address') is None:
        LOG.error('Attribute[\'address\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'address\'] can not be none.'})
    if message.get('customer_tel') is None:
        LOG.error('Attribute[\'customer_tel\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'customer_tel\'] can not be none.'})
    if message.get('package_code') is None:
        LOG.error('Attribute[\'package_code\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'package_code\'] can not be none.'})
    if message.get('creator') is None:
        LOG.error('Attribute[\'creator\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'creator\'] can not be none.'})
    if message.get('updater') is None:
        LOG.error('Attribute[\'updater\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'updater\'] can not be none.'})
    try:
        package_details = ProductPackageDetails.objects.extra(
            select={'product_level': 't_product.product_level'},
            tables=['t_product'],
            where=['t_product_package_details.product_code=t_product.product_code'],
        ).filter(package_code=message.get('package_code'))
        LOG.debug('Query records count is %s' % len(package_details))
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
        strptime = datetime.strptime(message.get('effective_date'), '%Y-%m-%d')
        if message.get('source') != 3:
            strptime = strptime + dtime.timedelta(days=2)
        else:
            strptime = strptime + dtime.timedelta(days=monthrange(strptime.year, strptime.month)[1])
        effective_month = strptime.month
        in_one_list = []
        num = 0
        if effective_month in (9, 10, 11):
            LOG.info('Effective_month are 9, 10, 11')
            in_one_list = []
        elif effective_month == 12:
            LOG.info('Effective_month is 12')
            num = 2
        elif effective_month == 1:
            num = 3
        elif effective_month == 2:
            num = 4
        elif effective_month == 3:
            LOG.info('Effective_month is 3')
            num = 5
        elif effective_month == 4:
            LOG.info('Effective_month is 4')
            num = 6
        elif effective_month == 5:
            LOG.info('Effective_month is 5')
            num = 7
        elif effective_month == 6:
            LOG.info('Effective_month is 6')
            num = 8
        elif effective_month == 7:
            LOG.info('Effective_month is 7')
            num = 9
        else:
            LOG.info('Effective_month is 8')
            in_one_list = products_dict.values()
            products_dict.clear()
        for i in range(num):
            index = i + 1
            if index in products_dict:
                item = products_dict.pop(index)
                LOG.debug('Current item is %s' % item)
                in_one_list.append(item)
        shipments = assemble_shipments(in_one_list, products_dict, message, strptime)
    except Exception as e:
        LOG.error('Orders split error.\n [ERROR]:%s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Orders split error.'})
    return Response(status=status.HTTP_200_OK, data=shipments, content_type='application/json;charset=utf-8')


@transaction.commit_manually
def assemble_shipments(in_one_list=[], products_dict={}, message={}, sent_date=None):
    in_one_dict = dict()
    shipments = []
    strptime = sent_date
    try:
        for item in in_one_list:
            LOG.debug('Item is %s' % item)
            LOG.debug('Current in_one_dict is %s' % in_one_dict)
            for product_code, package_detail in item.items():
                if product_code in in_one_dict:
                    LOG.debug('The package_detail of %s is %s' % (product_code, package_detail))
                    in_one_dict.get['product_code'].qty += package_detail.qty
                else:
                    in_one_dict[product_code] = package_detail
        LOG.debug('Current first shipment is %s' % in_one_dict)
        shipment_no = uuid.uuid4()
        now_time = datetime.now()
        total_qty = 0
        warehouse = Warehouse.objects.filter(type=1).first()
        warehouse_no = warehouse.warehouse_code
        if len(in_one_list) != 0:
            LOG.debug('----------->Create one shipment')
            for product_code, product in in_one_dict.items():
                rid = '%s%s' % (shipment_no, product_code)
                LOG.debug('New Shipment id is %s' % rid)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=product_code,
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
                warehouse=warehouse_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_code'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoice=int(message.get('has_invoice')),
                amount=0.0,
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost=0.00,
                courier='',
                courier_tel='',
                sent_date=strptime,
                create_time=now_time,
                creator=message.get('creator'),
                update_time=now_time,
                updater=message.get('updater'),
                status=0
            )
            shipment.save()
            shipment_seria = ShipmentSerializer(shipment).data
            shipments.append(shipment_seria)
            strptime = strptime + dtime.timedelta(days=monthrange(strptime.year, strptime.month)[1])
        LOG.debug('-------------> Create another shipments.')
        for level, package_detail in products_dict.items():
            LOG.debug('Current level is %s' % level)
            shipment_no = uuid.uuid4()
            total_qty = 0
            for product_code, product in package_detail.items():
                LOG.debug('Current product code is %s' % product_code)
                rid = '%s%s' % (shipment_no, product_code)
                detail = ShipmentDetails(
                    id=rid,
                    shipment_no=shipment_no,
                    code=product_code,
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
                warehouse=warehouse_no,
                orders_no=message.get('orders_no'),
                customer_no=message.get('customer_code'),
                customer_name=message.get('customer_name'),
                address=message.get('address'),
                customer_tel=message.get('customer_tel'),
                has_invoice=int(message.get('has_invoice')),
                amount=0.0,
                shipped_qty=total_qty,
                express_code='',
                express_orders_no='',
                express_name='',
                express_cost=0.00,
                courier='',
                courier_tel='',
                sent_date=strptime,
                create_time=now_time,
                creator=message.get('creator'),
                update_time=now_time,
                updater=message.get('updater'),
                status=0
            )
            shipment.save()
            shipment_seria = ShipmentSerializer(shipment).data
            shipments.append(shipment_seria)
            strptime = strptime + dtime.timedelta(days=monthrange(strptime.year, strptime.month)[1])
        transaction.commit()
    except Exception as e:
        LOG.error('Orders split error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        raise e
    return shipments


@api_view(['POST'])
@transaction.commit_manually
def picking(request, picking_no):
    LOG.info('Current method [picking], received picking_no is %s' % picking_no)

    if picking_no is None:
        LOG.error('Attribute[\'picking_no\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'picking_no\'] can not be none.'})

    message = request.DATA
    
    LOG.info('Current request body is %s' % message)

    try:
        picking_orders = PickingOrders.objects.select_for_update().filter(picking_no=picking_no, status=0).first()
        picking_orders.status = 1
        picking_orders.updater = message.get('updater')
        picking_orders.update_time = datetime.now()
        picking_orders.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Shipment picking error, message is %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Shipment picking error.'})
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.commit_manually
def picking_completed(request, picking_no):
    LOG.info('Current method [picking_completed], received picking_no is %s' % picking_no)
    
    if picking_no is None:
        LOG.error('Attribute[\'picking_no\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'picking_no\'] can not be none.'})
    
    message = request.DATA
    
    LOG.info('Current request body is %s' % message)
    
    try:
        picking_orders = PickingOrders.objects.select_for_update().filter(picking_no=picking_no, status=1).first()
        picking_orders.status = 2
        picking_orders.save()
        picking_orders_details = PickingOrdersDetails.objects.filter(picking_no=picking_no)
    
        shipment_nos = []
        for picking_detail in picking_orders_details:
            shipment_nos.append(picking_detail.id[36:72])
        shipments = Shipment.objects.select_for_update().filter(shipment_no__in=shipment_nos)
        for shipment in shipments:
            shipment_details = ShipmentDetails.objects.filter(shipment_no=shipment.shipment_no)
            out_goods = dict()
            for item in shipment_details:
                if item.is_gift:
                    goods = WarehouseGoodsDetails.objects.filter(goods_code=item.code).filter(
                        warehouse=shipment.warehouse).first()
                    goods.qty -= item.qty
                    goods.not_picking_qty -= item.qty
                    goods.save()
                    if goods.goods_code in out_goods:
                        out_goods[goods.goods_code] += item.qty
                    else:
                        out_goods[goods.goods_code] = item.qty
                elif item.is_product:
                    product = WarehouseProductDetails.objects.filter(product_code=item.code).filter(
                        warehouse=shipment.warehouse).first()
                    product.qty -= item.qty
                    product_details = ProductDetails.objects.filter(product_code=product.product_code)
                    for detail in product_details:
                        goods = WarehouseGoodsDetails.objects.filter(goods_code=detail.goods_code).filter(
                            warehouse=shipment.warehouse).first()
                        goods.qty -= detail.qty
                        goods.picking_qty -= detail.qty
                        goods.save()
                        if goods.goods_code in out_goods:
                            out_goods[goods.goods_code] += item.qty
                        else:
                            out_goods[goods.goods_code] = item.qty
                    product.save()
            LOG.info('Current output goods is %s' % out_goods)
            now_time = datetime.now()
            shipment.status = 3
            shipment.updater = message.get('updater')
            shipment.update_time = now_time
            for goods_code, qty in out_goods.items():
                storage_record = StorageRecords(
                    goods_code=goods_code,
                    goods_qty=qty,
                    code=message.get('shipment_no'),
                    warehouse=shipment.warehouse,
                    type=STORAGE_RECORD_TYPE_OUTPUT,
                    create_time=now_time,
                    creator=message.get('updater'),
                    update_time=now_time,
                    updater=message.get('updater'),
                    status=0
                )
                storage_record.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Shipment picking error, message is %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Shipment picking error.'})
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def query_shipments_by_picking_no(request, picking_no):
    LOG.info('Current method [picking_completed], received picking_no is %s' % picking_no)

    if picking_no is None:
        LOG.error('Attribute[\'picking_no\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'picking_no\'] can not be none.'})
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
        picking_orders_details = PickingOrdersDetails.objects.filter(picking_no=picking_no)
        shipment_nos = []
        for picking_detail in picking_orders_details:
            shipment_nos.append(picking_detail.id[36:72])
        shipments = Shipment.objects.filter(shipment_no__in=shipment_nos)
        paginator = Paginator(shipments, pageSize, orphans=0, allow_empty_first_page=True)
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
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


@api_view(['POST'])
@transaction.commit_manually
def sent(request):
    message = request.DATA

    LOG.info('Current received message is %s' % message)
    try:
        now_time = datetime.now()
        shipment = Shipment.objects.filter(shipment_no=message.get('shipment_no'), status=3).first()
        shipment.express_code = message.get('express_code')
        shipment.express_orders_no = message.get('express_orders_no')
        shipment.express_name = message.get('express_name')
        shipment.express_cost = message.get('express_cost')
        shipment.courier = message.get('courier')
        shipment.courier_tel = message.get('courier_tel')
        shipment.status = 4
        shipment.updater = message.get('updater')
        shipment.update_time = now_time
        shipment.save()
        records = StorageRecords.objects.filter(code=message.get('shipment_no'))
        for record in records:
            record.status = 1
            record.updater = message.get('updater')
            record.update_time = now_time
            record.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Sent error, message is %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Sent error.'})
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.commit_manually
def set_orders_amount(request):
    message = request.DATA
    
    LOG.info('Current received message is %s' % message)
    
    if message.get('orders_no') is None:
        LOG.error('Attribute[\'orders_no\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'orders_no\'] can not be none.'})

    if message.get('amount') is None or message.get('amount') == 0.00:
        LOG.error('The value of Attribute[\'amount\'] is invalid.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'The value of Attribute[\'amount\'] is invalid.'})

    if message.get('updater') is None:
        LOG.error('The value of Attribute[\'updater\'] is invalid.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'The value of Attribute[\'updater\'] is invalid.'})
    
    try:
        first_shipment = Shipment.objects.select_for_update().filter(
            orders_no=message.get('orders_no')).order_by('sent_date').first()
        LOG.info("The first shipment of orders [%s] will be sent at %s" 
                 % (message.get('orders_no'), first_shipment.sent_date))
        first_shipment.amount = message.get('amount')
        first_shipment.updater = message.get('updater')
        first_shipment.update_time = datetime.now()
        first_shipment.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Amount setting error. [ERROR] is %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Sent error.'})
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.commit_manually
def assemble_picking_orders(request):
    message = request.DATA
    
    LOG.info('Current method is [assemble_pickings], received message is %s' % message)
    
    if message.get('shipment_nos') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Request attribute [shipment_nos] can not be none.'})
    if not isinstance(message.get('shipment_nos'), type([])):
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Request attribute [shipment_nos] must be an array.'})
    try:
        shipments = Shipment.objects.select_for_update().filter(shipment_no__in=message.get('shipment_nos'))
        effective_nos = []
        for shipment in shipments:
            if shipment.status == 1:
                effective_nos.append(shipment.shipment_no)
        else:
            message.pop('shipment_nos')
        if len(effective_nos) != 0:
            shipment_details = ShipmentDetails.objects.select_for_update().filter(shipment_no__in=effective_nos)
            details_dict = dict()
            picking_no = uuid.uuid4()
            now_time = datetime.now()
            total_qty = 0
            for shipment_detail in shipment_details:
                if shipment_detail.code in details_dict:
                    details_dict[shipment_detail.code].qty += shipment_detail.qty
                else:
                    picking_detail = PickingOrdersDetails(
                        id='%s%s' % (picking_no, shipment_detail.shipment_no),
                        picking_no=picking_no,
                        code=shipment_detail.code,
                        is_product=shipment_detail.is_product,
                        is_gift=shipment_detail.is_gift,
                        qty=shipment_detail.qty,
                        creator=message.get('creator'),
                        create_time=now_time,
                        updater=message.get('updater'),
                        update_time=now_time
                    )
                    details_dict[shipment_detail.code] = picking_detail
                total_qty += shipment_detail.qty
            picking_details_srias = []
            for picking_detail in details_dict.values():
                picking_detail.save()
                picking_detail_seria = PickingOrdersDetailsSerializer(picking_detail)
                if picking_detail.is_product:
                    product = Product.objects.filter(product_code=picking_detail.code).first()
                    name = product.product_name
                elif picking_detail.is_gift:
                    goods = Goods.objects.filter(goods_code=picking_detail.code).first()
                    name = goods.goods_name
                seria_data = picking_detail_seria.data
                seria_data['name'] = name
                picking_details_srias.append(seria_data)
            LOG.debug('Total_qty is %s' % total_qty)
            picking_orders = PickingOrders(
                picking_no=picking_no,
                picking_qty=total_qty,
                creator=message.get('creator'),
                create_time=now_time,
                updater=message.get('updater'),
                update_time=now_time,
                status=0
            )
            picking_orders.save()
            for shipment in shipments:
                shipment.status = 2
                shipment.updater = message.get('updater')
                shipment.update_time = now_time
            picking_orders_seria = PickingOrdersSerializer(picking_orders).data
            picking_orders_seria['details'] = picking_details_srias
        transaction.commit()
    except Exception as e:
        LOG.error('Assemble picking_orders error. [ERROR] is %s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Assemble picking_orders error.'})
    return Response(status=status.HTTP_200_OK, data=picking_orders_seria, content_type='application/json;charset=utf-8')


@api_view(['POST'])
def query_picking_orders_list(request):
    message = request.DATA
    
    LOG.info('Current method is [query_picking_orders_list], received message is %s' % message)

    pageSize = message.pop('pageSize')
    if pageSize is None or pageSize == 0:
        pageSize = DEFAULT_PAGE_SIZE
    pageNo = message.pop('pageNo')
    if pageNo is None or pageNo == 0:
        pageNo = 1

    resp_message = dict()

    now_time = datetime.now()
    try:
        query_month = int(message.get('month')) if message.get('month') is not None else now_time.month
        query_list = PickingOrders.objects.filter(create_time__month=query_month, create_time__year=now_time.year, status=1).order_by('create_time')
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
            record_seria = PickingOrdersSerializer(item)
            resp_array.append(record_seria.data)
        resp_message['records'] = resp_array
        resp_message['recordsCount'] = paginator.count
        resp_message['pageSize'] = pageSize
        resp_message['pageNumber'] = total_page_count
        resp_message['pageNo'] = pageNo
    except Exception as e:
        LOG.error('Query picking orders information error. [ERROR] %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'error': 'Query picking orders information error'},
                        content_type='application/json;charset=utf-8')
    return Response(status=status.HTTP_200_OK, data=resp_message, content_type='application/json;charset=utf-8')


@api_view(['GET'])
def query_single_picking_orders(request, picking_no):
    LOG.info('Current method [query_], received picking_no is %s' % picking_no)

    if picking_no is None:
        LOG.error('Attribute[\'picking_no\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset=utf-8',
                        data={'error': 'Attribute[\'picking_no\'] can not be none.'})
    try:
        picking_orders = PickingOrders.objects.filter(picking_no=picking_no).first()
        picking_orders_details = PickingOrdersDetails.objects.filter(picking_no=picking_no)
        picking_details_srias = []
        for picking_detail in picking_orders_details:
            picking_detail_seria = PickingOrdersDetailsSerializer(picking_detail)
            if picking_detail.is_product:
                product = Product.objects.filter(product_code=picking_detail.code).first()
                picking_detail_seria.name = product.product_name
            elif picking_detail.is_gift:
                goods = Goods.objects.filter(goods_code=picking_detail.code).first()
                picking_detail_seria.name = goods.goods_name
            picking_details_srias.append(picking_detail_seria.data)
        picking_orders_seria = PickingOrdersSerializer(picking_orders).data
        picking_orders_seria['details'] = picking_details_srias
    except Exception as e:
        LOG.error('Query picking_orders error. [ERROR] is %s' % str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset=utf-8',
                        date={'error': 'Query picking_orders error.'})
    return Response(status=status.HTTP_200_OK, data=picking_orders_seria, content_type='application/json;charset=utf-8')

