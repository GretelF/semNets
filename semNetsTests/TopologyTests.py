from unittest import TestCase
from semNets.Topology import Topology
from semNets.Primitives import Node, Relation, RelationType

class TopologyTests (TestCase):
  def test_relationType(self):
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






