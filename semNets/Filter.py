from semNets.Primitives import Node, Relation, RelationType, RelationAttributeType, Attribute
from semNets.Topology import Topology

conditionTypes = {}

def conditionType(name):
  def wrapper(func):
    conditionTypes[name] = func
    return func
  return wrapper

@conditionType("missingAllRelations")
def makeMissingAllRelations(data):

  def missingAllRelations(topology, node):
    for rel in data:
      type = RelationType(rel["type"])
      target = Node(rel["target"])
      attrs = [Attribute(RelationAttributeType(a["type"]), a["value"]) for a in rel["attributes"]]
      relations = [r for r in topology.relations if r.source == node]

      for r in relations:
        # if a relation is found, that does exist within the topology: return False
        if r.type == type and r.target == target and all(r.hasAttribute(a) for a in attrs):
          return False
    # if none of the given relations is found within the topology: return True
    return True

  return missingAllRelations

@conditionType("missingAnyRelation")
def makeMissingAnyRelation(data):

  def missingAnyRelation(topology, node):
    for rel in data:
      type = RelationType(rel["type"])
      target = Node(rel["target"])
      attrs = [Attribute(RelationAttributeType(a["type"]), a["value"]) for a in rel["attributes"]]
      relationInRelationList = False                                                                    # Flag

      relation = [r for r in topology.relations if r.source == node]
      for r in relations:
        if r.type == type or r.target == target or any(r.hasAttribute(a) for a in attrs):
          relationInRelationList = True
          break

      # If a relation is found, that does not exist within the topology: return True
      if not relationInRelationList:
        return True
    # It the topology is not missing any of the given relations: return False
    return False

  return missingAnyRelation


@conditionType("hasAllRelations")
def makeHasAllRelations(data):
  def hasAllRelations(topology, node):
    for rel in data:
      type = RelationType(rel["type"])
      target = Node(rel["target"])
      attrs = [Attribute(RelationAttributeType(a["type"]), a["value"]) for a in rel["attributes"]]
      relations = [r for r in topology.relations if r.source == node]

      relationInRelationList = False
      for r in relations:
        if r.type == type and r.target == target and all(r.hasAttribute(a) for a in attrs):
          relationInRelationList = True

      # if the current relation does not exist within the topology: return False
      if not relationInRelationList:
        return False
    # if none of the given relations is missing in the topology: return True
    return True

  return hasAllRelations

@conditionType("hasAnyRelation")
def makeHasAnyRelation(data):
  def hasAnyRelation(topology, node):
    for rel in data:
      type = RelationType(rel["type"])
      target = Node(rel["target"])
      attrs = [Attribute(RelationAttributeType(a["type"]), a[value]) for a in rel["attributes"]]
      relations = [r for r in topology.relations if r.source == node]

      for r in relations:
        if r.type == type and r.target == target and all(r.hasAttribute(a) for a in attrs):
          return True
    return False

  return hasAnyRelation



def translate(data):

  conditionFuncs = []
  for ct in data.keys():
    maker = conditionTypes[ct]
    conditionFuncs.append(maker(data[ct]))

  def check(topology, node):
    return all(func(topology, node) for func in conditionFuncs)

  return check






