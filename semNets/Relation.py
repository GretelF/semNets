relationTypes = {}

def RelationType(name):
  """
  HAX(!)
  if relationType already exists returns existing instance, else returns new instance and adds it to relationTypes dictionary
  """
  return relationTypes.setdefault(name, _RelationType(name))

class _RelationType:
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return self.name

  def __repr__(self):
    return "RelationType(name = {})".format(repr(self.name))


class Relation:
  def __init__(self, type, source, target):
    self.type = type
    self.source = source
    self.target = target

  def __str__(self):
    return "{} {} {}".format(self.source, self.type, self.target)

  def __repr__(self):
    return "Relation(type = {}, source = {}, target = {})".format(repr(self.type), repr(self.source), repr(self.target))
