# Auction iPay Python bindings
# Author: Chee-Hyung Yoon <yoon@tikkon.com>

import suds

# Auction's iPay API endpoint
api_base = 'https://api.auction.co.kr/ArcheSystem/IpayService.asmx?wsdl'

class AddAttributePlugin(suds.plugin.MessagePlugin):
    """Plugin to add the item_option_name attribute to the IpayServiceItems."""
    def marshalled(self, context):
        body = context.envelope.getChild('Body')
        if body[0].name == 'InsertIpayOrder':
            for item in body[0][1]:
                if item.get('item_option_name') is None:
                    # Then set an empty item_option_name
                    item.set('item_option_name', '')

class IpayAPI(object):
    """A client for the Auction iPay API."""
    
    def __init__(self, seller_id, ipay_key):
        self.seller_id = seller_id
        self.client = suds.client.Client(
            api_base, faults=False, plugins=[AddAttributePlugin()]
        )
        # Manual setting of soap header is required due to an iPay bug
        xmlns = ('s2', 'http://www.auction.co.kr/Security')
        ticket = suds.sax.element.Element('EncryptedTicket', ns=xmlns)
        value = suds.sax.element.Element('Value', ns=xmlns).setText(ipay_key)
        ticket.append(value)
        self.client.set_options(soapheaders=ticket)
    
    def create_item(self, name, seller_order_no, price, qty, item_url,
                    thumbnail_url, image_url=None, description=None,
                    option=None, cancellable=True):
        """
        Creates an item to be ordered.
        @return: The created item.
        """
        item = self.client.factory.create('ns0:IpayServiceItems')
        item._item_name = name
        item._ipay_itemno = seller_order_no
        item._item_option_name = option
        item._item_price = price
        item._order_qty = qty
        item._item_url = item_url
        item._thumbnail_url = thumbnail_url
        item._item_image_url = image_url
        item._item_description = description
        item._cancel_restriction = 0 if cancellable else 1
        return item
    
    def create_order(self, payment_rule, total, shipping_price, shipping_type,
                     back_url, service_url, redirect_url, address_required=True,
                     buyer_name=None, buyer_tel_no=None, buyer_email=None,
                     redirection_enabled=False):
        """
        Creates an order for the given items.
        @param shipping_type: Type of shipping (1: Free, 2: COD, 3: Paid)
        @type shipping_type: int
        @return: The created order.
        """
        order = self.client.factory.create('ns0:IpayServiceOrder')
        order._payment_rule = payment_rule
        order._pay_price = total
        order._shipping_price = shipping_price
        order._shipping_type = shipping_type
        order._back_url = back_url
        order._service_url = service_url
        order._redirect_url = redirect_url
        order._is_address_required = address_required
        order._buyer_name = buyer_name
        order._buyer_tel_no = buyer_tel_no
        order._buyer_email = buyer_email
        order._move_to_redirect_url = redirection_enabled
        return order
    
    def place_order(self, order, items):
        """Places an order for the given items."""
        ipay_items = self.client.factory.create('ArrayOfIpayServiceItems')
        for item in items:
            ipay_items.IpayServiceItems.append(item)
        return self.client.service.InsertIpayOrder(order, ipay_items)
        
    def finalize_order(self, order_no, seller_order_no, reason):
        """Finalizes an order and requests payment from Auction."""
        req = self.client.factory.create('ns0:DoOrderDecisionRequestT')
        req._SellerID = self.seller_id
        req._OrderNo = order_no
        req._SellerManagementNumber = seller_order_no
        req._RequestReason = reason
        return self.client.service.DoIpayOrderDecisionRequest(req)
    
    def get_order_status(self, cart_no, item_no):
        """Returns the status of an order."""
        return self.client.service.GetIpayReceiptStatus(cart_no, item_no)
    
    def get_order_data(self, pay_no):
        """Returns the payment and other data for the given order."""
        return self.client.service.GetIpayAccountNumb(pay_no)
    
    def get_order_list(self, search_type, value):
        """Returns the list of paid orders for the given query data."""
        req = self.client.factory.create('ns0:GetOrderListRequestT')
        req._SearchType = search_type
        req._SearchValue = value        
        return self.client.service.GetIpayPaidOrderList(req)
    
    def ship_order(self, order_no, ship_date):
        """Changes the shipment status of the order to shipped."""            
        req = self.client.factory.create('ns0:DoShippingGeneralRequestT')
        req._SellerID = self.seller_id
        req._OrderNo = order_no
        # TODO: implement this method
        return self.client.service.DoIpayShippingGeneral(req)
    
    def test(self):
        """Returns the IP address of the client."""
        return self.client.service.test()
