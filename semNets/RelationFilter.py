from semNets.Primitives import Node, Relation, RelationType, RelationAttributeType, Attribute
from semNets.Topology import Topology

conditionTypes = {}

def conditionType(name):
  def wrapper(func):
    conditionTypes[name] = func
    return func
  return wrapper

@conditionType("missingAllAttributes")
def makeMissingAllAttributes(data):
  def missingAllAttributes(topology, relation):
    for attr in data:
      type = RelationAttributeType(attr["type"]) if attr["type"] != None else None
      value = attr["value"]

      for attribute in relation.attributes:
        if (type == None or attribute.type == type) and (value == None or attribute.value == value):
            return False
    return True

  return missingAllAttributes

@conditionType("missingAnyAttribute")
def makeMissingAnyAttribute(data):
  def missingAnyAttribute(topology, relation):
    for attr in data:
      type = RelationAttributeType(attr["type"]) if attr["type"] != None else None
      value = attr["value"]
      attributeInAttributeList = False                                                                    # Flag

      for attribute in relation.attributes:
        if (type != None and attribute.type == type) or (value != None and attribute.value == value):
          attributeInAttributeList = True
          break

      # If an attribute is found, that does not exist within the relation: return True
      if not attributeInAttributeList:
        return True
    # It the relation is not missing any of the given attributes: return False
    return False

  return missingAnyAttribute


@conditionType("hasAllAttributes")
def makeHasAllAttributes(data):
  def hasAllAttributes(topology, relation):
    for attr in data:
      type = RelationAttributeType(attr["type"]) if attr["type"] != None else None
      value = attr["value"]
      attributeInAttributeList = False
      for attribute in relation.attributes:
        if (type == None or attribute.type == type) and (value == None or attribute.value == value):
          attributeInAttributeList = True

      # if the current attribute does not exist within the relation: return False
      if not attributeInAttributeList:
        return False
    # if none of the given attributes is missing in the relation: return True
    return True
  return hasAllAttributes

@conditionType("hasAnyAttribute")
def makeHasAnyAttribute(data):
  def hasAnyAttribute(topology, relation):
    for attr in data:
      type = RelationAttributeType(attr["type"]) if attr["type"] != None else None
      value = attr["value"]

      for attribute in relation.attributes:
        if (type == None or attribute.type == type) and (value == None or attribute.value == value):
          return True
    return False
  return hasAnyAttribute



def translate(data):

  conditionFuncs = []
  for ct in data.keys():
    maker = conditionTypes[ct]
    conditionFuncs.append(maker(data[ct]))

  def check(topology, node):
    return all(func(topology, node) for func in conditionFuncs)

  return check






