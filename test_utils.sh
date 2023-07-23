#!/bin/bash 
 
/opt/odoo/odoo-bin -c /etc/odoo.conf -d abc -i base_utils,test_base_utils --stop-after-init 
/opt/odoo/odoo-bin -c /etc/odoo.conf -d abc --test-tag /base_utils,/test_base_utils --stop-after-init