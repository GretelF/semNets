from collections import namedtuple
import scipy.spatial.distance as sci

relationTypes = {}
attributeTypes = {}


def euclideanDistance(u, v):
  sumSq=0.0

  #add up the squared differences
  for i in range(len(u)):
    sumSq+=(u[i]-v[i])**2

  #take the square root of the result
  return (sumSq**0.5)



class NamedTypeBase:
  def __init__(self, name, typeName):
    self.name = name
    self.typeName = typeName

  def __str__(self):
    return self.name

  def __repr__(self):
    return "{}(name = '{}')".format(self.typeName, self.name)

  def __eq__(self, other):
    return self is other

def RelationType(name):
  """
  HAX(!)
  if relationType already exists returns existing instance, else returns new instance and adds it to relationTypes dictionary
  """
  return relationTypes.setdefault(name, NamedTypeBase(name, "RelationType"))

def RelationAttributeType(name):
  """
  HAX(!)
  if attributeType already exists returns existing instance, else returns new instance and adds it to attributeTypes dictionary
  """
  return attributeTypes.setdefault(name, NamedTypeBase(name, "RelationAttributeType"))

def NodeAttributeType(name):
  """
  HAX(!)
  if attributeType already exists returns existing instance, else returns new instance and adds it to attributeTypes dictionary
  """
  return attributeTypes.setdefault(name, NamedTypeBase(name, "NodeAttributeType"))


class Node :
  def __init__(self, name):
    self.name = name
    self.attributes = []

  def __str__(self):
    return str(self.name)

  def __repr__(self):
    return "Node(name = '{}')".format(self.name)

  def createAttribute(self, type, value):
    a = Attribute(type, value)
    self.attributes.append(a)
    return a

  def __eq__(self, other):
    return self.name == other.name


class Relation:
  def __init__(self, type, source, target):
    self.type = type
    self.source = source
    self.target = target
    self.attributes = []

  def __str__(self):
    return "{} {} {}".format(self.source, self.type, self.target)

  def __repr__(self):
    return "Relation(type = '{}', source = '{}', target = '{}')".format(self.type, self.source, self.target)

  def __eq__(self, other):
    return self.type == other.type and \
           self.source == other.source and \
           self.target == other.target and \
           self.attributes == other.attributes


  def createAttribute(self, type, value):
    for attr in self.attributes:
      assert type != attr.type

    a = Attribute(type, value)
    self.attributes.append(a)
    return a

  def hasAttribute(self, attr):
    return attr in self.attributes

  def hasAttributeOfType(self, type):
    for attr in self.attributes:
      if attr.type == type:
        return True
    return False

  def getAttributeValue(self, type):
    for attr in self.attributes:
      if attr.type == type:
        return attr.value
    return None

  def calculateAttributeDistance(self, other, wMissingAttribute = 0.25, wDifferentStringValue = 0.25):
    dist = 0

    # attribute similarity
    selftypes = []
    selfvalues = []
    othertypes = []
    othervalues = []

    for attr in self.attributes:
      if other.hasAttributeOfType(attr.type):
        selftypes.append(attr.type)
        othertypes.append(attr.type)
        selfvalues.append(attr.value)
        othervalues.append(other.getAttributeValue(attr.type))
      else:
        dist += wMissingAttribute

    for attr in other.attributes:
      if not self.hasAttributeOfType(attr.type):
        dist += wMissingAttribute

    # deal with the str values (-> add error weight to dist if different)
    for i in range(len(selfvalues)):
      if type(selfvalues[i]) is str or type(othervalues[i]) is str:
        if selfvalues[i] != othervalues[i]:
          dist += wDifferentStringValue
        selfvalues[i] = 0
        othervalues[i] = 0
    dist += euclideanDistance(selfvalues, othervalues)
    return dist

  def calculateDistance(self, other, wAttr = 0.25, wSource = 0.25, wTarget = 0.25, wType = 0.25, wMissingAttribute = 0.25, wDifferentStringValue = 0.25):
    dif = 0

    if self.type != other.type:
      dif += wType
    if self.source != other.source:
      dif += wSource
    if self.target != other.target:
      dif += wTarget
    dif += self.calculateAttributeDistance(other, wMissingAttribute, wDifferentStringValue) * wAttr
    return dif


class Attribute:
  def __init__(self, type, value):
    self.type = type
    self.value = value

  def __str__(self):
    return "{}: {}".format(self.type, self.value)

  def __repr__(self):
    return "Attribute(type = '{}', value = '{}')".format(self.type, self.value)

  def __eq__(self, other):
    return self.type == other.type and self.value == other.value
