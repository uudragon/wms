####商品与产品定义接口说明

##### 索引

- [商品定义接口](https://github.com/uudragon/wms/blob/master/README.md#11-url)
- [产品定义接口](https://github.com/uudragon/wms/blob/master/README.md#21-url)
- [商品查询接口](https://github.com/uudragon/wms/blob/master/README.md#31-url)
- [产品查询接口](https://github.com/uudragon/wms/blob/master/README.md#41-url)
- [商品批量查询接口](https://github.com/uudragon/wms/blob/master/README.md#51-url)
- [产品批量查询接口](https://github.com/uudragon/wms/blob/master/README.md#61-url)

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
