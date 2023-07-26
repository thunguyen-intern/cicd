from odoo.tests import TransactionCase, tagged


class TestUtilsCommon(TransactionCase):
    def setUp(self):
        super().setUp()
        self.utils = self.env.utl


@tagged('post_install', 'basic_test', '-at_install')
class TestUtils(TestUtilsCommon):
    def test_access_utils_registry(self):
        self.assertTrue(self.utils)

    def test_access_utils_class(self):
        util_names = ['t.a', 't.b', 't.c', 't.d', 't.e']

        for name in util_names:
            with self.subTest(name=name):
                self.assertTrue(self.utils[name])
                self.assertEqual(self.utils[name].cls._name, name)

    def test_access_unknown_utils(self):
        with self.assertRaises(KeyError):
            self.assertTrue(self.utils['test.z'].cls)

    def test_instantiate_utils_class(self):
        util_names = ['t.a', 't.b', 't.c', 't.d', 't.e']

        for name in util_names:
            with self.subTest(name=name):
                self.assertTrue(self.utils[name].cls())
                self.assertTrue(self.utils[name]())

    def test_access_utils_environment(self):
        self.assertIs(self.utils['t.a'].cls.env, self.env)
        self.assertIs(self.utils['t.b'].cls().env, self.env)
        self.assertIs(self.utils['t.c']().env, self.env)


@tagged('post_install', 'basic_test', '-at_install')
class TestUtilsInheritance(TestUtilsCommon):
    def test_get_util_static_values(self):
        util_values = {
            't.a': {'value': 3, 'number': 1},
            't.b': {'value': 5, 'number': 1},
            't.c': {'value': 7, 'number': 2},
            't.d': {'value': 9, 'number': 1},
            't.e': {'value': 6, 'number': 6},
        }

        for name, values in util_values.items():
            with self.subTest(name=name):
                cls = self.utils[name].cls
                self.assertEqual(cls.value, values['value'])
                self.assertTrue(cls.number, values['number'])

    def test_individual_method_call(self):
        util_values = {
            't.a': 4,
            't.b': 6,
            't.c': 9,
            't.d': 10,
            't.e': 12,
        }

        for name, value in util_values.items():
            with self.subTest(name=name):
                instance = self.utils[name]()
                res_sum = instance.get_sum_value_and_number()
                self.assertTrue(res_sum, value)

    def test_override_method_call(self):
        util_values = {
            't.a': 1,
            't.b': 2,
            't.c': 3,
            't.d': 3,
            't.e': 22,
        }

        for name, value in util_values.items():
            with self.subTest(name=name):
                instance = self.utils[name]()
                res_sum = instance.get_total_number()
                self.assertTrue(res_sum, value)