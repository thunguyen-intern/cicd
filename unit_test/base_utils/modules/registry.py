# Copyright © 2022 Novobi, LLC
# See LICENSE file for full copyright and licensing details.

import functools

from collections.abc import Mapping

from odoo import SUPERUSER_ID
from odoo.modules import registry

from ..api import Environment


class UtilRegistry(Mapping):
    def __init__(self):
        super().__init__()
        self.utils = {}

    def __len__(self):
        return len(self.utils)

    def __iter__(self):
        return iter(self.utils)

    def __getitem__(self, util_name):
        return self.utils[util_name]

    def __call__(self, util_name):
        return self.__getitem__(util_name)

    def __setitem__(self, util_name, util):
        self.utils[util_name] = util

    def __delitem__(self, util_name):
        del self.utils[util_name]


class Registry(registry.Registry):
    utl: UtilRegistry

    # Initiate a shared registry
    # WARNING:
    # * This is NOT for use,
    # * This is only for avoiding errors when installing module
    # * Please make sure this module is included in `server_wide_modules`
    #   to ensure the features work as expected
    registry.Registry.utl = UtilRegistry()

    original_init = registry.Registry.init

    @functools.wraps(original_init)
    def init(self, db_name):
        res = self.original_init(db_name)
        self.utl = UtilRegistry()
        return res

    registry.Registry.init = init
    registry.Registry.original_init = original_init

    original_load = registry.Registry.load

    @functools.wraps(original_load)
    def load(self, cr, module):
        res = self.original_load(cr, module)

        from .. import utils

        for cls in utils.MetaUtil.module_to_utils.get(module.name, []):
            cls._build_utils(self.utl)

        return res

    registry.Registry.load = load
    registry.Registry.original_load = original_load

    original_setup_models = registry.Registry.setup_models

    @functools.wraps(original_setup_models)
    def setup_models(self, cr):
        res = self.original_setup_models(cr)

        env = Environment(cr, SUPERUSER_ID, {})
        utils = list(env.registry.utl.values())
        if self.ready:
            for util in utils:
                util._unregister_hook()
        for util in utils:
            util._prepare_setup()
        for util in utils:
            util._setup_base()
        for util in utils:
            util._setup_complete()
        if self.ready:
            for util in utils:
                util._register_hook()

        return res

    registry.Registry.setup_models = setup_models
    registry.Registry.original_setup_models = original_setup_models
