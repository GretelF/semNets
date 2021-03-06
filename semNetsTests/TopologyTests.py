from unittest import TestCase
from semNets.Topology import Topology
from semNets.Primitives import Node, Relation, RelationType, NodeAttributeType, RelationAttributeType
import json


class TopologyTests(TestCase):
  def test_insertNodesAndRelations(self):
    t = Topology()
    n0 = Node("bird")
    n1 = Node("pelican")
    rt = RelationType("is_a")
    r = Relation(rt, n0, n1)

    self.assertFalse(t.existsNode(n0))
    self.assertFalse(t.existsNode(n1))
    self.assertFalse(t.existsRelation(r))

    t.insertNode(n0)
    t.insertNode(n1)
    t.insertRelation(r)

    self.assertTrue(t.existsNode(n0))
    self.assertTrue(t.existsNode(n1))
    self.assertTrue(t.existsRelation(r))

    with self.assertRaises(AssertionError):
      t.insertNode(n0)

    t.insertRelation(r)
    self.assertTrue(len(t.relations), 2)

  def test_load(self):
    with open("TestData.json") as file:
      net = json.load(file)

    t = Topology()
    t.load(net)

    self.assertTrue(t.existsNode(Node("bird")))
    self.assertTrue(t.existsNode(Node("pelican")))
    self.assertTrue(len(t.nodes), 4)
    self.assertEqual(len(t.relations),4)
    self.assertEqual(t.nodes[1], Node("pelican"))
    self.assertEqual(t.nodes[1].attributes[0].type, NodeAttributeType("size"))
    self.assertEqual(t.nodes[1].attributes[0].value, "big")
    self.assertEqual(t.nodes[1].attributes[1].type, NodeAttributeType("color"))
    self.assertEqual(t.nodes[1].attributes[1].value, "white")

    r = Relation(RelationType("is_a"), Node("pelican"), Node("bird"))

    self.assertEqual(t.relations[0], r)

    r2 = Relation(RelationType("has"), Node("bird"), Node("wings"))
    r2.createAttribute(RelationAttributeType("amount"), 2)

    self.assertEqual(t.relations[1], r2)

# Todo: test findPath(), existsPath(), getAllRelations()

  def test_existsPath(self):
    with open("findPathTest.json") as file:
      net = json.load(file)


    t = Topology()
    t.load(net)

    bool = t.existsPath(Node("pelican"), Node("creature"))
    bool2 = t.existsPath(Node("wings"), Node("creature"))
    self.assertTrue(bool)
    self.assertFalse(bool2)

  def test_findPath(self):
    with open("findPathTest.json") as file:
      net = json.load(file)

    t = Topology()
    t.load(net)

    path, iterations = t.findPath(Node("pelican"), Node("creature"))

    self.assertEqual(iterations, 2)
    self.assertEqual(path[0], Node("pelican"))
    self.assertEqual(path[1], Node("bird"))
    self.assertEqual(path[2], Node("animal"))
    self.assertEqual(path[3], Node("creature"))

  def test_existsNodeIncludingParentTopology(self):
    with open("graph1.json") as file:
      net = json.load(file)

    t = Topology()
    t.load(net)

    t2 = Topology()
    n = Node("black")
    t2.insertNode(n)

    t2.setParent(t)

    n2 = Node("violet")

    self.assertTrue(t2.existsNode(n))
    self.assertTrue(t2.existsNode(n2))
