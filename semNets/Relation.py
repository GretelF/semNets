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

def RelationType(name):
  """
  HAX(!)
  if relationType already exists returns existing instance, else returns new instance and adds it to relationTypes dictionary
  """
  return relationTypes.setdefault(name, NamedTypeBase(name, "RelationType"))

def AttributeType(name):
  """
  HAX(!)
  if attributeType already exists returns existing instance, else returns new instance and adds it to attributeTypes dictionary
  """
  return attributeTypes.setdefault(name, NamedTypeBase(name, "AttributeType"))

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

  def createAttribute(self, type, value):
    a = Attribute(type, self, value)
    self.attributes.append(a)
    return a

class Attribute:
  def __init__(self, type, relation, value):
    self.type = type
    self.relation = relation
    self.value = value

  def __str__(self):
    return "{} with {}: {}".format(self.relation, self.type, self.value)

  def __repr__(self):
    return "Attribute(type = '{}', relation = '{}', value = '{}')".format(self.type, self.relation, self.value)
