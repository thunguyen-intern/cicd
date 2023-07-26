# Copyright © 2022 Novobi, LLC
# See LICENSE file for full copyright and licensing details.

import collections
from collections.abc import Mapping

from odoo.tools import LastOrderedSet

from . import api
from .modules import registry


class MetaUtil(type):
    """
    The metaclass of all utilities.
    Its main purpose is to register the utilities.
    """

    module_to_utils = collections.defaultdict(list)

    def __new__(mcs, name, bases, attrs):
        if attrs.get('_register', True) and '_module' not in attrs:
            module = attrs['__module__']
            assert module.startswith('odoo.addons.'), \
                f"Invalid import of {module}.{name}, it should start with 'odoo.addons'."
            attrs['_module'] = module.split('.')[2]

        inherit = attrs.get('_inherit', ())
        if isinstance(inherit, str):
            inherit = attrs['_inherit'] = (inherit,)
        else:
            attrs['_inherit'] = inherit
        if '_name' not in attrs:
            attrs['_name'] = inherit[0] if len(inherit) == 1 else name

        return super().__new__(mcs, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if attrs.get('_register', True) and '_module' in attrs:
            cls.module_to_utils[attrs['_module']].append(cls)


class UtilMappingProxy(Mapping):
    class UtilProxy:
        env: api.Environment
        _cls: MetaUtil

        __slots__ = ('env', '_cls')

        def __init__(self, env, cls):
            super().__init__()
            self.env = env
            self._cls = cls

        def __call__(self, *args, **kwargs):
            res = self._cls(*args, **kwargs)
            res.env = self.env
            return res

        @property
        def cls(self):
            klass = self._cls
            name = klass.__name__
            res = type(name, (klass,), {
                '_name': name,
                '_register': False,
                'env': self.env
            })
            return res

    env: api.Environment
    utils: registry.UtilRegistry

    __slots__ = ('env', 'utils')

    def __init__(self, env, utils):
        super().__init__()
        self.env = env
        self.utils = utils

    def __len__(self):
        return len(self.utils)

    def __iter__(self):
        return iter(self.utils)

    def __getitem__(self, util_name):
        cls = self.utils[util_name]
        return self.UtilProxy(self.env, cls)

    def __call__(self, util_name):
        return self.__getitem__(util_name)

    def __setitem__(self, util_name, util):
        self.utils[util_name] = util

    def __delitem__(self, util_name):
        del self.utils[util_name]


class BaseUtil(metaclass=MetaUtil):
    _name: str
    _inherit: tuple
    _module: str
    _register: bool = False

    __base_classes: tuple

    @classmethod
    def _build_utils(cls, pool):
        name = cls._name
        parents = list(cls._inherit)
        if name != 'base' and 'base' in pool:
            parents.append('base')

        if name in parents:
            if name not in pool:
                raise TypeError(f'Utility {name!r} does not exist in registry.')
            util = pool[name]
        else:
            util = type(name, (cls,), {
                '_name': name,
                '_register': False,
            })

        bases = LastOrderedSet([cls])
        for parent in parents:
            if parent not in pool:
                raise TypeError(f'Utility {name!r} inherits from non-existing Utility {parent!r}.')
            parent_class = pool[parent]
            if parent == name:
                for base in parent_class.__base_classes:
                    bases.add(base)
            else:
                bases.add(parent_class)

        util.__base_classes = tuple(bases)

        util.pool = pool
        pool[name] = util

        return util

    @classmethod
    def _prepare_setup(cls):
        """Things to do before setting up"""
        if cls.__bases__ != cls.__base_classes:
            cls.__bases__ = cls.__base_classes

    @classmethod
    def _setup_base(cls):
        """Things to do when setting up"""

    @classmethod
    def _setup_complete(cls):
        """Things to do when finishing setting up"""

    @classmethod
    def _register_hook(cls):
        """Things to do right after the registry is built"""

    @classmethod
    def _unregister_hook(cls):
        """Clean up what `_register_hook` has done"""


class Utility(BaseUtil):
    _register = False


class GenesisUtil(Utility):
    _name = 'base'
