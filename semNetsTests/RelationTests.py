from unittest import TestCase
from semNets.Relation import Relation, RelationType, AttributeType
from semNets.Node import Node

class RelationTests (TestCase):
  def test_relationType(self):
    rt = RelationType("is-a")
    rt2 = RelationType("is-a")
    self.assertEqual(rt.name, "is-a")
    self.assertEqual(str(rt), "is-a")
    self.assertEqual(repr(rt), "RelationType(name = 'is-a')")
    self.assertIs(rt, rt2)

  def test_relation(self):
    rt = RelationType("is-a")
    source = Node("pelican")
    target = Node("bird")
    r = Relation(rt, source, target)
    self.assertEqual(r.type, rt)
    self.assertEqual(r.source, source)
    self.assertEqual(r.target, target)
    self.assertEqual(str(r), "pelican is-a bird")
    self.assertEqual(repr(r), "Relation(type = 'is-a', source = 'pelican', target = 'bird')")

  def test_attributeType(self):
    at = AttributeType("amount")
    at2 = AttributeType("amount")
    self.assertEqual(at.name, "amount")
    self.assertEqual(str(at), "amount")
    self.assertEqual(repr(at), "AttributeType(name = 'amount')")
    self.assertIs(at, at2)


  def test_relationWithAttributes(self):
    rt = RelationType("has")
    at = AttributeType("amount")
    source = Node("bird")
    target = Node("wing")
    r = Relation(rt, source, target)
    a = r.createAttribute(at, 2)

    self.assertIs(r.attributes[0], a)
    self.assertIs(a.type, at)
    self.assertEqual(a.value, 2)
    self.assertEqual(str(a), "bird has wing with amount: 2")
    self.assertEqual(repr(a), "Attribute(type = 'amount', relation = 'bird has wing', value = '2')")
