from unittest import TestCase
from semNets.Primitives import Node, NodeAttributeType

class NodeTests (TestCase):
  def test_node(self):
    n = Node("Hello")
    self.assertIsNot(n, Node("Hello"))
    self.assertEqual(n, Node("Hello"))
    self.assertEqual(str(n), "Hello")
    self.assertEqual(repr(n), "Node(name = 'Hello')")\

  def test_nodeAttributes(self):
    at = NodeAttributeType("color")
    at2 = NodeAttributeType("color")
    self.assertEqual(at.name, "color")
    self.assertEqual(str(at), "color")
    self.assertEqual(repr(at), "NodeAttributeType(name = 'color')")
    self.assertIs(at, at2)

  def test_nodeWithAttributes(self):
    n = Node("pelican")
    at = NodeAttributeType("color")
    a = n.createAttribute(at, "white")
    self.assertIs(n.attributes[0], a)
    self.assertIs(a.type, at)
    self.assertEqual(str(a), "color: white")
    self.assertEqual(repr(a), "Attribute(type = 'color', value = 'white')")

