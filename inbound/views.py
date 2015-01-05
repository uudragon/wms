from datetime import datetime
import logging
from django.db import transaction

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from big_house.models import Receipt, ReceiptDetails, StorageRecord, WarehouseGoodsDetails
from commons.exceptions import ValueIsNoneException
from uudragon_wms.local.settings import INBOUND_RECEIPT_STATUS_NONE, INBOUND_RECEIPT_DETAIL_STATUS_NONE, \
    INBOUND_RECEIPT_STATUS_CANCEL, YN_NO, INBOUND_RECEIPT_DETAIL_STATUS_CANCEL, \
    INBOUND_RECEIPT_DETAIL_STATUS_COMPLETED, INBOUND_RECEIPT_DETAIL_STATUS_PRE_STORAGE, STORAGE_RECORD_TYPE_RECEIPT, \
    INBOUND_RECEIPT_STATUS_COMPLETED, INBOUND_RECEIPT_STATUS_UNCOMPLETED

LOG = logging.getLogger(__name__)


@api_view(['POST'])
@transaction.commit_manually
def create_receipt(request):
    message = request.DATA
    
    LOG.info('Current method is %s, received message is %s' % (__name__, message))

    if message.get('receipt_code') is None:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'receipt_code\'] can not be none.'})
    code = message.get('receipt_code')
    if message.get('qty') is None:
        LOG.error('Attribute[\'qty\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'qty\'] can not be none.'})
    details = message.get('details')
    if details is None or len(details) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'details\'] must be a non-empty array.'})

    nowTime = datetime.now()
    try:
        receipt = Receipt(
            receipt_code=code,
            receipt_date=message.get('receipt_date'),
            receipt_desc=message.get('receipt_desc'),
            receipt_stat=message.get('receipt_stat'),
            warehouse=message.get('warehouse'),
            status=INBOUND_RECEIPT_STATUS_NONE,
            creator=message.get('creator'),
            create_time=nowTime,
            updater=message.get('updater'),
            update_time=nowTime,
            yn=message.get('yn')
        )
        receipt.save()
        for detail in details:
            if detail.get('goods_code') is None:
                raise ValueIsNoneException('The goods code can not be none.')
            receipt_detail = ReceiptDetails(
                id='%s%s' % (code, detail.get('goods_code')),
                goods_code=detail.get('goods_code'),
                receipt_code=code,
                qty=message.get('qty'),
                actual_qty=0,
                status=INBOUND_RECEIPT_DETAIL_STATUS_NONE,
                creator=message.get('creator'),
                create_time=nowTime,
                updater=message.get('updater'),
                update_time=nowTime
            )
            receipt_detail.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Receipt Information saved error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Receipt Information saved error.'})
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@transaction.commit_manually
def cancel_receipt(request, receipt_code):
    code = receipt_code

    LOG.debug('Current method is %s, received goods_code is %s' % (__name__, code))
    
    try:
        receipt = Receipt.objects.get(code=code)
        if receipt is not None:
            receipt.state = INBOUND_RECEIPT_STATUS_CANCEL
            receipt.yn = YN_NO
            details = ReceiptDetails.filter(code=code)
            for detail in details:
                detail.status = INBOUND_RECEIPT_DETAIL_STATUS_CANCEL
        transaction.commit()
    except Exception as e:
        LOG.error('Receipt Information cancel error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Receipt Information cancel error.'})
        
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@transaction.commit_manually
def putin(request):
    message = request.DATA
    
    LOG.info('Current method %s, received message is %s' % (__name__, message))
    
    receipt_code = message.get('receipt_code')
    if receipt_code is None:
        LOG.error('Attribute[\'receipt_code\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'receipt_code\'] can not be none.'})
    goods_code = message.get('goods_code')
    if goods_code is None:
        LOG.error('Attribute[\'goods_code\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'goods_code\'] can not be none.'})
    current_qty = message.get('qty')
    if current_qty is None:
        LOG.error('Attribute[\'qty\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'qty\'] can not be none.'})
    warehouse = message.get('warehouse')
    if warehouse is None:
        LOG.error('Attribute[\'warehouse\'] can not be none.')
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Attribute[\'warehouse\'] can not be none.'})
    
    now_time = datetime.now()
    try:
        receipt_detail = ReceiptDetails.objects.get(receipt_code=receipt_code, goods_code=goods_code)
        cur_acutal_qty = receipt_detail.actual_qty + current_qty
        if receipt_detail.qty < cur_acutal_qty:
            LOG.error('Actual qty of goods is gt the expect qty.')
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            content_type='application/json;charset-utf-8',
                            date={'error': 'Actual qty of goods is gt the expect qty.'})
        elif receipt_detail.qty == cur_acutal_qty:
            receipt_detail.status = INBOUND_RECEIPT_DETAIL_STATUS_COMPLETED
        else:
            receipt_detail.status = INBOUND_RECEIPT_DETAIL_STATUS_PRE_STORAGE
        receipt_detail.actual_qty = cur_acutal_qty
        receipt_detail.save()
        
        StorageRecord(
            goods_code=goods_code,
            goods_qty=current_qty,
            warehouse=warehouse,
            code=receipt_code,
            type=STORAGE_RECORD_TYPE_RECEIPT,
            creator=message.get('updater'),
            create_time=now_time,
            updater=message.get('updater'),
            update_time=now_time,
        ).save()
        warehouse_goods = WarehouseGoodsDetails.object.get(warehouse=warehouse, goods_code)
        if warehouse_goods is not None:
            warehouse_goods.qty += current_qty
            warehouse_goods.updater=message.get('updater')
            warehouse_goods.update_time=now_time
        else:
            warehouse_goods = WarehouseGoodsDetails(
                warehouse=warehouse,
                goods_code=goods_code,
                qty=current_qty,
                picking_qty=0,
                not_picking_qty=0,
                creator=message.get('updater'),
                create_time=now_time,
                updater=message.get('updater'),
                update_time=now_time
            )
        warehouse_goods.save()
        transaction.commit()
        details = ReceiptDetails.objects.filter(receipt_code=receipt_code)
        completed = False
        for detail in details:
            if detail.qty == detail.actual_qty:
                completed = True
            else:
                completed = False
        receipt = Receipt.objects.get(receipt_code=receipt_code)
        if completed:
            receipt.status = INBOUND_RECEIPT_STATUS_COMPLETED
        else:
            receipt.status = INBOUND_RECEIPT_STATUS_UNCOMPLETED
        receipt.save()
        transaction.commit()
    except Exception as e:
        LOG.error('Goods Putin error.\n [ERROR]:%s' % str(e))
        transaction.rollback()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content_type='application/json;charset-utf-8',
                        date={'error': 'Goods Putin error.'})
    
    return Response(status=status.HTTP_200_OK)