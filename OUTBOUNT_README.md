#####目录
- [订单拆分接口](#11-url)
- [按出库单号查询出库单接口](#21-url)
- [修改出库单接口](#31-url)
- [批量查询出库单接口](#41-url)
- [出库复核接口](#51-url)
- [出库备货锁定接口](#61-url)
- [出库拣货完成接口](#71-url)
- [发货接口](#81-url)
- [按订单号查询发货单](#91-url)
- [按订单号设置应收款金额](#101-url)
- [生成拣货单](#111-url)
- [批量查询拣货单](#121-url)
- [按拣货单号查询拣货明细](#131-url)
- [按订单号修改拣货单信息](#141-url)
- [合并出库单](#151-url)
- [上传快递单接口](#161-url)
- [批量出库复核接口](#171-url)
- [查询待打印出库单接口](#181-url)
- [同步发货单接口](#191-url)

----
#####1.订单拆分接口
接收客服系统发送的订单信息，按照一定规则将其拆分成发货单并返回将发货单信息返回给客服系统
######1.1 url
	method: POST
	wms/outbound/split/
	注意：结尾的’/’不能省略
######1.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######1.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
effective_date|date|Y|生效日期
address|String|Y|客户地址
customer_tel|String|Y|客户电话
source|Int|Y|订单来源。1：网站；2：电话；3：代理商代下单。
has_invoice|int|Y|是否有发票。0：无；1：有
package_code|String|Y|套餐编号。0：无；1：有
creator|String|Y|创建人
updater|String|Y|需改人

样例报文：

	{'orders_no':'001010101',
	'customer_code':'user001',
	'customer_name':'yonghu1',
	'effective_date':'2014-12-31',
	'address':'北京市天安门',
	'customer_tel':'18600000000',
	'source':2,
	'has_invoice':0,
	'package_code':'pack00001',
	'creator':'admin',
	'updater':'admin'}

######1.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

发货单列表

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
sent_date|String|O|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货

样例报文：

	[{
	    'orders_no':'00010101',
	    'shipment_no':'shipment0001',
	    'customer_code':'user001',
	    'customer_name':'user1',
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'amount':110.11,
	    'shipped_qty':10,
	    'has_invoice':0,
	    'sent_date':'2015-01-01',
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0
	}......]
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{'error':'Orders split error.'}

----
#####2.按出库单号查询出库单信息
按给定的出库单号查询对应的出库单信息
######2.1 url
	method: GET
	wms/outbound/shipment/${shipment_no}/
	注意：结尾的’/’不能省略, ${shipment_no}为出库单号
######2.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######2.3 请求参数
名称|类型|是否必填|说明
-|-|-|-
shipmenet_no|String|Y|出库单号

样例报文：
无

######2.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
express_code|String|Y|快递公司编号
express_orders_no|String|Y|快递单号
express_name|String|Y|快递公司名称
express_cost|decimal|Y|快递费用
courier|String|Y|快递员
courier_tel|String|Y|快递员电话
sent_date|String|Y|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货
details|array|Y|发货明细

`Details`

名称|类型|是否必填|说明
---|---|---|---
shipment_no|String|Y|出库单号
code|String|Y|编号
name|String|Y|名称
is_product|int|Y|是否产品。0：否；1：是
is_gift|int|Y|是否赠品。0：否；1：是
qty|int|Y|数量
status|int|Y|状态。0：未确认；1：已确认


样例报文：

	{
	    'orders_no':'00010101',
	    'shipment_no':'shipment0001',
	    'customer_code':'user001',
	    'customer_name':'user1',
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'amount':110.11,
	    'shipped_qty':10,
	    'has_invoice':0,
	    'express_code':'express0001',
        'express_orders_no':'010101010',
        'express_name':'顺丰',
        'express_cost':22:00,
        'courier':'aaaa',
        'courier_tel':18700000000,
        'sent_date':'2015-01-01',
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0,
	    'details':[{
	        'shipment_no':'shipment001',
	        'code':'goods001',
	        'name':'商品1'
	        'is_product':1,
	        'is_gift':0,
	        'qty':10,
	        status:0
	    }]
	}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipment query error.’}

----
#####3.保存出库单接口
该接口用于保存用户对于出库单的修改
######3.1 url
	method: POST
	wms/outbound/shipment/save/
	注意：结尾的’/’不能省略
######3.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######3.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
sent_date|String|Y|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货
details|array|Y|发货明细

Details

名称|类型|是否必填|说明
---|---|---|---
shipment_no|String|Y|出库单号
code|String|Y|编号
is_product|int|Y|是否是产品。0：否；1：是
is_gift|int|Y|是否赠品。0：否；1：是
qty|int|Y|数量
status|int|Y|状态。0：未确认；1：已确认


样例报文：

	{
	    'orders_no':'00010101',
	    'shipment_no':'shipment0001',
	    'customer_code':'user001',
	    'customer_name':'user1',
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'amount':110.11,
	    'shipped_qty':10,
	    'has_invoice':0,
        'sent_date':'2015-01-01',
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0,
	    'details':[{
	        'shipment_no':'shipment001',
	        'code':'goods001',
	        'is_product':1,
	        'is_gift':0,
	        'qty':10,
	        status:0
	    }]
	}

######3.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

无

异常响应：

	a．    HTTP_STATUS_CODE:400 Bad request；
	b．    HTTP_STATUS_CODE:500 Server Error
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

{‘error’:’Shipment query error.’}

----
#####4.批量查询出库单接口
该接口用于批量查询出库单
######4.1 url
	method: POST
	wms/outbound/shipments/
	注意：结尾的’/’不能省略
######4.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######4.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
month|Int|Y|查询月份

样例报文：

{
	'pageSize':8,
	'pageNo':1,
	'month':3
}

######4.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
---|---|---|---
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<Records-Item>

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
express_code|String|O|快递公司编号
express_orders_no|String|O|快递单号
express_name|String|O|快递公司名称
express_cost|decimal|O|快递费用
courier|String|O|快递员
courier_tel|String|O|快递员电话
sent_date|String|O|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	'records':[{
	    'orders_no':'00010101',
	    'shipment_no':'shipment0001',
	    'customer_code':'user001',
	    'customer_name':'user1',
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'amount':110.11,
	    'shipped_qty':10,
	    'has_invoice':0,
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0
		}......]
	}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}
	
----
#####5.出库拣货接口
该接口用于锁定拣货单状态，进行线下拣货操作。
######5.1 url
	method: POST
	wms/outbound/picking_orders/picking/${picking_no}/
	注意：结尾的’/’不能省略
######5.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######5.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
updater|String|Y|操作人

样例报文：
	{
	    'updater':'admin'
	}

######5.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}


----
#####6.出库拣货完成接口
该接口用于仓库操作员按照拣货后调用此接口用于确认拣货完成。调用此接口后出库单的状态先由备货中（2）-->发货中（3），
并且将出库商品记录入“商品出入库表”（状态为“预占”状态0，表示即将出库但尚未出库）并未扣除库存。
######6.1 url
	method: POST
	wms/outbound/picking_orders/picking_completed/${picking_no}/
	注意：结尾的’/’不能省略
######6.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######6.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
updater|String|Y|需改人

样例报文：
	{
	    'updater':'admin'
	}

######6.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200
	
响应报文说明：

无


异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}


----
#####7.查询拣货单对应发货单
按照拣货单号查询对应发货单
######7.1 url
	method: POST
	wms/outbound/picking_orders/query_shipments/${picking_no}/
	注意：结尾的’/’不能省略
######7.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######7.3 请求参数
无

######7.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200
	
名称|类型|是否必填|说明
---|---|---|---
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<Records-Item>

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
express_code|String|O|快递公司编号
express_orders_no|String|O|快递单号
express_name|String|O|快递公司名称
express_cost|decimal|O|快递费用
courier|String|O|快递员
courier_tel|String|O|快递员电话
sent_date|String|O|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	'records':[{
	    'orders_no':'00010101',
	    'shipment_no':'shipment0001',
	    'customer_code':'user001',
	    'customer_name':'user1',
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'amount':110.11,
	    'shipped_qty':10,
	    'has_invoice':0,
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0
		}......]
	}

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}


----
#####8.发货接口
该接口用于仓库操作员进行发货操作，此接口需要操作员提供快递单与快递员相关信息，修改出入库对应记录状态（改为“已完成（1）”）。调用此接口后出库单的状态先由发货中（3）-->已发货（4），
######8.1 url
	method: POST
	wms/outbound/shipment/sent/
	注意：结尾的’/’不能省略
######8.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######8.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
shipment_no|String|Y|发货单号
express_code|String|Y|快递公司编号
express_orders_no|String|Y|快递单号
express_name|String|Y|快递公司名称
express_cost|decimal|Y|快递费用
courier|String|Y|快递员
courier_tel|String|Y|快递员电话
updater|String|Y|需改人

样例报文：
	{
		'shipment_no':'S00001',
		'express_code':'express0001',
        'express_orders_no':'010101010',
        'express_name':'顺丰',
        'express_cost':22:00,
        'courier':'aaaa',
        'courier_tel':18700000000,
	    'updater':'admin'
	}

######8.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}
	

----
#####9.按订单号查询出库单信息
按给定的订单号查询对应的出库单信息
######9.1 url
	method: GET
	wms/outbound/shipments/orders${orders_no}/
	注意：结尾的’/’不能省略, ${orders_no}为出库单号
######9.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######9.3 请求参数

样例报文：
无

######9.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
express_code|String|Y|快递公司编号
express_orders_no|String|Y|快递单号
express_name|String|Y|快递公司名称
express_cost|decimal|Y|快递费用
courier|String|Y|快递员
courier_tel|String|Y|快递员电话
sent_date|String|Y|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货

报文样例：

	[{
	    'orders_no':'00010101',
	    'shipment_no':'shipment0001',
	    'customer_code':'user001',
	    'customer_name':'user1',
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'amount':110.11,
	    'shipped_qty':10,
	    'has_invoice':0,
	    'sent_date':'2015-01-01',
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0
	}......]
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipments query error.’}


----
#####10.按订单号设置应收款金额
该接口按给定的订单号查询最早发货的发货单数据，并将应收款金额设置到发货单信息中。
######10.1 url
	method: POST
	wms/outbound/shipment/amount_setting/
	注意：结尾的’/’不能省略
######10.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######10.3 请求参数

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
amount|Decimal（10，2）|Y|应收金额
updater|String|Y|更新人

样例报文：

	{
		'orders_no':'O00001',
		'amount':100.23,
		'updater':'admin'
	}

######10.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipments query error.’}

----
#####11.生成拣货单
该接口按给定的发货单号生成拣货单
######11.1 url
	method: POST
	wms/outbound/picking_orders/create/
	注意：结尾的’/’不能省略
######11.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######11.3 请求参数

名称|类型|是否必填|说明
---|---|---|---
shipment_nos|Array|Y|订单号数组
creator|String|Y|创建人
updater|String|Y|更新人

样例报文：

	{
		'shipment_nos':['000001','000002'],
		'creator':'admin',
		'updater':'admin'
	}

######11.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

名称|类型|是否必填|说明
---|---|---|---
picking_no|String|Y|拣货单号
picking_qty|Int|Y|拣货总数量
status|Int|Y|拣货单状态
details|Array|Y|拣货单明细
creator|String|Y|创建人
create_time|String|Y|创建时间
updater|String|更新人
update_time|String|Y|更新时间

<拣货单明细>

名称|类型|是否必填|说明
---|---|---|---
picking_no|String|Y|拣货单号
code|String|Y|产品/商品编号
name|String|Y|名称
is_product|int|Y|是否产品。0：否；1：是
is_gift|int|Y|是否赠品。0：否；1：是
qty|int|Y|数量

样例报文：

	{
	    'picking_no':'00010101',
	    'picking_qty':10,
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0,
	    'details':[{
	        'picking_no':'shipment001',
	        'code':'goods001',
	        'name':'商品1'
	        'is_product':1,
	        'is_gift':0,
	        'qty':10
	    }]
	}

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipments query error.’}

----
#####12.批量查询拣货单接口
该接口用于批量查询拣货单
######4.1 url
	method: POST
	wms/outbound/picking_orders/
	注意：结尾的’/’不能省略
######4.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######4.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
month|Int|Y|查询月份

样例报文：

{
	'pageSize':8,
	'pageNo':1,
	'month':3
}

######4.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
---|---|---|---
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<Records-Item>

名称|类型|是否必填|说明
---|---|---|---
picking_no|String|Y|拣货单号
picking_qty|Int|Y|拣货总数量
status|Int|Y|拣货单状态。0：未拣货；1：拣货中；2：拣货完成
details|Array|Y|拣货单明细
creator|String|Y|创建人
create_time|String|Y|创建时间
updater|String|更新人
update_time|String|Y|更新时间

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	'records':[{
	    'picking_no':'00010101',
	    'picking_qty':10,
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0
		}......]
	}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}

----
#####13.按订单号查询出库单信息
按给定的订单号查询对应的出库单信息
######13.1 url
	method: GET
	wms/outbound/picking_orders/${picking_no}/
	注意：结尾的’/’不能省略, ${picking_no}为出库单号
######13.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######13.3 请求参数

样例报文：
无

######9.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
---|---|---|---
picking_no|String|Y|拣货单号
picking_qty|Int|Y|拣货总数量
status|Int|Y|拣货单状态
details|Array|Y|拣货单明细
creator|String|Y|创建人
create_time|String|Y|创建时间
updater|String|更新人
update_time|String|Y|更新时间

<拣货单明细>

名称|类型|是否必填|说明
---|---|---|---
picking_no|String|Y|拣货单号
code|String|Y|产品/商品编号
name|String|Y|名称
is_product|int|Y|是否产品。0：否；1：是
is_gift|int|Y|是否赠品。0：否；1：是
qty|int|Y|数量

样例报文：

	{
	    'picking_no':'00010101',
	    'picking_qty':10,
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0,
	    'details':[{
	        'picking_no':'shipment001',
	        'code':'goods001',
	        'name':'商品1'
	        'is_product':1,
	        'is_gift':0,
	        'qty':10
	    }]
	}

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipments query error.’}

----
#####14.按订单号查询出库单信息
按给定的订单号查询对应的出库单信息
######14.1 url
	method: POST
	wms/outbound/shipments/modify_by_orders/${orders_no}/
	注意：结尾的’/’不能省略, ${orders_no}为出库单号
######14.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######14.3 请求参数

名称|类型|是否必填|说明
---|---|---|---
address|String|Y|客户地址
customer_tel|String|Y|客户电话
updater|String|Y|修改人

样例报文：

	{
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'updater':'admin'
	}

######14.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipments query error.’}


----
#####15.合并出库单
按照给定的出库单号合并出库单，待合并的出库单状态为“为审核状态”。如果给定的出库单号包含其它状态则系统自动过滤。
合并后的出库单发货日期以原出库单中最早发货时间为准。
######15.1 url
	method: POST
	wms/outbound/shipment/merge/
	注意：结尾的’/’不能省略
######15.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######15.3 请求参数

名称|类型|是否必填|说明
---|---|---|---
shipment_nos|Array|Y|出库单号列表
updater|String|Y|修改人

样例报文：

	{
	    'shipment_nos':['0001','0002'],
	    'updater':'admin'
	}

######15.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipments query error.’}
	


----
#####16.上传快递单接口
该接口用于向快递公司上传发货单信息，后去发货单号与大头笔信息
######16.1 url
	method: POST
	wms/outbound/request_express_info/
	注意：结尾的’/’不能省略
######16.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######16.3 请求参数
名称|类型|是否必填|说明
---|---|---|---
shipment_no|String|Y|发货单号
updater|String|Y|需改人

样例报文：
	{
		'shipment_no':'S00001',
	    'updater':'admin'
	}

######16.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

名称|类型|是否必填|说明
---|---|---|---
express_orderno|String|Y|快递单号

样例报文：
	{
		'express_orderno':'S00001'
	}

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}

----
#####17.批量出库复合接口
按照给定的出库单号批量复合出库单，出库单状态为“未审核状态”。如果给定的出库单号包含其它状态则系统自动过滤。
######17.1 url
	method: POST
	wms/outbound/shipments/check/
	注意：结尾的’/’不能省略
######17.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######17.3 请求参数

名称|类型|是否必填|说明
---|---|---|---
shipment_nos|Array|Y|出库单号列表
updater|String|Y|修改人

样例报文：

	{
	    'shipment_nos':['0001','0002'],
	    'updater':'admin'
	}

######17.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Check shipments error.’}

----
#####18 查询待打印出库单接口
查询当前需要打印的出库单接口
######18.1 url
	method: GET
	wms/outbound/shipments/print/
	注意：结尾的’/’不能省略
######18.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######18.3 请求参数

无

######18.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

响应报文为出库单列表数组，数组项如下：

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
express_code|String|Y|快递公司编号
express_orders_no|String|Y|快递单号
express_name|String|Y|快递公司名称
express_cost|decimal|Y|快递费用
courier|String|Y|快递员
courier_tel|String|Y|快递员电话
sent_date|String|Y|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货
details|array|Y|发货明细

`Details`

名称|类型|是否必填|说明
---|---|---|---
shipment_no|String|Y|出库单号
code|String|Y|编号
name|String|Y|名称
is_product|int|Y|是否产品。0：否；1：是
is_gift|int|Y|是否赠品。0：否；1：是
qty|int|Y|数量
status|int|Y|状态。0：未确认；1：已确认


样例报文：

	[{
	    'orders_no':'00010101',
	    'shipment_no':'shipment0001',
	    'customer_code':'user001',
	    'customer_name':'user1',
	    'address':'北京天安门',
	    'customer_tel':'18600000000',
	    'amount':110.11,
	    'shipped_qty':10,
	    'has_invoice':0,
	    'express_code':'express0001',
        'express_orders_no':'010101010',
        'express_name':'顺丰',
        'express_cost':22:00,
        'courier':'aaaa',
        'courier_tel':18700000000,
        'sent_date':'2015-01-01',
	    'create_time':'2015-01-01T00:00:00',
	    'creator':'admin',
	    'update_time':'2015-01-01T00:00:00',
	    'updater':'admin',
	    'status':0,
	    'details':[{
	        'shipment_no':'shipment001',
	        'code':'goods001',
	        'name':'商品1'
	        'is_product':1,
	        'is_gift':0,
	        'qty':10,
	        status:0
	    }]
	},...]
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipment query error.’}
	

----
#####19 同步发货单接口
查询当前需要打印的出库单接口
######19.1 url
	method: GET
	wms/outbound/shipments/sync/
	注意：结尾的’/’不能省略
######19.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######19.3 请求参数

名称|类型|是否必填|说明
---|---|---|---
agent_code|string|N|代理商编号
begin_date|string|Y|发货开始日期，格式：YYYY-MM-DD
end_date|string|Y|发货结束日期,格式：YYYY-MM-DD
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号

样例：
wms/outbound/shipments/sync/?agent_code=101010&begin_date=2015-01-01&end_date=2015-01-31

######19.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
---|---|---|---
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<records-object>

名称|类型|是否必填|说明
---|---|---|---
orders_no|String|Y|订单号
shipment_no|String|Y|发货单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
source|int|Y|订单来源。
agent_code|String|Y|代理商编号
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
shipped_qty|int|Y|发货数量
has_invoice|int|Y|是否有发票。0：无；1：有
express_code|String|Y|快递公司编号
express_orders_no|String|Y|快递单号
express_name|String|Y|快递公司名称
express_cost|decimal|Y|快递费用
courier|String|Y|快递员
courier_tel|String|Y|快递员电话
sent_date|String|Y|发货时间
create_time|String|Y|创建时间
creator|String|Y|创建人
update_time|String|Y|修改时间
updater|String|Y|需改人
status|int|Y|发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货



样例报文：

	{'pageSize':8,
    	'pageNo':1,
    	'recordsCount':15,
    	'pageNumber':2,
    	'records':[{
    	    'orders_no':'00010101',
    	    'shipment_no':'shipment0001',
    	    'customer_code':'user001',
    	    'customer_name':'user1',
    	    'address':'北京天安门',
    	    'customer_tel':'18600000000',
    	    'amount':110.11,
    	    'shipped_qty':10,
    	    'has_invoice':0,
    	    'create_time':'2015-01-01T00:00:00',
    	    'creator':'admin',
    	    'update_time':'2015-01-01T00:00:00',
    	    'updater':'admin',
    	    'status':0
    		}......]
    }
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Shipment query error.’}