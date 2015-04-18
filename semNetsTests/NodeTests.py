from unittest import TestCase
from semNets.Node import Node

class NodeTests (TestCase):
  def test_(self):
    n = Node("Hello")
    self.assertIsNot(n, Node("Hello"))
    self.assertNotEqual(n, Node("Hello"))
    self.assertEqual(str(n), "N['Hello']")
    self.assertEqual(repr(n), "Node(name = 'Hello')")
