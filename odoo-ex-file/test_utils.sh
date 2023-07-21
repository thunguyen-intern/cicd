#!/bin/bash 
 
/opt/odoo/odoo-bin -c /etc/odoo.conf -d db_1 -i test_base_utils --stop-after-init
/opt/odoo/odoo-bin -c /etc/odoo.conf -d db_1 --test-tag /test_base_utils --stop-after-init