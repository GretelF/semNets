from collections import namedtuple

relationTypes = {}
attributeTypes = {}

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
    a = Attribute(type, self, value)
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
    a = Attribute(type, self, value)
    self.attributes.append(a)
    return a

class Attribute:
  def __init__(self, type, target, value):
    self.type = type
    self.value = value

  def __str__(self):
    return "{}: {}".format(self.type, self.value)

  def __repr__(self):
    return "Attribute(type = '{}', value = '{}')".format(self.type, self.value)

  def __eq__(self, other):
    return self.type == other.type and self.value == value
