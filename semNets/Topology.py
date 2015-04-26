class Topology:

  def __init__(self):
    self.nodes = []
    self.relations = []

  def __str__(self):
    return "Topology"

  def __repr__(self):
    return "Topology"

  def load(self, data):
    for node in data.get("nodes"):
      pass                                            # TODO

  def existsNode(self, n):
    return n in self.nodes

  def insertNode(self, n):
    assert n not in self.nodes, "{} already in {}.".format(repr(n), repr(self))
    self.nodes.append(n)

  def deleteNode(self, n):
    if n in self.nodes:
      self.nodes.remove(n)

  def existsRelation(self, r):
    return r in self.relations

  def insertRelation(self, r):
    assert r.target in self.nodes, "{} not in {}.".format(repr(r.target), repr(self))
    assert r.source in self.nodes, "{} not in {}.".format(repr(r.source), repr(self))
    self.relations.append(r)

  def deleteRelation(self, r):
    if r in self.relations:
      self.relations.remove(r)

  def validate(self):
    pass                                        # TODO ?????
