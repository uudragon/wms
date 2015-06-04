__author__ = 'pluto'

DEFAULT_PAGE_SIZE = 8

#YN 
YN_YES = 1
YN_NO = 0

#INBOUND RECEIPT STATUS
INBOUND_RECEIPT_STATUS_CANCEL = -1
INBOUND_RECEIPT_STATUS_NONE = 0
INBOUND_RECEIPT_STATUS_UNCOMPLETED = 1
INBOUND_RECEIPT_STATUS_COMPLETED = 2

#INBOUND RECEIPT DETAIL STATUS
INBOUND_RECEIPT_DETAIL_STATUS_CANCEL = -1
INBOUND_RECEIPT_DETAIL_STATUS_NONE = 0
INBOUND_RECEIPT_DETAIL_STATUS_PRE_STORAGE = 1
INBOUND_RECEIPT_DETAIL_STATUS_COMPLETED = 2

#BILL TYPE
STORAGE_RECORD_TYPE_RECEIPT = 1
STORAGE_RECORD_TYPE_OUTPUT = 5

CLIENT_ID = 'K100511456'
PRIVATE_KEY = 'U45BawXC'
#CLIENT_ID = 'K24000154'
#PRIVATE_KEY = 'weH71Rbq'
LOGISTIC_PROVIDER_ID = 'YTO'

TO_SENDER_REQUEST_HEADERS = {'content-type': 'application/x-www-form-urlencoded',
                        'Accept': 'application/x-www-form-urlencoded'}

#SENDER_SERVICE_API = 'http://58.32.246.71:8088/CommonOrderModeBServlet.action'
SENDER_SERVICE_API = 'http://service.yto56.net.cn/CommonOrderModeBServlet.action'

DEFAULT_SENDER_NAME = '\xe4\xbc\x98\xe4\xbc\x98\xe9\xbe\x99\xe6\x95\x99\xe8\x82\xb2'