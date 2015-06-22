from unittest import TestCase
from semNets.Primitives import Relation, RelationType, RelationAttributeType, NodeAttributeType, Node
import semNets.GraphDistance as gd


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

  def test_relationAttributeType(self):
    at = RelationAttributeType("amount")
    at2 = RelationAttributeType("amount")
    self.assertEqual(at.name, "amount")
    self.assertEqual(str(at), "amount")
    self.assertEqual(repr(at), "RelationAttributeType(name = 'amount')")
    self.assertIs(at, at2)


  def test_relationWithAttributes(self):
    rt = RelationType("has")
    at = RelationAttributeType("amount")
    source = Node("bird")
    target = Node("wing")
    r = Relation(rt, source, target)
    a = r.createAttribute(at, 2)

    self.assertIs(r.attributes[0], a)
    self.assertIs(a.type, at)
    self.assertEqual(a.value, 2)
    self.assertEqual(str(a), "amount: 2")
    self.assertEqual(repr(a), "Attribute(type = 'amount', value = '2')")

  def test_SameAttributeTypeTwice(self):
    rt = RelationType("has")
    at = RelationAttributeType("amount")
    source = Node("bird")
    target = Node("wing")
    r = Relation(rt, source, target)
    a = r.createAttribute(at, 2)
    with self.assertRaises(AssertionError):
      a2 = r.createAttribute(at, 10)

  def test_hasAttributeOfType(self):
    rt = RelationType("has")
    at = RelationAttributeType("amount")
    source = Node("bird")
    target = Node("wing")
    r = Relation(rt, source, target)
    a = r.createAttribute(at, 2)
    x = r.hasAttributeOfType(at)
    self.assertTrue(x)

  def test_calculateAttributeDistance_sameRelation(self):
    rt = RelationType("is_a")
    at = RelationAttributeType("wings")
    at2 = RelationAttributeType("color")
    at3 = RelationAttributeType("size")
    source = Node("EmporerPenguin")
    target = Node("Bird")
    r = Relation(rt, source, target)
    a = r.createAttribute(at, 2)
    a2 = r.createAttribute(at2, "blackwhite")
    a3 = r.createAttribute(at3, "big")

    dist = gd.calculateRelationDistance(r, r)
    self.assertEqual(dist, 0)

  def test_calculateDistance_differentSource(self):
    rt = RelationType("is_a")
    source = Node("EmporerPenguin")
    source2 = Node("LittlePenguin")
    target = Node("Bird")

    r = Relation(rt, source, target)
    r2 = Relation(rt, source2, target)

    dist = gd.calculateRelationDistance(r, r2)
    self.assertEqual(dist, 0.25)

  def test_calculateDistance_differentTarget(self):
    rt = RelationType("is_a")
    source = Node("Anna")
    target = Node("Student")
    target2 = Node("Employee")

    r = Relation(rt, source, target)
    r2 = Relation(rt, source, target2)

    dist = gd.calculateRelationDistance(r, r2)
    self.assertEqual(dist, 0.25)

  def test_calculateDistance_differentOrMissingAttributes(self):
    #               emporer penguin:    emporer penguin
    #   wings       2                   2
    #   color       blackwhite          blackwhite
    #   size        big                 -
    #   population  -                   notsomany

    rt = RelationType("is_a")
    at = RelationAttributeType("wings")
    at2 = RelationAttributeType("color")
    at3 = RelationAttributeType("size")
    at4 = RelationAttributeType("population")
    source = Node("EmporerPenguin")
    target = Node("Bird")
    r = Relation(rt, source, target)
    a = r.createAttribute(at, 2)
    a2 = r.createAttribute(at2, "blackwhite")
    a3 = r.createAttribute(at3, "big")
    r2 = Relation(rt, source, target)
    a4 = r2.createAttribute(at, 2)
    a5 = r2.createAttribute(at2, "blackwhite")
    a6 = r2.createAttribute(at4, "notsomany" )

    dist = gd.calculateRelationDistance(r, r2)
    self.assertEqual(dist, 0.125)

  def test_calculateDistance_Symmetry(self):
    rt = RelationType("is_a")
    at = RelationAttributeType("wings")
    at2 = RelationAttributeType("size")
    source = Node("EmporerPenguin")
    source2 = Node("LittlePenguin")
    target = Node("Bird")
    r = Relation(rt, source, target)
    r2 = Relation(rt, source2, target)
    r.createAttribute(at, 2)
    r2.createAttribute(at, 2)
    r.createAttribute(at2, "big")
    r2.createAttribute(at2, "small")

    dist1 = gd.calculateRelationDistance(r,r2)
    dist2 = gd.calculateRelationDistance(r2, r)
    self.assertEqual(dist1, dist2)

  def test_calculateDistance_customWeights(self):
    rt = RelationType("is_a")
    at = RelationAttributeType("wings")
    at2 = RelationAttributeType("size")
    source = Node("EmporerPenguin")
    source2 = Node("LittlePenguin")
    target = Node("Bird")

    r = Relation(rt, source, target)
    r2 = Relation(rt, source2, target)

    r.createAttribute(at, 2)
    r.createAttribute(at2, "big")
    r2.createAttribute(at2, "small")
    dist = gd.calculateRelationDistance(r, r2, wSource=0.5, wDifferentStringValue=0.3, wMissingAttribute=0.7)
    self.assertEqual(dist, 0.75)


