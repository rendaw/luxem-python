import unittest

from luxem import loads
from luxem import Typed


class TestRead(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(loads(b''), [])

    def test_primitive(self):
        self.assertEqual(loads(b'a'), ['a'])

    def test_primitive1(self):
        self.assertEqual(loads(b'a,'), ['a'])

    def test_root_array(self):
        self.assertEqual(loads(b'a, a'), ['a', 'a'])

    def test_typed(self):
        self.assertEqual(loads(b'(b)a'), [Typed('b', 'a')])

    def test_array(self):
        self.assertEqual(loads(b'[]'), [[]])

    def test_array1(self):
        self.assertEqual(loads(b'[],'), [[]])

    def test_typed_array(self):
        self.assertEqual(loads(b'(b)[]'), [Typed('b', [])])

    def test_array_element(self):
        self.assertEqual(loads(b'[a]'), [['a']])

    def test_object(self):
        self.assertEqual(loads(b'{}'), [{}])

    def test_object1(self):
        self.assertEqual(loads(b'{},'), [{}])

    def test_typed_object(self):
        self.assertEqual(loads(b'(b){}'), [Typed('b', {})])

    def test_object_element(self):
        self.assertEqual(loads(b'{k: a}'), [{'k': 'a'}])
