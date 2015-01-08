##### 索引

- [商品定义接口](#11-url)
- [产品定义接口](#21-url)
- [商品查询接口](#31-url)
- [产品查询接口](#41-url)
- [商品批量查询接口](#51-url)
- [产品批量查询接口](#61-url)
- [新建入库单接口](#71-url)
- [取消入库单接口](#81-url)
- [商品入库接口](#91-url)
- [批量查询入库单接口](#101-url)
- [按入库单号查询入库单接口](#111-url)
- [库房定义接口](#121-url)
- [库房列表查询](#131-url)
- [按库房号查询库房信息接口](#141-url)

####商品与产品定义接口说明
------

#####1.	商品定义接口
该结构可用于商品定义的创建与修改功能，当所传入的goods_code已经存在于数据库时，会按照传入的goods_code对已有数据进行更新；
否则按新纪录插入到数据表中
######1.1 url
	method: POST
	wms/baseinfo/goods_define/
	注意：结尾的’/’不能省略
######1.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######1.3 请求参数

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
goods_name | String  | Y | 商品名称
goods_code | String  | Y | 商品编码
goods_type|	int|Y|商品类型
goods_desc|String|N	|商品描述
goods_price|decimal|Y|价格
goods_unit|String|Y	|商品规格描述
isbn|String|N|ISBN
barcode|String|N|条码
product_date|datetime|Y	|生产日期
creator|String|Y|创建人
updater|String|Y|修改人
yn|Int|Y|是否失效。默认1。1有效；0失效

样例报文：

	{‘goods_code’:’book000001’,
	’goods_name’:’书1’,
	‘goods_type’:1,
	‘goods_desc’:’英语教材1’,
	‘goods_price’:100.00,
	‘goods_unit’:16*8,
	‘isbn’:’aaa-aaa-aaaa-aaaa’,
	‘barcode’:’091-13131-2233141324’,
	‘product_date’:’2014-12-22 10:00:00’,
	‘creator’:’aa’,
	‘updater’:’aa’,
	‘yn’:1}
######1.4 响应报文
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

	{‘error’:’Attribute[‘goods_code’] can not be none.’}
			
#####2.	产品定义接口
该接口用于产品定义的创建与更新。如果所传入的product_code已经在数据库中有对应记录，则按该product_code更新已有纪录；
否则，按新纪录进行创建。
注意：如果是update，则当前product_code关联的ProductDetails表中的商品记录会被删除，并按照新提交的数据重新插入到ProductDetails表中。
######2.1 url

	method：POST
	wms/baseinfo/product_define/
	注意：结尾的’/’不能省略

######2.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######2.3 请求参数
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | ----------
product_code|String	|Y	|产品码，唯一
product_name|String	|Y	|产品名称
product_desc|String|N|产品描述
details	|Array|	Y|产品明细，
creator|String|Y|创建人
updater|String|Y|修改人
yn|Int|Y|是否失效。默认1。1有效；0失效


名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | ------------
goods_code|String|Y	|商品编码,必填
qty|Int|Y|数量，非0
is_gift|Int|Y|是否赠品，1是；0不是。Default：0


样例报文：

	{‘product_code’:’P00001’,
 	’product_name’:’产品1’,
 	‘product_desc’:1,
 	‘details’:[{
		‘goods_code’:’book000001’,
		‘qty’:’100’,
		‘is_gift’:0
	}],
	‘creator’:’aa’,
 	‘updater’:’aa’,
	‘yn’:1}

######2.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

异常响应：

	a.	HTTP_STATUS_CODE:400 Bad request；
	b.	HTTP_STATUS_CODE:500 Server Error

异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Attribute[‘goods_code’] can not be none.’}

#####3.	商品查询接口
######3.1 url
	method：GET
	wms/baseinfo/query_goods/${goods_code}/
	注意：结尾的’/’不能省略, ${goods_code}为商品编号
######3.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######3.3 请求参数
无
######3.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
goods_name | String  | Y | 商品名称
goods_code | String  | Y | 商品编码
goods_type|	int|Y|商品类型
goods_desc|String|N	|商品描述
goods_price|decimal|Y|价格
goods_unit|String|Y	|商品规格描述
isbn|String|N|ISBN
barcode|String|N|条码
product_date|datetime|Y	|生产日期
creator|String|Y|创建人
create_time|datetime|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|修改时间，update时，永远显示当前时间
yn|Int|Y|是否失效。默认1。1有效；0失效

样例报文：

	{‘goods_code’:’book000001’,
	’goods_name’:’书1’,
	‘goods_type’:1,
	‘goods_desc’:’英语教材1’,
	‘goods_price’:100.00,
	‘goods_unit’:16*8,
	‘isbn’:’aaa-aaa-aaaa-aaaa’,
	‘barcode’:’091-13131-2233141324’,
	‘product_date’:’2014-12-22 10:00:00’,
	‘creator’:’aa’,
	‘create_time’:’ 2014-12-22 10:00:00’,
	‘updater’:’aa’,
	‘update_time’:’ 2014-12-22 10:00:00’,
	‘yn’:1}

异常响应：
	a.HTTP_STATUS_CODE:500 Server Error
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：
{‘error’:’Query goods [${goods_code}]  information error.’}

#####4.	产品查询接口
#######4.1 url
	method: GET
	wms/baseinfo/query_product /${product_code}/
	注意：结尾的’/’不能省略, ${product_code}为产品号
######4.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######4.3 请求参数
无
######4.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | ----------
product_code|String	|Y	|产品码，唯一
product_name|String	|Y	|产品名称
product_desc|String|N|产品描述
details	|Array|	Y|产品明细，
creator|String|Y|创建人
create_time|datetime|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|修改时间，update时，永远显示当前时间
yn|Int|Y|是否失效。默认1。1有效；0失效


名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | ------------
goods_code|String|Y	|商品编码,必填
qty|Int|Y|数量，非0
is_gift|Int|Y|是否赠品，1是；0不是。Default：0


样例报文：

	{‘product_code’:’P00001’,
 	’product_name’:’产品1’,
 	‘product_desc’:1,
 	‘details’:[{
		‘goods_code’:’book000001’,
		‘qty’:’100’,
		‘is_gift’:0
	}],
	‘creator’:’aa’,
 	‘create_time’:’ 2014-12-22 10:00:00’,
 	‘updater’:’aa’,
 	‘update_time’:’ 2014-12-22 10:00:00’,
	‘yn’:1}

异常响应：
	a.	HTTP_STATUS_CODE:500 Server Error
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：
{‘error’:’ Query goods [${product_code}]  information error..’}
#####5.	商品批量查询接口
######5.1 url
	method：POST
	wms/baseinfo/query_goods_list/
	注意：结尾的’/’不能省略
######5.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######5.3 请求参数
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
goods_name | String  | O(可选) | 商品名称
goods_code | String  | O(可选) | 商品编码
goods_type|	int|O(可选)|商品类型
yn|Int|O(可选)|是否失效。默认1。1有效；0失效
pageSize|Int|Y|每页显示记录数，默认8
pageNo|Int|Y|当前页号，默认1

样例报文：

	{‘goods_code’:’book000001’,
	’goods_name’:’书1’,
	‘goods_type’:1,
	‘yn’:1}
######5.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

名称|类型|是否必填|说明
--|--|--|--
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<Records-Item>

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
goods_name | String  | Y | 商品名称
goods_code | String  | Y | 商品编码
goods_type|	int|Y|商品类型
goods_desc|String|N	|商品描述
goods_price|decimal|Y|价格
goods_unit|String|Y	|商品规格描述
isbn|String|N|ISBN
barcode|String|N|条码
product_date|datetime|Y	|生产日期
creator|String|Y|创建人
create_time|datetime|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|修改时间，update时，永远显示当前时间
yn|Int|Y|是否失效。默认1。1有效；0失效

样例报文：

	[{‘goods_code’:’book000001’,
	’goods_name’:’书1’,
	‘goods_type’:1,
	‘goods_desc’:’英语教材1’,
	‘goods_price’:100.00,
	‘goods_unit’:16*8,
	‘isbn’:’aaa-aaa-aaaa-aaaa’,
	‘barcode’:’091-13131-2233141324’,
	‘product_date’:’2014-12-22 10:00:00’,
	‘creator’:’aa’,
	‘create_time’:’ 2014-12-22 10:00:00’,
	‘updater’:’aa’,
	‘update_time’:’ 2014-12-22 10:00:00’,
	‘yn’:1},...]

异常响应：
	a.HTTP_STATUS_CODE:500 Server Error
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：
{‘error’:’Query goods [${goods_code}]  information error.’}

#####6.	产品批量查询接口
######6.1 url
	method：POST
	wms/baseinfo/query_product_list/
	注意：结尾的’/’不能省略
######6.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######6.3 请求参数
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
product_name | String  | O(可选) | 产品名称
product_code | String  | O(可选) | 产品编码
yn|Int|O(可选)|是否失效。默认1。1有效；0失效
pageSize|Int|Y|每页显示记录数，默认8
pageNo|Int|Y|当前页号，默认1

样例报文：

	{‘product_code’:’book000001’,
	’product_name’:’书1’,
	'pageSize':8,
	'pageNo':1,
	‘yn’:1}
######6.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

名称|类型|是否必填|说明
--|--|--|--
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<Records-Item>

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
product_name | String  | Y | 产品名称
product_code | String  | Y | 产品编码
creator|String|Y|创建人
create_time|datetime|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|修改时间，update时，永远显示当前时间
yn|Int|Y|是否失效。默认1。1有效；0失效

样例报文：

	[{‘product_code’:’book000001’,
	’product_name’:’书1’,
	‘creator’:’aa’,
	‘create_time’:’ 2014-12-22 10:00:00’,
	‘updater’:’aa’,
	‘update_time’:’ 2014-12-22 10:00:00’,
	‘yn’:1},...]

异常响应：
	a.HTTP_STATUS_CODE:500 Server Error
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：
{‘error’:’Query goods [${goods_code}]  information error.’}




####入库接口
----

#####7.新建入库单接口
该接口可用于在数据库中新建入库单数据。新建的入库单状态为“未入库（0）”。<br>新建的入库单可以被“取消”或者进行“入库操作”。
######7.1 url
	method: POST
	wms/inbound/receipt/create/
	注意：结尾的’/’不能省略
######7.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######1.3 请求参数

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
receipt_code | String  | Y | 入库单编号名称
receipt_desc|	int|Y|入库单描述
warehouse|String|Y	|库房编号
details|array|Y|入库单明细
creator|String|Y|创建人
updater|String|Y|修改人

<ReceiptDetails>

名称|类型|是否必填|说明
-|-|-|-
goods_code|String|Y|商品编码
qty|int|Y|商品数量，预入库数量


样例报文：

	{‘receipt_code’:’receipt0001’,
	’receipt_desc’:’入库单1’,
	‘warehouse’:'1',
	'details':[
		{'goods_code':'goods001',
		'qty':100}
	]
	‘creator’:’aa’,
	‘updater’:’aa’}
######7.4 响应报文
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

	{‘error’:’Receipt information saved error.’}

#####8.取消入库单接口
该接口用于将传入的入库单号（${receipt_code}）对应的入库单信息标记成“取消（-1）”状态。<br>注意：如果调用此接口，则入库单
信息将不能再被编辑。
######8.1 url
	method: GET
	wms/inbound/receipt/${receipt_code}/cancel/
	注意：结尾的’/’不能省略, ${receipt_code}为入库单编号
######8.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######8.3 请求参数

无

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

	{‘error’:’Receipt information cancel error.’}

#####9.商品入库接口
该接口用于商品入库。
######9.1 url
	method: POST
	wms/inbound/putin/
	注意：结尾的’/’不能省略
######9.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######9.3 请求参数

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
receipt_code | String  | Y | 入库单编号名称
warehouse|String|Y	|库房编号
details|array|Y|入库商品信息明细
updater|String|Y|修改人


名称|类型|是否必填|说明
-|-|-|-
goods_code|String|Y|商品编号
putin_qty|int|Y|入库数量


样例报文：

	{‘receipt_code’:’receipt0001’,
	‘warehouse’:'1',
	'details':[
		{'goods_code':'goods001',
		'putin_qty':10}
	]
	‘updater’:’aa’}
######9.4 响应报文
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

	{‘error’:’Goods Putin error.’}

#####10.批量查询入库单接口
按条件批量查询入库单接口。可用于按给定条件查询当前入库单表中的信息。
######10.1 url
	method: POST
	wms/inbound/receipts/
	注意：结尾的’/’不能省略
######10.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######10.3 请求参数

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
receipt_code | String  | O(可选) | 入库单编号名称
status|int|O(可选)|入库单状态
creator|String|O(可选)|创建人
updater|String|O(可选)|修改人

样例报文：

	{‘receipt_code’:’receipt0001’,
	’status’:2,
	‘creator’:’aa’,
	‘updater’:’aa’}
######10.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
--|--|--|--
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<Records-Item>
	
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
receipt_code | String  | Y | 入库单编号名称
receipt_desc|	int|Y|入库单描述
warehouse|String|Y	|库房编号
status|int|Y|入库单状态。-1：撤销；0：未入库；1：部分入库；2：入库完成
creator|String|Y|创建人
create_time|datetime|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|更新时间

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	records:[
		{'receipt_code':'receipt0001',
		'receipt_desc':'入库单1',
		'warehouse':1,
		'status':2,
		'creator':'aa',
		'create_time':'2015-01-05T00:00:00',
		'updater':'aa',
		'create_time':'2015-01-05T00:00:00'}
	...]}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Receipt list query error.’}

#####11.按入库单号查询入库单信息
按给定的入库单号查询对应入库单信息。如果入库单状态不是“未入库（0）”，则不能对该入库单做任何的修改操作。
######11.1 url
	method: POST
	wms/inbound/receipt/${receipt_code}/
	注意：结尾的’/’不能省略,${receipt_code}为入库单号
######11.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######11.3 请求参数

无
######11.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

	
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
receipt_code | String  | Y | 入库单编号名称
receipt_date|String|Y|入库单时间
receipt_desc|	int|Y|入库单描述
warehouse|String|Y	|库房编号
status|int|Y|入库单状态。-1：撤销；0：未入库；1：部分入库；2：入库完成
details|array|Y|入库单明细
creator|String|Y|创建人
create_time|datetime|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|更新时间

<ReceiptDetails>

名称|类型|是否必填|说明
-|-|-|-
id|String|Y|主键
receipt_code|String|Y|入库单号
goods_code|String|Y|商品号
qty|int|Y|入库数量
actual_qty|int|Y|当期实际入库数量
status|int|Y|当前入库状态。0：未入库；1：预入库；2：入库完成
creator|String|Y|创建人
create_time|datetime|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|更新时间

样例报文：

	{'receipt_code':'receipt0001',
		'receipt_date':'2015-01-06T00:00:00',
		'receipt_desc':'入库单1',
		'warehouse':1,
		'status':2,
		'creator':'aa',
		'create_time':'2015-01-05T00:00:00',
		'updater':'aa',
		'create_time':'2015-01-05T00:00:00',
		'details':[
			{'id':'receipt001goods001',
			'receipt_code':'receipt001',
			'goods_code':'goods001',
			'qty':10,
			'actual_qty':5,
			'status':1,
			'create_time':'2015-01-05T00:00:00',
			'updater':'aa',
			'create_time':'2015-01-05T00:00:00'}
		]
	}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Receipt list query error.’}

####库房管理
----
#####12.保存库房信息
该接口用于用户定义的库房信息。
######12.1 url
	method: POST
	wms/baseinfo/warehouse/save/
	注意：结尾的’/’不能省略
######12.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######12.3 请求参数

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
warehouse_code | String  | Y | 库房编号
warehouse_name|	int|Y|库房名称
address|String|Y|库房地址
type|int|Y|库房类型。1：主库；2：备库。默认1
creator|String|Y|创建人
updater|String|Y|修改人
yn|INT|Y|是否生效。1生效；0失效。默认1

样例报文：

	{‘warehouse_code’:’warehouse0001’,
	’warehouse_name’:’优优龙主库’,
	‘address’:'北京马驹桥',
	'type':1,
	‘creator’:’aa’,
	‘updater’:’aa’,
	'yn':1}
######12.4 响应报文
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

	{‘error’:’Warehouse saved error.’}

#####13.批量查询入库单接口
按条件批量查询库房信息接口。可用于按给定条件查询当前库房信息信息。
######13.1 url
	method: POST
	wms/baseinfo/warehouses/
	注意：结尾的’/’不能省略
######13.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######13.3 请求参数

名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
warehouse_code | String  | O(可选) | 库房编号
yn|INT|O(可选)|是否有效。1有效；0失效
creator|String|O(可选)|创建人
updater|String|O(可选)|修改人

样例报文：

	{‘warehouse_code’:’warehouse0001’,
	’yn’:1,
	‘creator’:’aa’,
	‘updater’:’aa’}
######13.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

名称|类型|是否必填|说明
--|--|--|--
pageSize|Int|Y|每页显示记录数
pageNo|Int|Y|当前页号
recordsCount|Int|Y|总记录数
pageNumber|Int|Y|总页数
records|Array|N|当前页记录

<Records-Item>
	
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
warehouse_code | String  | Y | 库房编号
warehouse_name|String|Y|库房名称
address|int|Y|库房地址
type|INT|Y|库房类型。1：主库；2：备库
creator|String|Y|创建人
create_time|array|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|修改时间
yn|INT|Y|是否生效

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	'records':[
		{‘warehouse_code’:’warehouse0001’,
		’warehouse_name’:’优优龙主库’,
		‘address’:'北京马驹桥',
		'type':1,
		‘creator’:’aa’,
		‘updater’:’aa’,
		'yn':1}
	...]}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse list query error.’}

	
#####14.按入库单号查询入库单信息
按给定的库房号查询对应库房信息。
######14.1 url
	method: GET
	wms/baseinfo/warehouse/${warehouse_code}/
	注意：结尾的’/’不能省略,${warehouse_code}为仓库号
######14.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######14.3 请求参数

无
######14.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

	
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
warehouse_code | String  | Y | 库房编号
warehouse_name|String|Y|库房名称
address|int|Y|库房地址
type|INT|Y|库房类型。1：主库；2：备库
creator|String|Y|创建人
create_time|array|Y|创建时间
updater|String|Y|修改人
update_time|datetime|Y|修改时间
yn|INT|Y|是否生效

样例报文：

	{‘warehouse_code’:’warehouse0001’,
	’warehouse_name’:’优优龙主库’,
	‘address’:'北京马驹桥',
	'type':1,
	‘creator’:’aa’,
	‘updater’:’aa’,
	'yn':1}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}