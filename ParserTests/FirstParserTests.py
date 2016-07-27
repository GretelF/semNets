from unittest import TestCase
import json
import semNets.GraphDistance as gd
from semNets.Topology import Topology
import Parser
from Parser.Parser import goToNextPhrase, parseLog, parseValues
from semNets.Primitives import Node, Relation, RelationAttributeType, RelationType, Attribute, NodeAttributeType
from sys import maxsize

class FirstParserTests(TestCase):
  def test_firstparsertests(self):
    # load static semantic network consisting of card names and so on
    # still missing: things like "game" and "turn"

    with open("homerock.json") as file:
      net1 = json.load(file)

    g1 = Topology()
    g1.load(net1)
    g2 = Topology()



    #with open("hearthstone_log_parseTransitionsTest.txt") as file:
    with open("hearthstone_2016_06_20_15_30_29.log") as file:
        g2 = parseLog(file, g1)

    relationtype_is_a = RelationType("is_a")
    relationtype_has = RelationType("has")
    water_elemental = Node("Water Elemental")
    friendly_deck = Node("Location_Friendly_Deck_0")
    minion_0 = Node("Minion_0")
    relation1 = Relation(relationtype_is_a, minion_0, water_elemental)
    relation2 = Relation(relationtype_has, friendly_deck, minion_0)
    self.assertTrue(g2.existsRelation(relation1), "The relation 'Minion_0 is_a Water Elemental' should exist")
    self.assertTrue(g2.existsRelation(relation2), "The relation 'Location_Friendly_Deck_0 has Minion_0' should exist")
    id = g2.getNodeByName("Minion_0").getAttributeValue(NodeAttributeType("id"))
    self.assertEqual(id, 17, "minion_0 should have the ID 17, but has {0}".format(id))
    id = g2.getNodeByName("Minion_1").getAttributeValue(NodeAttributeType("id"))
    self.assertEqual(id, 29, "minion_1 should have the ID 23, but has {0}".format(id))
    id = g2.getNodeByName("Minion_2").getAttributeValue(NodeAttributeType("id"))
    self.assertEqual(id, 13, "minion_2 should have the ID 13, but has {0}".format(id))


  def test_goToNextPhrase(self):
    with open("testGoToNextPhrase.txt") as file:
      x = goToNextPhrase(file, "Hello World")
      self.assertEqual(x, "Hello World\n", "The first line containing 'Hello World' should be 'Hello World'!")
      y = goToNextPhrase(file, "Hello World")
      self.assertEqual(y, "Hello World this is a test\n", "The second line containing 'Hello World' should be 'Hello World this is a test'!")
      z = goToNextPhrase(file, "Hello World")
      self.assertEqual(z, 'Omg this is a Hello World test\n', "The third line containing 'Hello World' should be 'Omg this is a Hello World test'!")


  def test_parseValues(self):
    s = "abc=2 xy=Hallo Welt z=33"
    d = {"abc" : 2, "xy" : "Hallo Welt", "z" :33}

    d2 = parseValues(s)
    self.assertEqual(d, d2, "the parsed dict and the given dict should be equal")

    s = "name=Boulderfist Ogre id=13 zone=HAND zonePos=3 cardId=CS2_200 player=1"
    d = {"name" : "Boulderfist Ogre", "id":13, "zone":"HAND", "zonePos":3, "cardId":"CS2_200", "player":1}

    d2 = parseValues(s)

    self.assertEqual(d, d2, "the parsed dict and the given dict should be equal")

  def test_parseValuesWithEmptyString(self):
    s = ""
    d = {}
    d2 = parseValues(s)
    self.assertEqual(d, d2, "parsing an empty string for values should lead an empty dict")








