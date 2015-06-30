from unittest import TestCase
import semNets.GraphDistance as gd
from semNets.Topology import Topology
from semNets.Primitives import Node, Relation, RelationAttributeType, RelationType

class GraphDistanceTests(TestCase):
  def test_RelationMatching(self):
    rt = RelationType("is_a")
    at = RelationAttributeType("wings")
    at2 = RelationAttributeType("color")
    at3 = RelationAttributeType("size")
    at4 = RelationAttributeType("population")
    source = Node("EmporerPenguin")
    target = Node("Bird")
    target2 = Node("Thing")
    r = Relation(rt, source, target)
    r.createAttribute(at, 2)
    r.createAttribute(at2, "blackwhite")
    r.createAttribute(at3, "big")
    r2 = Relation(rt, source, target)
    r2.createAttribute(at, 2)
    r2.createAttribute(at2, "blackwhite")
    r2.createAttribute(at4, "notsomany" )
    r3 = Relation(rt, source, target2)
    r3.createAttribute(at, 4)
    r3.createAttribute(at2, "black")
    r3.createAttribute(at3, "enormous")

    t = Topology()
    t.insertNode(source)
    t.insertNode(target)
    t.insertNode(target2)
    t.insertRelation(r3)
    t.insertRelation(r)
    t.insertRelation(r2)

    matchedRelations = gd.matchRelations(r, source, t)
    self.assertEqual(matchedRelations[0], r)
    self.assertEqual(matchedRelations[1], r2)
    self.assertEqual(matchedRelations[2], r3)