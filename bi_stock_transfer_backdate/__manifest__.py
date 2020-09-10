# -*- coding : utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name'          : 'Stock Transfer Backdate and Remarks in Odoo',
    'version'       : '12.0.0.0',
    'category'      : 'Warehouse',
    'summary'       : 'Custom back date will be transfer to stock entries and accounting entries',
    'description'   : """The stock passing same date to move and account
    
     
    stock transfer backdating
    stock transfers backdating
    inventory stock transfer backdating
     inventory transfer backdating
     inventory transfer backdating
     stock backdate
     Stock Transfers Backdate
     inventory Transfers Backdate
     inventory backdating option
     stock backdating options
     Inventory Backdate Operations
     Backdate Options
     backdating options
     Inventory Backdate Operations
     Backdate Operations
     warehouse backdate operations
     wareshouse stock backdate operations
    
    
    
     entries so to avoid the problem this app will help to put custom back date and remarks.Custom back date will be transfer to stock entries and accounting entries  
    """,
    'author'        : 'Browseinfo',
    'website'       : 'https://www.browseinfo.in',
    'currency': 'EUR',
    'price': 25, 
    'depends'       : ['base','sale_management','stock','stock_account'],
    'data'          : [
                        'wizard/stock_wizards_views.xml',
                        'views/stockpicking_views.xml',
                        'views/stock_move_views.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
    "live_test_url":'https://youtu.be/0zzY-nwp1ro',
    "images":["static/description/Banner.png"],
}
