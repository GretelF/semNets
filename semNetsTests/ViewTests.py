from unittest import TestCase
from semNets.Topology import Topology
from semNets.Primitives import Node, Relation, RelationType
from semNets.View import View

def buildTopology():
  t = Topology()

  n0 = Node("foo")
  n1 = Node("bar")
  n2 = Node("baz")
  rt = RelationType("x")
  r0 = Relation(rt, n0, n1)
  r1 = Relation(rt, n1, n2)
  t.insertNode(n0)
  t.insertNode(n1)
  t.insertNode(n2)
  t.insertRelation(r0)
  t.insertRelation(r1)
  return t


class ViewTests(TestCase):
  def test_basicViewOperations(self):
    n = Node("bums")
    t = buildTopology()
    t.insertNode(n)
    r = Relation(RelationType("z"), n, t.nodes[1])
    t.insertRelation(r)
    v = View(t)

    with self.assertRaises(AssertionError):
      v.includeNode(Node("xyz"))

    self.assertEqual(len(v.nodes), 0)
    self.assertEqual(len(v.relations), 0)

    v.includeNode(n)
    v.includeRelation(r)

    self.assertIn(n, v.nodes)
    self.assertIn(r, v.relations)

    v.mend()

    self.assertIn(t.nodes[1], v.nodes)




