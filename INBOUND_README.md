#####目录
- [在库预拣货接口](#11-url)
- [在库商品查询](#21-url)
- [在库预拣货产品查询](#31-url)
- [库房出入库记录查询](#41-url)

----
#####1.在库预拣货接口
按照给定的库房号与产品号信息，指定库房内对应产品进行预拣货。
######1.1 url
	method: POST
	inner/${warehouse_code}/picking/
	注意：结尾的’/’不能省略,${warehouse_code}为仓库号
######1.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######1.3 请求参数
名称|类型|是否必填|说明
-|-|-|-
product_code|String|Y|产品号
updater|String|Y|修改人

样例报文：

	{'product_code':'product0001',
	'updater':'uudragon'}

######1.4 响应报文
成功响应：

	HTTP_STATUS_CODE:200

响应报文说明：

	
名称 | 类型 | 是否必填 | 说明
------------ | ------------- | ------------ | --------------
picking_qty|int|Y|当前完成预拣货数量

样例报文：

	{'picking_qty':15}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}

#####2.在库商品查询
按照给定的库房号查询对应库房中存在的商品信息
######2.1 url
	method: POST
	inner/${warehouse_code}/goods/
	注意：结尾的’/’不能省略,${warehouse_code}为仓库号
######2.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######2.3 请求参数
名称|类型|是否必填|说明
-|-|-|-
goods_code|String|O(可选)|商品编码

样例报文：

	{'goods_code':'goods0001'}

######2.4 响应报文
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
warehouse|String|Y|库房编码
warehouse_name|String|Y|库房名称
goods_code|String|Y|商品编码
goods_name|String|Y|商品名称
qty|int|Y|商品总数
not_picking_qty|int|Y|为拣货商品数
picking_qty|int|Y|已预拣货数量
create_time|DateTime|Y|记录创建时间
creator|String|Y|记录创建人
update_time|DateTime|Y|记录修改时间
updater|String|Y|记录最后修改人

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	'records':[
		{‘warehouse’:’warehouse0001’,
		’warehouse_name’:’优优龙主库’,
		‘goods_code’:'goods001',
		'goods_name':'商品1'
		'qty':15,
		'not_picking_qty':7,
		'picking_qty':8,
		‘creator’:’aa’,
		'create_time':'2015-01-02T00:00:00'
		‘updater’:’aa’,
		'update_time':'2015-01-02T00:00:00'}
	...]}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}

#####3.在库预拣产品查询
按照给定的库房号查询对应库房中已经预拣货的产品记录
######3.1 url
	method: POST
	inner/${warehouse_code}/products/
	注意：结尾的’/’不能省略,${warehouse_code}为仓库号
######3.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######3.3 请求参数
名称|类型|是否必填|说明
-|-|-|-
product_code|String|O(可选)|产品编码

样例报文：

	{'product_code':'product0001'}

######3.4 响应报文
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
warehouse|String|Y|库房编码
warehouse_name|String|Y|库房名称
product_code|String|Y|产品编码
product_name|String|Y|产品名称
qty|int|Y|预拣产品总数
create_time|DateTime|Y|记录创建时间
creator|String|Y|记录创建人
update_time|DateTime|Y|记录修改时间
updater|String|Y|记录最后修改人

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	'records':[
		{‘warehouse’:’warehouse0001’,
		’warehouse_name’:’优优龙主库’,
		‘product_code’:'product001',
		'product_name':'产品1'
		'qty':15,
		‘creator’:’aa’,
		'create_time':'2015-01-02T00:00:00'
		‘updater’:’aa’,
		'update_time':'2015-01-02T00:00:00'}
	...]}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}
	
#####4.库房出入库记录查询
按照给定的库房号查询对应库房的出入库记录
######2.1 url
	method: POST
	inner/${warehouse_code}/records/
	注意：结尾的’/’不能省略,${warehouse_code}为仓库号
######2.2 header
	Content_Type:application/json;charset=utf-8
	Accept:application/json
######3 请求参数
名称|类型|是否必填|说明
-|-|-|-
goods_code|String|O(可选)|商品编码

样例报文：

	{'goods_code':'goods0001'}

######2.4 响应报文
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
warehouse|String|Y|库房编码
warehouse_name|String|Y|库房名称
goods_code|String|Y|商品编码
goods_name|String|Y|商品名称
qty|int|Y|商品数量
code|String|Y|单据号
type|int|Y|单据类型。1：一般入库；2：退货入库；3：调货入库；4：调货出库（在途）；5：一般出库
create_time|DateTime|Y|记录创建时间
creator|String|Y|记录创建人
update_time|DateTime|Y|记录修改时间
updater|String|Y|记录最后修改人

样例报文：

	{'pageSize':8,
	'pageNo':1,
	'recordsCount':15,
	'pageNumber':2,
	'records':[
		{‘warehouse’:’warehouse0001’,
		’warehouse_name’:’优优龙主库’,
		‘goods_code’:'goods001',
		'goods_name':'商品1'
		'qty':15,
		'type':1,
		‘creator’:’aa’,
		'create_time':'2015-01-02T00:00:00'
		‘updater’:’aa’,
		'update_time':'2015-01-02T00:00:00'}
	...]}
异常响应：

	a．	HTTP_STATUS_CODE:400 Bad request；
	b．	HTTP_STATUS_CODE:500 Server Error
	
异常报文：

名称 | 类型 | 说明
------------ | ------------- | ------------
error| String  | 错误信息

样例报文：

	{‘error’:’Warehouse query error.’}
