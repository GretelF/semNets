from unittest import TestCase
from semNets.Relation import Relation
from semNets.Relation import RelationType
from semNets.Node import Node

class RelationTypeTests (TestCase):
  def test_(self):
    rt = RelationType("is-a")
    rt2 = RelationType("is-a")
    self.assertEqual(rt.name, "is-a")
    self.assertEqual(str(rt), "is-a")
    self.assertEqual(repr(rt), "RelationType(name = 'is-a')")
    self.assertEqual(rt, rt2)

class RelationTests (TestCase):
  def test_(self):
    rt = RelationType("is-a")
    source = Node("pelican")
    target = Node("bird")
    r = Relation(rt, source, target)
    self.assertEqual(r.type, rt)
    self.assertEqual(r.source, source)
    self.assertEqual(r.target, target)
    self.assertEqual(str(r), "pelican is-a bird")
    self.assertEqual(repr(r), "Relation(type = RelationType(name = 'is-a'), source = Node(name = 'pelican'), target = Node(name = 'bird'))")
