from unittest import TestCase
from semNets.Topology import Topology
from semNets.Primitives import Node, Relation, RelationType, RelationAttributeType
from semNets.View import View
import json

def buildTopology():
  t = Topology()

  with open("TestData.json") as file:
    net = json.load(file)

    t = Topology()
    t.load(net)
  return t


class ViewTests(TestCase):
  def test_basicViewOperations(self):
    n = Node("penguin")
    t = buildTopology()
    t.insertNode(n)
    r = Relation(RelationType("is_a"), n, Node("bird"))
    t.insertRelation(r)
    v = View(t)

    with self.assertRaises(AssertionError):
      v.includeNode(Node("beatle"))                 # does not exist in topology t

    self.assertEqual(len(v.nodes), 0)
    self.assertEqual(len(v.relations), 0)

    v.includeNode(n)
    v.includeRelation(r)

    self.assertIn(n, v.nodes)
    self.assertIn(r, v.relations)

    v.mend()

    self.assertIn(Node("bird"), v.nodes)            # after mend the Node(name="bird") should be in the view, too

  def test_expand(self):
    t = buildTopology()
    v = View(t)

    v.includeNode(Node("bird"))




