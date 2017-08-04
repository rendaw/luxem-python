import unittest

import luxem

long_text = b'''{
    key1: val1,
    key1.5: val1.5,
    key3: (type3) val3,
    key4: (type4) "val4 with spaces",
    key5: [
        val5.1,
        val5.2,
        (type5.3) {
            val5.3.3: [
            ],
        },
        {
        },
    ],
},
'''


def write_long_sequence(writer):
    (
        writer.object_begin()
            .key('key1').primitive('val1')  # noqa
            .key('key1.5').primitive('val1.5')
            .key('key3').type('type3').primitive('val3')
            .key('key4').type('type4').primitive('val4 with spaces')
            .key('key5').array_begin()
                .primitive('val5.1')  # noqa
                .primitive('val5.2')  # noqa
                .type('type5.3').object_begin()  # noqa
                    .key('val5.3.3').array_begin().array_end()  # noqa
                .object_end()  # noqa
                .object_begin()  # noqa
                .object_end()  # noqa
            .array_end()
        .object_end()
    )


class TestRawWrite(unittest.TestCase):
    def setUp(self):
        self.sequence = []
        self.writer = luxem.Writer(
            target=lambda text: self.sequence.append(text),
            pretty=True,
            use_spaces=True,
            indent_multiple=4
        )

    def compare(self, string):
        output = b''.join(self.sequence)
        if isinstance(string, set):
            self.assertIn(output, string)
        else:
            self.assertEqual(output, string)

    def test_string(self):
        self.writer.primitive('primitive')
        self.compare(b'primitive,\n')

    def test_string_spaces(self):
        self.writer.primitive('has spaces')
        self.compare(b'"has spaces",\n')

    def test_string_quotes(self):
        self.writer.primitive('"')
        self.compare(b'"\\"",\n')

    def test_type(self):
        self.writer.type('type').primitive('value')
        self.compare(b'(type) value,\n')

    def test_type_with_spaces(self):
        self.writer.type('has spaces').primitive('value')
        self.compare(b'(has spaces) value,\n')

    def test_object(self):
        self.writer.object_begin().object_end()
        self.compare(b'{\n},\n')

    def test_typed_object(self):
        self.writer.type('type').object_begin().object_end()
        self.compare(b'(type) {\n},\n')

    def test_object_object(self):
        (
            self.writer.object_begin()
                .key('key').object_begin().object_end()
            .object_end()
        )
        self.compare(b'{\n    key: {\n    },\n},\n')

    def test_object_one_element(self):
        (
            self.writer.object_begin()
                .key('key').primitive('primitive')
            .object_end()
        )
        self.compare(b'{\n    key: primitive,\n},\n')

    def test_object_one_typed_element(self):
        (
            self.writer.object_begin()
                .key('key').type('type').primitive('primitive')
            .object_end()
        )
        self.compare(b'{\n    key: (type) primitive,\n},\n')

    def test_array(self):
        self.writer.array_begin().array_end()
        self.compare(b'[\n],\n')

    def test_object_array(self):
        (
            self.writer.object_begin()
                .key('key').array_begin().array_end()
            .object_end()
        )
        self.compare(b'{\n    key: [\n    ],\n},\n')

    def test_typed_array(self):
        self.writer.type('type').array_begin().array_end()
        self.compare(b'(type) [\n],\n')

    def test_array_one_element(self):
        self.writer.array_begin().primitive('primitive').array_end()
        self.compare(b'[\n    primitive,\n],\n')

    def test_basic(self):
        write_long_sequence(self.writer)
        self.compare(long_text)


class TestRawWriteBuffer(unittest.TestCase):
    def setUp(self):
        self.writer = luxem.Writer(
            pretty=True,
            use_spaces=True,
            indent_multiple=4
        )

    def compare(self, string):
        output = self.writer.dump()
        self.assertEqual(output, string)

    def test_string(self):
        self.writer.primitive('primitive')
        self.compare(b'primitive,\n')

    def test_basic(self):
        write_long_sequence(self.writer)
        self.compare(long_text)


class TestRawWriteFile(unittest.TestCase):
    def setUp(self):
        self.file = open('test_temp_file', 'wb+')
        self.file.truncate()
        self.writer = luxem.Writer(
            target=self.file,
            pretty=True,
            use_spaces=True,
            indent_multiple=4
        )

    def tearDown(self):
        self.file.close()

    def compare(self, string):
        self.file.seek(0)
        output = self.file.read()
        self.assertEqual(output, string)

    def test_string(self):
        self.writer.primitive('primitive')
        self.writer = None
        self.compare(b'primitive,\n')

    def test_basic(self):
        write_long_sequence(self.writer)
        self.writer = None
        self.compare(long_text)
