import unittest

from luxem import dumps, Typed


class TestWrite(unittest.TestCase):
    def test_int(self):
        self.assertEqual(dumps(7), b'7,')

    def test_typed_int(self):
        self.assertEqual(dumps(Typed('int', 7)), b'(int)7,')

    def test_float(self):
        self.assertEqual(dumps(7.9), b'7.9,')

    def test_string(self):
        self.assertEqual(dumps('hey'), b'hey,')

    def test_spaced_string(self):
        self.assertEqual(dumps('hey glovebox'), b'"hey glovebox",')

    def test_escaped_string(self):
        self.assertEqual(dumps('do\\g'), b'do\\g,')

    def test_escaped_spaced_string(self):
        self.assertEqual(dumps('hey \\glovebox'), b'"hey \\\\glovebox",')

    def test_object(self):
        self.assertEqual(dumps({}), b'{},')

    def test_object_keys(self):
        self.assertIn(
            dumps({'dig': 'wombat', 'fig': 'combat'}),
            {
                b'{dig:wombat,fig:combat,},',
                b'{fig:combat,dig:wombat,},',
            })

    def test_object_key_object(self):
        self.assertEqual(dumps({'elebent': {}}), b'{elebent:{},},')

    def test_object_key_array(self):
        self.assertEqual(dumps({'elebent': []}), b'{elebent:[],},')

    def test_array(self):
        self.assertEqual(dumps([]), b'[],')

    def test_array_elements(self):
        self.assertEqual(dumps(['flag', 'nutter']), b'[flag,nutter,],')

    def test_array_array(self):
        self.assertEqual(dumps([[]]), b'[[],],')

    def test_array_object(self):
        self.assertEqual(dumps([{}]), b'[{},],')

    def test_unknown_type(self):
        self.assertEqual(
            dumps(Typed('element', 'palloodium')),
            b'(element)palloodium,')
