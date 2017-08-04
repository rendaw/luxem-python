import unittest
try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest

import luxem

long_input = b'''

{
       key1: val1,key1.5:val1.5,
       \"key2 with spaces\": \"val2 with spaces\",
       key3: (type3) val3,
       key4:(type4)\"val4 with spaces\",
       key5: [
               val5.1,
               \"val5.2\",
               (type5.3) {
                       val5.3.3: [],
               },
               {
               }
       ]
}
'''

long_input_sequence = [
        ('object begin', None),
        ('key', 'key1'),
        ('primitive', 'val1'),
        ('key', 'key1.5'),
        ('primitive', 'val1.5'),
        ('key', 'key2 with spaces'),
        ('primitive', 'val2 with spaces'),
        ('key', 'key3'),
        ('type', 'type3'),
        ('primitive', 'val3'),
        ('key', 'key4'),
        ('type', 'type4'),
        ('primitive', 'val4 with spaces'),
        ('key', 'key5'),
        ('array begin', None),
        ('primitive', 'val5.1'),
        ('primitive', 'val5.2'),
        ('type', 'type5.3'),
        ('object begin', None),
        ('key', 'val5.3.3'),
        ('array begin', None),
        ('array end', None),
        ('object end', None),
        ('object begin', None),
        ('object end', None),
        ('array end', None),
        ('object end', None),
]


class TestRawRead(unittest.TestCase):
    def setUp(self):
        self.sequence = []
        self.reader = luxem.Reader(
            object_begin=lambda: self.sequence.append(
                ('object begin', None)),
            object_end=lambda: self.sequence.append(('object end', None)),
            array_begin=lambda: self.sequence.append(
                ('array begin', None)),
            array_end=lambda: self.sequence.append(('array end', None)),
            key=lambda data: self.sequence.append(('key', data)),
            type=lambda data: self.sequence.append(('type', data)),
            primitive=lambda data: self.sequence.append(
                ('primitive', data)),
        )

    def compare(self, expected_sequence):
        for got, expected in izip_longest(
                enumerate(self.sequence),
                enumerate(expected_sequence)):
            self.assertEqual(got, expected)

    def test_empty(self):
        self.reader.feed(b'')
        self.compare([])

    def test_comment(self):
        self.reader.feed(b'*nothing to see here*')
        self.compare([])

    def test_escaped_comment(self):
        self.reader.feed(b'*escape \\* escape*')
        self.compare([])

    def test_untyped(self):
        self.reader.feed(b'7')
        self.compare([('primitive', '7')])

    def test_untyped_comment(self):
        self.reader.feed(b'* before * *again* 7 * after * *lagoon*')
        self.compare([('primitive', '7')])

    def test_untyped_comma(self):
        self.reader.feed(b'7, ')
        self.compare([('primitive', '7')])

    def test_untyped_words(self):
        self.reader.feed(b'"yodel minister"')
        self.compare([('primitive', 'yodel minister')])

    def test_untyped_empty(self):
        self.reader.feed(b'""')
        self.compare([('primitive', '')])

    def test_untyped_word_escapes(self):
        self.reader.feed(b'goob\\er')
        self.compare([('primitive', 'goober')])

    def test_untyped_words_escapes(self):
        self.reader.feed(b'"\\" is \\\\ apple"')
        self.compare([('primitive', '" is \\ apple')])

    def test_untyped_nofinish(self):
        self.reader.feed(b'7', finish=False)
        self.compare([])

    def test_typed(self):
        self.reader.feed(b'(int) 7')
        self.compare([('type', 'int'), ('primitive', '7')])

    def test_object(self):
        self.reader.feed(b'{}')
        self.compare([('object begin', None), ('object end', None)])

    def test_key_object(self):
        self.reader.feed(b'{q:7}')
        self.compare([
            ('object begin', None),
            ('key', 'q'),
            ('primitive', '7'),
            ('object end', None)])

    def test_close_object_nofinish(self):
        self.reader.feed(b'{}', finish=False)
        self.compare([('object begin', None), ('object end', None)])

    def test_array(self):
        self.reader.feed(b'[]')
        self.compare([('array begin', None), ('array end', None)])

    def test_basic(self):
        read_length = self.reader.feed(long_input)
        self.assertEqual(read_length, len(long_input))
        self.compare(long_input_sequence)

    def test_break_whitespace(self):
        read_length = self.reader.feed(b' ', finish=False)
        self.assertEqual(read_length, 0)
        read_length = self.reader.feed(b'  a')
        self.assertEqual(read_length, 3)
        self.compare([('primitive', 'a')])

    def test_type_only(self):
        self.reader.feed(b'(x),')
        self.compare([('type', 'x'), ('primitive', '')])

    def test_type_only_eof(self):
        self.reader.feed(b'(x)', True)
        self.compare([('type', 'x'), ('primitive', '')])

    def test_type_only_array(self):
        self.reader.feed(b'[(x)]')
        self.compare([
            ('array begin', None),
            ('type', 'x'),
            ('primitive', ''),
            ('array end', None)])

    def test_type_only_object(self):
        self.reader.feed(b'{key: (x)}')
        self.compare([
            ('object begin', None),
            ('key', 'key'),
            ('type', 'x'),
            ('primitive', ''),
            ('object end', None)])


class TestRawReadFile(TestRawRead):
    def setUp(self):
        super(TestRawReadFile, self).setUp()
        self.data = open('test_temp_file', 'wb+')
        self.data.truncate()

    def tearDown(self):
        self.data.close()

    def test_test_setup(self):
        self.data.write(b'wizzly gumb')
        self.data.seek(0)
        self.assertEqual(self.data.read(), b'wizzly gumb')

    def test_empty(self):
        self.reader.feed(self.data)
        self.compare([])

    def test_untyped(self):
        self.data.write(b'7')
        self.data.seek(0)
        self.reader.feed(self.data)
        self.compare([('primitive', '7')])

    def test_untyped_comma(self):
        self.data.write(b'7, ')
        self.data.seek(0)
        self.reader.feed(self.data)
        self.compare([('primitive', '7')])

    def test_untyped_words(self):
        self.data.write(b'"yodel minister"')
        self.data.seek(0)
        self.reader.feed(self.data)
        self.compare([('primitive', 'yodel minister')])

    def test_object(self):
        self.data.write(b'{}')
        self.data.seek(0)
        self.reader.feed(self.data)
        self.compare([('object begin', None), ('object end', None)])

    def test_array(self):
        self.data.write(b'[]')
        self.data.seek(0)
        self.reader.feed(self.data)
        self.compare([('array begin', None), ('array end', None)])

    def test_basic(self):
        self.data.write(long_input)
        self.data.seek(0)
        self.reader.feed(self.data)
        self.compare(long_input_sequence)

    def test_long_file(self):
        compare_sequence = []
        for index in range(100):
            string = 'index {}, plus some junk: {}'.format(index, '*' * 30)
            self.data.write('"{}",'.format(string).encode('utf-8'))
            compare_sequence.append(('primitive', string))
        self.data.seek(0)
        self.reader.feed(self.data)
        self.compare(compare_sequence)


class TestRawRead2(unittest.TestCase):
    def test_callback_void_except(self):
        class TestError(Exception):
            pass

        def callback():
            raise TestError()
        reader = luxem.Reader(
            object_begin=callback,
            object_end=None,
            array_begin=None,
            array_end=None,
            key=None,
            type=None,
            primitive=None
        )
        self.assertRaises(TestError, reader.feed, b'{}')
