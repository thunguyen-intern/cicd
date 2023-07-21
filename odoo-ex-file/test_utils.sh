#!/bin/bash 
 
/opt/odoo/odoo-bin -c /etc/odoo.conf -d $1 -i base_utils,test_base_utils --stop-after-init