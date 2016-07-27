from semNets.Topology import Topology
from semNets.Primitives import Node, Relation, RelationAttributeType, RelationType, NodeAttributeType, Attribute

def parseLog(file, parent):
  test = ""
  top = Topology()
  minionCount = Node("MinionCount")
  minionCount.createAttribute(NodeAttributeType("amount"), 0)
  top.insertNode(minionCount)
  top.setParent(parent)

  #### utilities ####
  # counters
  dicts = {}
  dicts["friendlyPlayerCounter"] = 0
  dicts["hostilePlayerCounter"] = 0
  dicts["minionCount"] = 0
  dicts["hearthstone_internal_id_count"] = 0
  dicts["Location_Friendly_Deck_count"] = 0
  dicts["Location_Friendly_Hand_count"] = 0
  dicts["Location_Friendly_Board_count"] = 0
  dicts["Location_Friendly_Graveyard_count"] = 0
  dicts["Location_Hostile_Deck_count"] = 0
  dicts["Location_Hostile_Hand_count"] = 0
  dicts["Location_Hostile_Board_count"] = 0
  dicts["Location_Hostile_Graveyard_count"] = 0

  #heroes
  heroes = {}
  heroes["Jaina Proudmoore"] = "Mage"
  heroes["Rexxar"] = "Hunter"
  heroes["Uther Lightbringer"] = "Paladin"
  heroes["Garrosh Hellscream"] = "Warrior"
  heroes["Malfurion Stormrage"] = "Druid"
  heroes["Gul'dan"] = "Warlock"
  heroes["Thrall"] = "Shaman"
  heroes["Anduin Wrynn"] = "Priest"
  heroes["Valeera Sanguinar"] = "Rogue"




  # initialization
  game0 = createNode(top, "Game0")
  createRelation(top, game0, "is_a", getNode(top, "Game"))
  gameSetup = createNode(top, "GameSetup")
  createRelation(top, gameSetup, "is_a", getNode(top, "Turn"))
  friendlyPlayer = createNode(top, "FriendlyPlayer_{0}".format(dicts["friendlyPlayerCounter"]))
  hostilePlayer = createNode(top, "HostilePlayer_{0}".format(dicts["hostilePlayerCounter"]))
  friendly_player_node = getNode(top, "Friendly_Player")
  hostile_player_node = getNode(top, "Hostile_Player")
  createRelation(top, friendlyPlayer, "is_a", friendly_player_node)
  createRelation(top, hostilePlayer, "is_a", hostile_player_node)
  createRelation(top, game0, "has", friendlyPlayer)
  createRelation(top, game0, "has", hostilePlayer)

  zones = {
    "FRIENDLY DECK" : "Location_Friendly_Deck",
    "FRIENDLY HAND": "Location_Friendly_Hand",
    "FRIENDLY PLAY": "Location_Friendly_Board",
    "FRIENDLY GRAVEYARD": "Location_Friendly_Graveyard",
    "OPPOSING DECK": "Location_Hostile_Deck",
    "OPPOSING HAND": "Location_Hostile_Hand",
    "OPPOSING PLAY": "Location_Hostile_Board",
    "OPPOSING GRAVEYARD": "Location_Hostile_Graveyard",
    "FRIENDLY PLAY (Hero)": "Location_Friendly_Play_Hero",
    "FRIENDLY PLAY (Hero Power)": "Location_Friendly_Play_Hero_Power",
    "OPPOSING PLAY (Hero)": "Location_Hostile_Play_Hero",
    "OPPOSING PLAY (Hero Power)": "Location_Hostile_Play_Hero_Power",
  }

  nextLine = goToNextPhrase(file, "TRANSITIONING")

  minion_type = ""
 # set up of initial game state
  while nextLine != -1 and minion_type != "The Coin":
    minionCount = getAndIncreaseCurrentMinionCount(top)

    nextLine = nextLine.split("TRANSITIONING card [", 1)[1]
    lineEnd = nextLine.split("] to ", 1)[1][:-1]
    valuePairs = parseValues(nextLine)

    # Todo hash table for minion_nodes

    minion_id = valuePairs["id"]
    minion_node = getOrCreateNode(top, "Minion_{0}".format(minionCount))
    # create node "Hearthstone internal id" -> relation
    # if hash table doesn't contain minion_id then create a new entry as well as a new "hearthstone internal id" node
    minion_node.createAttribute(NodeAttributeType("id"), minion_id)
    if(top.existsNodeByName("{0}_0".format(zones[lineEnd]))):
      targetZone = top.getNodeByName("{0}_0".format(zones[lineEnd]))
    else:
      targetZone = createNode(top, "{0}_0".format(zones[lineEnd]))
      targetZone_node = getNode(parent, zones[lineEnd])
      createRelation(top, targetZone, "is_a", targetZone_node)
    createRelation(top, targetZone, "has", minion_node)
    if "name" in valuePairs.keys():
      minion_type = valuePairs["name"]
      minion_type_node = getNode(parent, minion_type)
      if minion_type_node is None:
        minion_type_node = getNode(parent, heroes[minion_type])
      createRelation(top, minion_node, "is_a", minion_type_node)

    nextLine = goToNextPhrase(file, "TRANSITIONING")

    #Todo: detect initialization end
      # when "The Coin" is transitioned the initialization is over
    #Todo: detect turn end
    #Todo: implement turn construct (has relations,...)
    #Todo: create was_a relations

  return top





def goToNextPhrase(file, phrase):
  for  i, line in enumerate(file, 1):
    if phrase in line:
      return line
  return -1

def parseValues(segment):
  dictionary = {}
  value = ""
  key = ""
  keybuffer = ""

  for char in list(segment):
    if char is "=":
      for c in reversed(value):
        if c is " ":
          value = value[:-1]
          break
        keybuffer = c + keybuffer
        value = value[:-1]
      if not value == "":
        if value.isdigit():
          value = int(value)
        dictionary[key] = value
      key = keybuffer
      keybuffer = ""
      value = ""
    else:
      value += char

  if value.isdigit():
    value = int(value)
  if not key is "" or not value is "":
    dictionary[key] = value

  return dictionary

def createNode(topology, nodeName):
  n = Node(nodeName)
  if topology.existsNode(n):
    AssertionError("Node {0} is already existing in the topology or its parent".format(n.name))
  topology.insertNode(n)
  return n

def getNode(topology, nodeName):
  if not topology.existsNodeByName(nodeName):
    return None
  return topology.getNodeByName(nodeName)

def getOrCreateNode(topology, nodeName):
  n = getNode(topology, nodeName)
  if n is not None:
    return n
  else:
    return createNode(topology, nodeName)

def createRelation(topology, source, relationType, target, attributeType = None, attributeValue = None):
  relationtype = RelationType(relationType)
  relation = Relation(relationtype, source, target)
  if attributeType != None:
    relationAttributeType = RelationAttributeType(attributeType)
    relation.createAttribute(relationAttributeType, attributeValue)
  topology.insertRelation(relation)

def getAndIncreaseCurrentMinionCount(topology):
  node = getNode(topology, "MinionCount")
  if node is None:
    assert("Node 'MinionCount' is missing in the given topology!")
  count = node.getAttributeValue(NodeAttributeType("amount"))
  if count is None:
    assert("Node 'MinionCount' is missing attribute 'amount'!")
  node.setAttributeValue(NodeAttributeType("amount"), count + 1)
  return count
