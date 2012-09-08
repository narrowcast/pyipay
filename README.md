pyipay
======

A Python library for accessing the Auction's iPay API


Installation
------------
pip install pyipay

Usage
-----

    import pyipay
    
    # Creates the API instance
    ipay = pyipay.IpayAPI("Your iPay ID", "Your iPay Key")
    
    # Creates an item
    item = ipay.create_item(
        "Test Item", "Test order", price=10, qty=2, option="Test option",
        item_url="http://localhost/item/", thumbnail_url="http://localhost/thumb",
        cancellable=True
    )
    items = (item, )
    
    # Creates an order
    order = ipay.create_order(
        payment_rule=0, total=20, shipping_price=0, shipping_type=1,
        back_url="http://localhost/back", service_url="http://localhost/service",
        redirect_url="http://localhost/redirect", address_required=False,
        redirection_enabled=True
    )

    # Places the order
    result = ipay.place_order(order, items)
    print result
