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
    t.insertRelation(r)
    self.assertIn(n0, t.nodeList)
    self.assertIn(n1, t.nodeList)
    self.assertIn(r, t.relationList)


