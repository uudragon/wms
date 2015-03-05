CREATE DATABASE IF NOT EXISTS `WMS`;

GRANT ALL PRIVILEGES ON `WMS`.* TO 'wms_admin'@'%' identified by 'wms_admin';
GRANT SELECT, UPDATE, INSERT, DELETE ON `WMS`.* TO 'wms_rw'@'%' identified by 'wms_rw';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS `T_GOODS_GROUP`(
  `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  GROUP_CODE VARCHAR(36) NOT NULL COMMENT '商品组编号',
  GROUP_NAME VARCHAR(255) NOT NULL COMMENT '商品组名称',
  GROUP_DESC VARCHAR(255) NOT NULL COMMENT '商品组描述',

  PRIMARY KEY(ID),
  UNIQUE KEY `UK_GROUP` (`GROUP_CODE`)
)
ENGINE=InnoDB
COMMENT='商品组信息表';

CREATE TABLE IF NOT EXISTS `T_PRODUCT_PACKAGE`(
  `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `PACKAGE_CODE` VARCHAR(50) NOT NULL COMMENT '套餐编号',
  `PACKAGE_NAME` VARCHAR(100) NOT NULL COMMENT '套餐名称',
  `PACKAGE_DESC` VARCHAR(255) COMMENT '套餐说明',
  `PACKAGE_TYPE` int(4) NOT NULL COMMENT '套餐类型。1：官网套餐；2：代理商套餐；3：其它套餐' DEFAULT 1,
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '经手人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '更新时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',
  `YN` tinyint(4) NOT NULL COMMENT '是否有效（0:有效;1:无效）',
  
  PRIMARY KEY (`ID`),
  UNIQUE KEY `UK_PACKAGE` (`PACKAGE_CODE`)
)
ENGINE=InnoDB
COMMENT='套餐信息表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_PRODUCT_PACKAGE_DETAILS` (
  `ID` VARCHAR(72) NOT NULL COMMENT 'ID',
  `PRODUCT_CODE`  VARCHAR(36)  NOT NULL COMMENT '产品编号，非空',
  `PACKAGE_CODE`  VARCHAR(36)  NOT NULL COMMENT '套餐编号，非空',
  `QTY`  INT NOT NULL COMMENT '数量，非空',

  PRIMARY KEY (`ID`)
)
ENGINE = InnoDB
COMMENT = '套餐明细表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_PRODUCT_PACKAGE_GIFTS` (
  `ID` VARCHAR(72) NOT NULL COMMENT 'ID',
  `GOODS_CODE`  VARCHAR(36)  NOT NULL COMMENT '商品编号，非空',
  `PACKAGE_CODE`  VARCHAR(36)  NOT NULL COMMENT '套餐编号，非空',
  `QTY`  INT NOT NULL COMMENT '数量，非空',

  PRIMARY KEY (`ID`)
)
ENGINE = InnoDB
COMMENT = '套餐赠品表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_PRODUCT` (
  `ID` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `PRODUCT_CODE`  VARCHAR(32)  NOT NULL COMMENT '产品编号',
  `PRODUCT_NAME`  VARCHAR(200) NOT NULL COMMENT '产品名称，非空',
  `PRODUCT_DESC`  VARCHAR(500) COMMENT '产品说明',
  `PRODUCT_LEVEL` INT(11) NOT NULL COMMENT '产品阶数' DEFAULT 1,
  `CREATE_TIME` TIMESTAMP NOT NULL  COMMENT '创建时间，非空',
  `CREATOR` VARCHAR(32) COMMENT '创建人',
  `UPDATE_TIME` TIMESTAMP  COMMENT '更新时间',
  `UPDATER` VARCHAR(32)  COMMENT '更新人',
  `YN`  TINYINT(1)  NOT NULL COMMENT '是否有效（0：有效；1：无效）',

  PRIMARY KEY (`ID`),
  UNIQUE INDEX `PRODUCT_CODE_UNIQUE` (`PRODUCT_CODE` ASC)
  )
ENGINE = InnoDB
COMMENT = '产品表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_PRODUCT_DETAILS` (
  `ID` VARCHAR(72) NOT NULL COMMENT 'ID',
  `PRODUCT_CODE`  VARCHAR(32)  NOT NULL COMMENT '产品编号，非空',
  `GOODS_CODE`  VARCHAR(32)  NOT NULL COMMENT '商品编号，非空', 
  `GOODS_NAME`  VARCHAR(255) NOT NULL COMMENT '商品名称，非空',
  `GOODS_QTY`  INT NOT NULL COMMENT '商品数量，非空',
  `IS_GIFT` TINYINT(1) NOT NULL COMMENT '是否赠品 0：否；1：是',

  PRIMARY KEY (`ID`)
)
ENGINE = InnoDB
COMMENT = '产品明细表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_WAREHOUSE` (
  `ID` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `CODE` VARCHAR(100) NOT NULL COMMENT '库房编号',
  `NAME` VARCHAR(255) COMMENT '库房名称',
  `ADDRESS` VARCHAR(255) COMMENT '库房地址',
  `TYPE` TINYINT(4) COMMENT '库房类型1:主库2：备库' DEFAULT 1,
  `CREATE_TIME` TIMESTAMP NOT NULL  COMMENT '创建时间，非空',
  `CREATOR` VARCHAR(32) COMMENT '创建人',
  `UPDATE_TIME` TIMESTAMP  COMMENT '更新时间',
  `UPDATER` VARCHAR(32)  COMMENT '更新人',
  `YN` TINYINT(1) COMMENT '是否有效。0有效，1失效。default:0' DEFAULT 0,

  PRIMARY KEY (`ID`),
  UNIQUE INDEX `WAREHOUSE_CODE_UNIQUE` (`CODE` ASC)
)
ENGINE = InnoDB
COMMENT = '库房信息表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_STORAGE_RECORD` (
  `ID` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `GOODS_CODE`  VARCHAR(32)  NOT NULL COMMENT '商品编号',
  `GOODS_QTY`  INT NOT NULL COMMENT '商品数量，非空',
  `CODE` VARCHAR(50) NOT NULL COMMENT '单号',
  `WAREHOUSE`  VARCHAR(32)  NOT NULL COMMENT '所在库房编号',
  `TYPE` TINYINT NOT NULL COMMENT '类型 1：一般入库；2：退货入库；3：调货入库；4：调货出库（在途）；5：一般出库',
  `CREATE_TIME` TIMESTAMP NOT NULL  COMMENT '创建时间，非空',
    `CREATOR` VARCHAR(32) NOT NULL COMMENT '创建人',
    `UPDATE_TIME` TIMESTAMP NOT NULL COMMENT '更新时间',
    `UPDATER` VARCHAR(32) NOT NULL COMMENT '更新人',
    `STATUS` INT(4) NOT NULL DEFAULT 1 COMMENT '状态。默认1。0：预占；1：完成',

  PRIMARY KEY (`ID`)
 )
ENGINE = InnoDB
COMMENT = '商品出入库记录表';


CREATE TABLE IF NOT EXISTS `WMS`.`T_RECEIPT` (
  `ID` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `CODE` VARCHAR(50) NOT NULL COMMENT '入库单号',
  `RECEIPT_DATE` TIMESTAMP COMMENT '入库单时间', 
  `RECEIPT_DESC` VARCHAR(255) COMMENT '入库描述', 
  `STATUS` TINYINT COMMENT '入库单状态 -1:取消； 0：未入库；1：部分入库；2：入库完成；' , 
  `WAREHOUSE`  VARCHAR(32)  NOT NULL COMMENT '所在库房编号',
  `CREATE_TIME` TIMESTAMP NOT NULL COMMENT '创建时间',
  `CREATOR` VARCHAR(50) NOT NULL COMMENT '创建人',
  `UPDATE_TIME` TIMESTAMP NOT NULL COMMENT '更新时间',
  `UPDATER` VARCHAR(32) NOT NULL COMMENT '更新人',

  PRIMARY KEY (`ID`),
  UNIQUE KEY `UK_CODE` (`CODE`)
 )
ENGINE = InnoDB
COMMENT = '商品入库单表';


CREATE TABLE IF NOT EXISTS `WMS`.`T_RECEIPT_DETAILS` (
  `ID` VARCHAR(100) NOT NULL COMMENT 'ID',
  `CODE` VARCHAR(50) NOT NULL COMMENT '入库单号',
  `GOODS_CODE`  VARCHAR(32)  NOT NULL COMMENT '商品编号',
  `GOODS_QTY`  INT NOT NULL COMMENT '商品数量，非空' DEFAULT 0,
  `ACTUAL_QTY` INT NOT NULL COMMENT '实际商品数量，非空' DEFAULT 0,
  `STATUS` INT NOT NULL COMMENT '状态：-1：取消；0：未入库；1：预入库；2：入库完成',
  `CREATE_TIME` TIMESTAMP NOT NULL COMMENT '创建时间',
  `CREATOR` VARCHAR(50) NOT NULL COMMENT '创建人',
  `UPDATE_TIME` TIMESTAMP NOT NULL COMMENT '更新时间',
  `UPDATER` VARCHAR(32) NOT NULL  COMMENT '更新人',

  PRIMARY KEY (`ID`)
)
ENGINE = InnoDB
COMMENT = '商品入库单明细表';


CREATE TABLE IF NOT EXISTS `WMS`.`T_W_GOODS_DETAILS` (
  `ID` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `WAREHOUSE` VARCHAR(50) NOT NULL COMMENT '库房号',
  `GOODS_CODE` VARCHAR(32) NOT NULL COMMENT '商品号',
  `QTY` INT(11) NOT NULL COMMENT '商品数量' DEFAULT 0,
  `PICKING_QTY` INT(11) NOT NULL COMMENT '拣货数量' DEFAULT 0,
  `NOT_PICKING_QTY` INT(11) NOT NULL COMMENT '未拣货数量' DEFAULT 0,
  `CREATOR` VARCHAR(50) COMMENT '创建人',
  `CREATE_TIME` TIMESTAMP COMMENT '创建时间',
  `UPDATER` VARCHAR(50) COMMENT '修改人',
  `UPDATE_TIME` TIMESTAMP COMMENT '修改时间',

  PRIMARY KEY (`ID`)
 )
ENGINE = InnoDB
COMMENT = '库房商品明细表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_W_PRODUCT_DETAILS`(
  `ID` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `WAREHOUSE` VARCHAR(50) NOT NULL COMMENT '库房号',
  `PRODUCT_CODE`  VARCHAR(32)  NOT NULL COMMENT '产品编号，非空',
  `EFFECTIVE_QTY` INT(11) NOT NULL COMMENT '有效数量' DEFAULT 0,
  `CREATOR` VARCHAR(50) COMMENT '创建人',
  `CREATE_TIME` TIMESTAMP COMMENT '创建时间',
  `UPDATER` VARCHAR(50) COMMENT '修改人',
  `UPDATE_TIME` TIMESTAMP COMMENT '修改时间',

  PRIMARY KEY (`ID`)
)
ENGINE = InnoDB
COMMENT = '库房产品明细表';


CREATE TABLE IF NOT EXISTS `WMS`.`T_GOODS` (
  `ID` BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `GOODS_TYPE` TINYINT(4) COMMENT '商品类型。1：教材（书籍）；2.音像制品（DVD/CD）；3：玩具；4：其它',
  `GOODS_CODE`  VARCHAR(32)  NOT NULL COMMENT '商品编号，非空（ISBN/ISSN+yyyyMMdd）',
  `GOODS_NAME`  VARCHAR(200) NOT NULL COMMENT '商品名称，非空',
  `GOODS_GROUP` VARCHAR(36) NULL COMMENT '商品归属',
  `GOODS_PRICE` DECIMAL(20,2) COMMENT '商品价格',
  `GOODS_BULK`  DECIMAL(20,4) NOT NULL COMMENT '商品体积，非空' DEFAULT 0.0,
  `GOODS_WEIGHT`  DECIMAL(20,4) NOT NULL COMMENT '商品重量，非空' DEFAULT 0.0,
  `GOODS_UNIT`  VARCHAR(200) COMMENT '商品规格', 
  `BARCODE`  VARCHAR(50) COMMENT '商品条码',
  `ISBN`  VARCHAR(50) COMMENT 'ISBN号',
  `PRODUCT_DATE` DATE  COMDATEMENT '生产日期',  
  `GOODS_DESC` VARCHAR(200) COMMENT '商品描述',
  `CREATE_TIME` TIMESTAMP NOT NULL  COMMENT '创建时间，非空',
  `CREATOR` VARCHAR(32) COMMENT '创建人',
  `UPDATE_TIME` TIMESTAMP  COMMENT '更新时间',
  `UPDATER` VARCHAR(32)  COMMENT '更新人',
  `YN`  TINYINT(4)  NOT NULL COMMENT '是否有效（0：有效；1：无效）',

  PRIMARY KEY (`ID`),
  UNIQUE INDEX `GOODS_CODE_UNIQUE` (`GOODS_CODE` ASC)
  )
ENGINE = InnoDB
COMMENT = '商品表';


CREATE TABLE IF NOT EXISTS `WMS`.`T_SHIPMENT` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `ORDERS_NO` VARCHAR(36) NOT NULL COMMENT '订单号，非空',
  `SHIPMENT_NO` varchar(36) NOT NULL COMMENT '发货单号，非空',
  `PICKING_NO` VARCHAR(36) NULL COMMENT '拣货单号，业务逻辑非空',
  `SOURCE` INT(4) NOT NULL COMMENT '订单来源。1：网站；2：电话；3：代理商代下单',
  `WAREHOUSE` varchar(36) NOT NULL COMMENT '所在库房编号',
  `SHIPPED_QTY` int(11) DEFAULT NULL COMMENT '发货商品总数',
  `CUSTOMER_NO` VARCHAR(36) NOT NULL COMMENT '客户编号',
  `CUSTOMER_NAME` VARCHAR(100) NOT NULL COMMENT '客户姓名',
  `CUSTOMER_TEL` VARCHAR(50) NOT NULL COMMENT '电话',
  `ADDRESS` VARCHAR(255) NOT NULL COMMENT '客户地址',
  `HAS_INVOICE` INT NOT NULL COMMENT '是否有发票 0：无|1：有',
  `AMOUNT` DECIMAL(20, 2) NOT NULL COMMENT '付款金额' DEFAULT 0.00,
  `EXPRESS_CODE` varchar(50) NULL COMMENT '快递公司编号',
  `EXPRESS_ORDERS_NO` varchar(100) NULL COMMENT '快递单号，非空',
  `EXPRESS_NAME` varchar(100) DEFAULT NULL COMMENT '快递公司名称',
  `EXPRESS_COST` decimal(20,0) DEFAULT 0.00 COMMENT '快递费用',
  `SENT_DATE` DATE NULL COMMENT '发货时间',
  `COURIER` varchar(100) DEFAULT NULL COMMENT '快递员姓名',
  `COURIER_TEL` varchar(32) DEFAULT NULL COMMENT '快递员电话',
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '发货人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '修改时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',
  `STATUS` int(11) NOT NULL DEFAULT 0 COMMENT '发货单状态。-1：无效；0：待审核；1：待发货；2：备货中；3：发货中；4：已发货',

  PRIMARY KEY (`ID`),
  UNIQUE INDEX `SHIPMENT_NO_UNIQUE` (`SHIPMENT_NO`)
)
ENGINE=InnoDB 
COMMENT='发货信息表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_SHIPMENT_DETAILS` (
  `ID` VARCHAR(72) NOT NULL COMMENT 'ID',
  `SHIPMENT_NO` varchar(36) NOT NULL COMMENT '发货单号，非空',
  `CODE` varchar(36) NOT NULL COMMENT '编号，非空',
  `IS_PRODUCT` int(4) NOT NULL DEFAULT 1 COMMENT '是否产品。0：否；1：是',
  `IS_GIFT` int(4) NOT NULL DEFAULT 0 COMMENT '是否赠品。0：否；1：是',
  `QTY` int NOT NULL DEFAULT 1 COMMENT '数量',
  `STATUS` int NOT NULL DEFAULT 0 COMMENT '状态。0：未确认；1：已确认',
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '经手人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '更新时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',
  
  PRIMARY KEY (`ID`)
)
ENGINE=InnoDB 
COMMENT='发货明细表';

CREATE TABLE IF NOT EXISTS `WMS`.`T_GOODS_2R_RECORD` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `ORDER_NO` varchar(32) NOT NULL COMMENT '订单号，非空',
  `AGENT_CODE` varchar(32) COMMENT '代理商编号',
  `OPT_TYPE` tinyint(4) NOT NULL COMMENT '操作类型（1：退货；2：换货）',
  `GOODS_CODE` varchar(32) NOT NULL COMMENT '商品编号，非空',
  `GOODS_NAME` varchar(200) NOT NULL COMMENT '商品名称，非空',
  `GOODS_QTY` int NOT NULL DEFAULT 1,
  `SHIPMENT_NO` varchar(32) COMMENT '发货单号（记录换货后的发货单号）',
  `EXPRESS_ORDERS_NO` varchar(100) COMMENT '快递单号（记录换货后的快递单号）',
  `REASON` varchar(200) DEFAULT NULL COMMENT '原因',
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '经手人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '更新时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',
  `YN` tinyint(4) NOT NULL COMMENT '是否有效（0：有效；1：无效）',
  
  PRIMARY KEY (`ID`),
  INDEX `ORDER_NO` (`ORDER_NO`)
) 
ENGINE=InnoDB 
COMMENT='退换货记录表';

CREATE TABLE IF NOT EXISTS `WMS`.`ORDERS`(
  `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `ORDERS_NO` VARCHAR(32) NOT NULL COMMENT '订单号，非空',
  `CUSTOMER_CODE` VARCHAR(50) NOT NULL COMMENT '客户编号',
  `CUSTOMER_NAME` VARCHAR(255) NOT NULL COMMENT '客户姓名',
  `PHONE` VARCHAR(20) NOT NULL COMMENT '电话',
  `EFFECTIVE_DATE` DATE NOT NULL COMMENT '生效日期',
  `HAS_INVOICE` INT NOT NULL COMMENT '是否有发票 0：无|1：有',
  `AMOUNT` DECIMAL(20, 2) NOT NULL COMMENT '付款金额' DEFAULT 0.00,
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '经手人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',
  `STATUS` INT(11) NOT NULL COMMENT '订单状态 -1：异常；0：未付款；1：已付款；2：已发货',
  `yn` INT(11) NOT NULL COMMENT '是否生效，0：失效；1：生效',
  
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ORDERS_NO_UNIQUE` (`ORDERS_NO`)
)
ENGINE=InnoDB 
COMMENT='订单信息表';

CREATE TABLE IF NOT EXISTS `WMS`.`ORDERS_DETAILS`(
  ID VARCHAR(50) COMMENT 'ID',
  `ORDERS_NO` VARCHAR(32) NOT NULL COMMENT '订单号，非空',
  `PRODUCT_CODE` VARCHAR(32) NOT NULL COMMENT '产品编号',
  `STATUS` INT(11) NOT NULL COMMENT '状态 -1：异常；0：未发货；1：已发货',
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '经手人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',
  
  PRIMARY KEY(ID)
)
ENGINE=InnoDB
COMMENT='订单明细表';


CREATE TABLE IF NOT EXISTS `WMS`.`T_PICKING_ORDERS`(
  `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `PICKING_NO` VARCHAR(36) NOT NULL COMMENT '拣货单号',
  `PICKING_QTY` INT(11) NOT NULL COMMENT '拣货数量' default 0,
  `STATUS` INT(4) NOT NULL COMMENT '拣货单状态。0：未拣货，1：正在拣货；2：拣货完成' default 0,
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '经手人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '更新时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',
  
  PRIMARY KEY(ID),
  UNIQUE INDEX `PICKING_NO_UNIQUE` (`PICKING_NO`)
)
ENGINE=InnoDB
COMMENT='拣货单表';


CREATE TABLE IF NOT EXISTS `WMS`.`T_PICKING_ORDERS_DETAILS`(
  `ID` VARCHAR(72) NOT NULL COMMENT 'ID',
  `PICKING_NO` varchar(36) NOT NULL COMMENT '拣货单号，非空',
  `CODE` VARCHAR(36) NOT NULL COMMENT '产品或商品编号，非空',
  `IS_PRODUCT` int(4) NOT NULL DEFAULT 1 COMMENT '是否产品。0：否；1：是',
  `IS_GIFT` int(4) NOT NULL DEFAULT 0 COMMENT '是否赠品。0：否；1：是',
  `QTY` int NOT NULL DEFAULT 1 COMMENT '数量',
  `CREATE_TIME` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间，非空',
  `CREATOR` varchar(32) NOT NULL COMMENT '经手人',
  `UPDATE_TIME` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '更新时间',
  `UPDATER` varchar(32) DEFAULT NULL COMMENT '更新人',

  PRIMARY KEY (`ID`)
)
ENGINE=InnoDB
COMMENT='拣货单明细表';