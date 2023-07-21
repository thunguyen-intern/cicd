from odoo.addons.base_utils import utils


class TestA(utils.Utility):
    _name = 't.a'

    value = 3
    number = 1

    def get_sum_value_and_number(self):
        return self.value + self.number

    def get_total_number(self):
        return self.number


class TestB(utils.Utility):
    _name = 't.b'
    _inherit = 't.a'

    value = 5

    def get_ancestor_sum_value(self):
        self.get_sum_value_and_number()

    def get_total_number(self):
        res = super().get_total_number()
        return res + self.number


class TestC(utils.Utility):
    _name = 't.c'
    _inherit = 't.a'

    value = 7
    number = 2

    def get_total_number(self):
        res = super().get_total_number()
        return res + self.number


class TestD(utils.Utility):
    _name = 't.d'
    _inherit = 't.b'

    value = 9

    def get_total_number(self):
        res = super().get_total_number()
        return res + self.number


class TestE1(utils.Utility):
    _name = 't.e'
    _inherit = ('t.d', 't.c')

    value = 2

    def get_total_number(self):
        res = super().get_total_number()
        return res + self.number


class TestE2(utils.Utility):
    _name = 't.e'
    _inherit = 't.e'

    value = 4
    number = 6

    def get_total_number(self):
        res = super().get_total_number()
        return res + self.number


class TestE3(utils.Utility):
    _name = 't.e'
    _inherit = ('t.e', 't.d')

    value = 6

    def get_total_number(self):
        res = super().get_total_number()
        return res + self.number
