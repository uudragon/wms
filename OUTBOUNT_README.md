#####目录
- [订单拆分接口](#11-url)
- [按出库单号查询出库单接口](#21-url)
- [修改出库单接口](#31-url)
- [批量查询出库单接口](#41-url)

----
#####1.订单拆分接口
接收客服系统发送的订单信息，按照一定规则将其拆分成发货单并返回将发货单信息返回给客服系统
######1.1 url
	method: POST
	outbound/split/
	注意：结尾的’/’不能省略
######1.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######1.3 请求参数
名称|类型|是否必填|说明
-|-|-|-
orders_no|String|Y|订单号
customer_code|String|Y|客户编号
customer_name|String|Y|客户姓名
effective_date|date|Y|生效日期
address|String|Y|客户地址
customer_tel|String|Y|客户电话
amount|decimal|Y|付款金额
has_invoice|int|Y|是否有发票。0：无；1：有
creator|String|Y|创建人
updater|String|Y|需改人
details|array|Y|订单明细

Details

名称|类型|是否必填|说明
-|-|-|-
product_code|String|Y|产品编号

样例报文：

	{'orders_no':'001010101',
	'customer_code':'user001',
	'customer_name':'yonghu1',
	'effective_date':'2014-012-31T00:00:00',
	'address':'北京市天安门',
	'customer_tel':'18600000000',
	'amount':110.11,
	'has_invoice':0,
	'creator':'admin',
	'updater':'admin',
	'details':[{
	    'product_code':'product001'
	 }]}

######1.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

发货单列表

名称|类型|是否必填|说明
-|-|-|-
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
update_time|String|修改时间
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

	{‘error’:’Orders split error.’}

----
#####2.按出库单号查询出库单信息
按给定的出库单号查询对应的出库单信息
######2.1 url
	method: GET
	outbound/shipment/${shipment_no}/
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
-|-|-|-
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

Details
名称|类型|是否必填|说明
-|-|-|-
shipment_no|String|Y|出库单号
goods_code|String|Y|商品编号
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
	        'goods_code':'goods001',
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
	outbound/shipment/save/
	注意：结尾的’/’不能省略
######3.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######3.3 请求参数
名称|类型|是否必填|说明
-|-|-|-
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

Details
名称|类型|是否必填|说明
-|-|-|-
shipment_no|String|Y|出库单号
goods_code|String|Y|商品编号
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
	        'goods_code':'goods001',
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
	inner/shipments/
	注意：结尾的’/’不能省略
######4.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######4.3 请求参数
无

样例报文：

暂略

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
