# Copyright © 2022 Novobi, LLC
# See LICENSE file for full copyright and licensing details.

from collections.abc import Mapping

from odoo import api
from odoo.tools import classproperty


class Environment(api.Environment):
    """
    Monkey-patch Environment, so that utilities can be easily accessed
    This should work the same way as company
    """

    @classproperty
    def envs(self):
        """Do nothing. Just to complete this class as the super does not implement this"""

    @api.lazy_property
    def utl(self) -> Mapping:
        from . import utils
        proxy = utils.UtilMappingProxy(
            self,
            self.registry.utl,
        )
        return proxy

    api.Environment.utl = utl
