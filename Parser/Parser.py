import json
from semNets.Topology import Topology
from semNets.Primitives import Node, Relation, RelationAttributeType, RelationType, Attribute


def parseLog(file, parent):
  counter = 0
  current_linenumber = 0
  test = ""
  top = Topology()
  top.setParent(parent)

  #### utilities ####
  utilities = {
  # counters
    "counters" : {
      "friendlyPlayerCounter": 0,
      "hostilePlayerCounter": 0,
      "minionCount": 0,
      "hearthstone_internal_id_count": 0,
      "Location_Friendly_Deck_count": 0,
      "Location_Friendly_Hand_count": 0,
      "Location_Friendly_Board_count": 0,
      "Location_Friendly_Graveyard_count": 0,
      "Location_Hostile_Deck_count": 0,
      "Location_Hostile_Hand_count": 0,
      "Location_Hostile_Board_count": 0,
      "Location_Hostile_Graveyard_count": 0,
      "Location_Friendly_Play_Weapon_count": 0,
      "Location_Hostile_Play_Weapon_count": 0,
      "Location_Hostile_Secrets_count": 0,
      "Location_Friendly_Secrets_count": 0
    },

    # heroes
    "heroes" : {
      "Jaina Proudmoore": "Mage",
      "Rexxar": "Hunter",
      "Uther Lightbringer": "Paladin",
      "Garrosh Hellscream": "Warrior",
      "Malfurion Stormrage": "Druid",
      "Gul'dan": "Warlock",
      "Thrall": "Shaman",
      "Anduin Wrynn": "Priest",
      "Valeera Sanguinar": "Rogue"
    },

    # zones
    "zones" : {
      "FRIENDLY DECK": "Location_Friendly_Deck",
      "FRIENDLY HAND": "Location_Friendly_Hand",
      "FRIENDLY PLAY": "Location_Friendly_Board",
      "FRIENDLY GRAVEYARD": "Location_Friendly_Graveyard",
      "OPPOSING DECK": "Location_Hostile_Deck",
      "OPPOSING HAND": "Location_Hostile_Hand",
      "OPPOSING PLAY": "Location_Hostile_Board",
      "OPPOSING GRAVEYARD": "Location_Hostile_Graveyard",
      "FRIENDLY PLAY (Hero)": "Location_Friendly_Play_Hero",
      "FRIENDLY PLAY (Hero Power)": "Location_Friendly_Play_Hero_Power",
      "FRIENDLY PLAY (Weapon)": "Location_Friendly_Play_Weapon",
      "FRIENDLY SECRET": "Location_Friendly_Secrets",
      "OPPOSING PLAY (Hero)": "Location_Hostile_Play_Hero",
      "OPPOSING PLAY (Hero Power)": "Location_Hostile_Play_Hero_Power",
      "OPPOSING PLAY (Weapon)": "Location_Hostile_Play_Weapon",
      "OPPOSING SECRET": "Location_Hostile_Secrets"
    },
    "current_locations": {
      "Location_Friendly_Deck": None,
      "Location_Friendly_Hand": None,
      "Location_Friendly_Board": None,
      "Location_Friendly_Graveyard": None,
      "Location_Hostile_Deck": None,
      "Location_Hostile_Hand": None,
      "Location_Hostile_Board": None,
      "Location_Hostile_Graveyard": None
    },

    "current_locations_filled" : {
      "Location_Friendly_Deck": [],
      "Location_Friendly_Hand": [],
      "Location_Friendly_Board": [],
      "Location_Friendly_Graveyard": [],
      "Location_Hostile_Deck": [],
      "Location_Hostile_Hand": [],
      "Location_Hostile_Board": [],
      "Location_Hostile_Graveyard": []
    },


    # this dictionary maps a minion_id to an actual minion node, which may change every turn
    # a was_a relation is created if the minion changes
    "minion_history" : {},

    # this dictionary maps a minion_id to its type
    "minion_type" : {},

    # this dictionary maps a minion to their current health in order to calculate it more easily
    "minion_health" : {},
    "minion_damage" : {},

    ### utilities ###
    "current_player" : -1,
    "zones_used_in_this_turn" : {},
    "current_turn" : 1,
    "current_turn_node" : None,
    "current_subturn" : 0,
    "current_subturn_node" : None
  }


  # initialization
  game0 = createNode(top, "Game0")
  createRelation(top, game0, "is_a", getNode(top, "Game"))
  #this is the initial turn
  gameSetup = createNode(top, "GameSetup")
  createRelation(top, gameSetup, "is_a", getNode(top, "Turn"))
  utilities["current_turn_node"] = gameSetup
  subturn0 = createNode(top, "SubTurn_0")
  createRelation(top, subturn0, "is_a", getNode(top, "Subturn"))
  createRelation(top, gameSetup, "has", subturn0)
  utilities["current_subturn_node"] = subturn0
  utilities["current_subturn"] = 1

  friendlyPlayer = createNode(top, "FriendlyPlayer_{0}".format(utilities["counters"]["friendlyPlayerCounter"]))
  hostilePlayer = createNode(top, "HostilePlayer_{0}".format(utilities["counters"]["hostilePlayerCounter"]))
  friendly_player_node = getNode(top, "Friendly_Player")
  hostile_player_node = getNode(top, "Hostile_Player")
  createRelation(top, friendlyPlayer, "is_a", friendly_player_node)
  createRelation(top, hostilePlayer, "is_a", hostile_player_node)
  createRelation(top, game0, "has", friendlyPlayer)
  createRelation(top, game0, "has", hostilePlayer)



  nextLine, phrase, current_linenumber = goToNextPhrases(file, ["TRANSITIONING"], current_linenumber)

  minion_type = ""
 # set up of initial game state
 # detect initialization end: when "The Coin" is transitioned the initialization is over
  while nextLine != -1 and minion_type != "The Coin":
    minionCount = utilities["counters"]["minionCount"]


    nextLine = nextLine.split("TRANSITIONING card [", 1)[1]
    lineEnd = nextLine.split("] to ", 1)[1][:-1]
    valuePairs = parseValues_Transitioning(nextLine)

    minion_id = valuePairs["id"]
    minion_node_name = "Minion_{0}".format(minionCount)
    minion_node = getOrCreateNode(top,minion_node_name)

    hearthstone_internal_card_id_node = createNode(top, "hearthstone_internal_card_id_{0}".format(minion_id))
    createRelation(top, minion_node, "has", hearthstone_internal_card_id_node)
    #TODO link to static network -> hearthstone_internal_card_id_XX - is_a - hearthstone_internal_card_id

    #add minion to the minion_history dict
    utilities["minion_history"][minion_id] = minion_node

    if(top.existsNodeByName("{0}_0".format(utilities["zones"][lineEnd]))):
      targetZone = top.getNodeByName("{0}_0".format(utilities["zones"][lineEnd]))
    else:
      targetZone = createNode(top, "{0}_0".format(utilities["zones"][lineEnd]))
      targetZone_node = getNode(parent, utilities["zones"][lineEnd])
      createRelation(top, targetZone, "is_a", targetZone_node)
      #update counter
      utilities["counters"][utilities["zones"][lineEnd]+"_count"] = 1
    createRelation(top, targetZone, "has", minion_node)
    if "name" in valuePairs.keys():
      minion_type = valuePairs["name"]
      minion_type_node = getNode(parent, minion_type)
      if minion_type_node is None:
        minion_type_node = getNode(parent, utilities["heroes"][minion_type])
        minion_health = 30
        utilities["minion_health"][minion_id] = minion_health
        utilities["minion_damage"][minion_id] = 0
        minion_curhealth_rel = createRelation(top, minion_node, "has", getNode(parent, "CurHealth"))
        minion_curhealth_rel.createAttribute(RelationAttributeType("amount"), minion_health)
      else:
        minion_health_rel = getRelation(parent, minion_type, "has", "MaxHealth")
        if minion_health_rel is None:
          #TODO: make it a spell
          print("Minion '{}' has no maxhealth. -> is no minion".format(minion_type))
        else:
          assert (minion_health_rel is not None, "{0} has no attribute 'MaxHealth'!")
          minion_health = minion_health_rel.getAttributeValue(RelationAttributeType("amount"))
          utilities["minion_health"][minion_id] = minion_health
          utilities["minion_damage"][minion_id] = 0
          createRelation(top, minion_node, "has", getNode(parent, "CurHealth"), RelationAttributeType("amount"), minion_health)

      utilities["minion_type"][minion_id] = minion_type_node
      createRelation(top, minion_node, "is_a", minion_type_node)

    else:
      utilities["minion_type"][minion_id] = None

    minionCount = minionCount + 1
    utilities["counters"]["minionCount"] = minionCount

    if minion_type == "The Coin":
      print("The Coin passed")
    nextLine, phrase, current_linenumber = goToNextPhrases(file, ["TRANSITIONING"], current_linenumber)



  nextLine, phrase, current_linenumber = goToNextPhrases(file, ["TRANSITIONING", "BlockType=ATTACK", "tag=DAMAGE"], current_linenumber)
  #normal game play starts here
  while nextLine != -1 and "CREATE_GAME" not in nextLine:
    utilities, top = functions[phrase](nextLine, utilities, top)
    nextLine, phrase, current_linenumber = goToNextPhrases(file, ["TRANSITIONING", "BlockType=ATTACK", "tag=DAMAGE", "CREATE_GAME"], current_linenumber)


  return top


def goToNextPhrases(file, phrases, current_linenumber):
  for  i, line in enumerate(file, 1):
    print("Line {}".format(current_linenumber))
    current_linenumber += 1
    for phrase in phrases:
      if "PowerTaskList.DebugPrintPower()" in line:
        break
      if phrase in line:
        return line, phrase, current_linenumber
  return -1, "", current_linenumber


def ProcessPhrase_Transition(org_line, utilities, topology):
  line = org_line.split("TRANSITIONING card [", 1)[1]
  lineEnd = line.split("] to ", 1)[1][:-1]
  while lineEnd == "":
    return utilities, topology

  zone = utilities["zones"][lineEnd]
  valuePairs = parseValues_Transitioning(line)

  new_player = valuePairs["player"]
  #check if new Turn is needed
  if new_player != utilities["current_player"]:
    utilities, topology = startNewTurn(utilities, topology)

  #since transitions are also subturns, create new subturn

  newSubturn = createNode(topology, "SubTurn_{}".format(utilities["current_subturn"]))
  createRelation(topology, newSubturn, "is_a", getNode(topology, "Subturn"))
  if not utilities["current_subturn_node"] is None:
    createRelation(topology, newSubturn, "was", utilities["current_subtturn_node"])
  utilities["current_subturn"] += 1
  utilities["current_subturn_node"] = newSubturn

  minionCount = utilities["counters"]["minionCount"]
  utilities["counters"]["minionCount"] = minionCount + 1

  minion_id = valuePairs["id"]
  minion_node_name = "Minion_{0}".format(minionCount)
  minion_node = getNode(topology, minion_node_name)

  if minion_node is None:
    minion_node = createNode(topology, minion_node_name)
    hearthstone_internal_card_id_node = getOrCreateNode(topology, "hearthstone_internal_card_id_{0}".format(minion_id))
    createRelation(topology, minion_node, "has", hearthstone_internal_card_id_node)

  # create relation to previous state of the minion if it existed before
  if minion_id in utilities["minion_history"].keys():
    previous = utilities["minion_history"][minion_id]
    createRelation(topology, minion_node, "was", previous)
    utilities["minion_history"][minion_id] = minion_node
  else:
    utilities["minion_history"][minion_id] = minion_node

  # create new Zone instance if neccessary
  current_zone_name = "{0}_{1}".format(zone, utilities["counters"][zone + "_count"])
  if current_zone_name in utilities["zones_used_in_this_turn"].keys():
    targetZone = utilities["zones_used_in_this_turn"][current_zone_name]
  else:
    targetZone = createNode(topology, current_zone_name)
    pastZone = getNode(topology, "{0}_{1}".format(zone, utilities["counters"][zone + "_count"] - 1))
    if pastZone is None:
      parentZone = getNode(topology.parent, utilities["zones"][lineEnd])
      createRelation(topology, targetZone, "is_a", parentZone)
    else:
      createRelation(topology, targetZone, "was", pastZone)
    # update counter
    utilities["counters"][zone + "_count"] = utilities["counters"][zone + "_count"] + 1
    utilities["zones_used_in_this_turn"][current_zone_name] = targetZone
  createRelation(topology, targetZone, "has", minion_node)
  #associate targetZone with current subturn
  createRelation(topology, newSubturn, "has", targetZone)
  #update the current_locations dicts
  if not zone in ["Location_Friendly_Play_Hero", "Location_Hostile_Play_Hero", "Location_Hostile_Play_Hero_Power", "Location_Friendly_Play_Hero_Power", "Location_Friendly_Play_Weapon", "Location_Hostile_Play_Weapon", "Location_Friendly_Secrets", "Location_Hostile_Secrets"] :
    utilities["current_locations_filled"][zone].append(minion_node)
    utilities["current_locations"][zone] = targetZone

  if "name" in valuePairs.keys():
    minion_type = valuePairs["name"]
    minion_type_node = getNode(topology.parent, minion_type)
    if minion_type_node is None:
      minion_type_node = getNode(topology.parent, utilities["heroes"][minion_type])
    createRelation(topology, minion_node, "is_a", minion_type_node)

    # when the minion is not in the dict "minion_type", then it must be a new one, that hasen't been in the game yet.
    if minion_id not in utilities["minion_type"].keys() or utilities["minion_type"][minion_id] is None :
      utilities["minion_type"][minion_id] = minion_type_node
      #get the relation that indicates how much maxhealth a minion has (from static network)
      minion_maxhealth_rel = getRelation(topology.parent, minion_type, "has", "MaxHealth")
      # this relation should exist otherwise -> error
      if minion_maxhealth_rel is None:
        print("minion '{}' has no maxhealth -> is no minion".format(minion_type))
      else:
        assert (minion_maxhealth_rel is not None, "{0} has no attribute 'MaxHealth'!")
        # now get the actual amount of health from the relation and set it in the minion_health dict
        minion_health = minion_maxhealth_rel.getAttributeValue(RelationAttributeType("amount"))
        utilities["minion_health"][minion_id] = minion_health
        utilities["minion_damage"][minion_id] = 0
        #create relation from current minion node to CurHealth (static node)
        minion_curhealth_rel = createRelation(topology, minion_node, "has", getNode(topology.parent, "CurHealth"))
        #this relation should have the current health, i.e. the maxhealth at this point, as an amount
        minion_curhealth_rel.createAttribute(RelationAttributeType("amount"), minion_health)

  return utilities, topology

def ProcessPhrase_Attack(org_line, utilities, topology ):
  line = org_line.split("BLOCK_START BlockType=ATTACK ", 1)[1]
  valuePairs = parseValues_Nested(line)
  source_minion_id = valuePairs["Entity"]["id"]
  target_minion_id = valuePairs["Target"]["id"]

  if source_minion_id not in utilities["minion_history"].keys():
    #TODO: what about Lord Jaraxxus? The minion_id doesn't show up, because it changes mid game in an attack block(e.g. from 35 to 98)
    print("source_minion_id {0} not in minion_history!".format(source_minion_id))
    return utilities, topology
  source_minion_node_old = utilities["minion_history"][source_minion_id]
  target_minion_node_old = utilities["minion_history"][target_minion_id]
  currentMinion_count = utilities["counters"]["minionCount"]
  source_minion_node_new = createNode(topology, "Minion_{}".format(currentMinion_count))
  currentMinion_count += 1
  target_minion_node_new = createNode(topology, "Minion_{}".format(currentMinion_count))
  utilities["counters"]["minionCount"] = currentMinion_count + 1

  createRelation(topology, source_minion_node_new, "was", source_minion_node_old)
  createRelation(topology, target_minion_node_new, "was", target_minion_node_old)

  utilities["minion_history"][source_minion_id] = source_minion_node_new
  utilities["minion_history"][target_minion_id] = target_minion_node_new


  new_player = valuePairs["Entity"]["player"]
  if new_player != utilities["current_player"]:
    utilities, topology = startNewTurn(utilities, topology)

  newSubturn = createNode(topology, "SubTurn_{}".format(utilities["current_subturn"]))
  utilities["current_subturn"] += 1
  createRelation(topology, newSubturn, "is_a", getNode(topology.parent, "Subturn"))
  if not utilities["current_subturn_node"] is None:
    createRelation(topology, newSubturn, "was", utilities["current_subturn_node"])
  utilities["current_subturn_node"] = newSubturn
  createRelation(topology, newSubturn, "has", getNode(topology.parent, "Action_MinionAttack"))
  createRelation(topology, newSubturn, "has", source_minion_node_new)
  createRelation(topology, source_minion_node_new, "is_a", getNode(topology.parent, "Action_MinionAttack_Source"))
  createRelation(topology, newSubturn, "has", target_minion_node_new)
  createRelation(topology, target_minion_node_new, "is_a", getNode(topology.parent, "Action_MinionAttack_Target"))


  return utilities, topology


def ProcessPhrase_Damage(org_line, utilities, topology ):
  if "processing" in org_line:
    return utilities, topology
  line = org_line.split("TAG_CHANGE ", 1)[1]
  valuePairs = parseValues_Nested(line)

  if "Entity" not in valuePairs.keys():
    print("ERROR")
  new_player = valuePairs["Entity"]["player"]
  if new_player != utilities["current_player"]:
    utilities, topology = startNewTurn(utilities, topology)

  minion_id = valuePairs["Entity"]["id"]
  minion_type = valuePairs["Entity"]["name"]
  if minion_id not in utilities["minion_history"].keys():
    print("WARINING: tag change on nonexistend minion {}".format(minion_type))
  minion_node = utilities["minion_history"][minion_id]
  damage = int(valuePairs["value"])
  health = utilities["minion_health"][minion_id]
  utilities["minion_damage"][minion_id] = damage
  createRelation(topology, minion_node, "has", getNode(topology.parent, "CurHealth"), "amount", health - damage )
  return utilities, topology

def ProcessPhrase_Health(org_line, utlities, topology):
  return

def startNewTurn(utilities, topology):
  # new turn starts
  newTurn = createNode(topology, "Turn_{}".format(utilities["current_turn"]))
  utilities["current_turn"] += 1

  createRelation(topology, newTurn, "is_a", getNode(topology, "Turn"))
  createRelation(topology, newTurn, "was", utilities["current_turn_node"])
  utilities["current_turn_node"] = newTurn
  for location, location_node in utilities["current_locations"].items():
    # create new location, that is logically just a copy of the location in the las subturn,
    # however it will have a relation to every minion associated with this location at the time of the turn
    location_count = utilities["counters"]["{0}_count".format(location)]
    new_location = createNode(topology, "{0}_{1}".format(location, location_count))
    utilities["counters"]["{0}_count".format(location)] = location_count + 1

    if not location_node is None:
      createRelation(topology, new_location, "was", location_node)
    # update the utilities section for the current location, so that future subturns reference this new location
    utilities["current_locations"][location] = new_location
    for minion in utilities["current_locations_filled"][location]:
      createRelation(topology, new_location, "has", minion)

    createRelation(topology, newTurn, "has", new_location)

  utilities["current_subturn_node"] = None
  utilities["zones_used_in_this_turn"].clear()
  return utilities, topology

def parseValues_segment(segment):
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
        if value.lstrip("-").isdigit():
          value = int(value)
        dictionary[key] = value
      key = keybuffer
      keybuffer = ""
      value = ""
    else:
      value += char

  if value.lstrip("-").isdigit():
    value = int(value)
  if not key is "" or not value is "":
    dictionary[key] = value

  return dictionary

def parseValues_Transitioning(segment):
  return parseValues_segment(segment)

def parseValues_Nested(segment):
  dictionary = {}
  value = ""
  key = ""
  keybuffer = ""
  index = 0
  valuedict = {}
  peeking = False
  peekchar = ""
  peekbuffer = ""

  for char in list(segment):
    if peeking:
      if char == "]":
        dictionary[key] = parseValues_segment(peekbuffer)
        peekbuffer = ""
        key = ""
        peeking = False
      else:
        peekbuffer += char
    elif char == "[":
      peeking = True
    elif char is "=":
      for c in reversed(value):
        if c is " ":
          value = value[:-1]
          break
        keybuffer = c + keybuffer
        value = value[:-1]
      if not value == "":
        if value.lstrip("-").isdigit():
          value = int(value)
        dictionary[key] = value
      key = keybuffer
      keybuffer = ""
      value = ""
    else:
      value += char
    index += 1


  if value.lstrip("-").isdigit():
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

def getRelation(topology, source, relationtype, target):
  for relation in topology.relations:
    if relation.source == Node(source) and relation.target == Node(target) and relation.type == RelationType(relationtype):
      return relation
  return None

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
  return relation



functions = {
  "TRANSITIONING" : ProcessPhrase_Transition,
  "BlockType=ATTACK" : ProcessPhrase_Attack,
  "tag=DAMAGE" : ProcessPhrase_Damage
}

