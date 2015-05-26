class View:
  def __init__(self, topology):
    self.topology = topology
    self.nodes = []
    self.relations = []

  def __str__(self):
    pass

  def __repr__(self):
    pass

  # easy expand
  def expand(self, relationFilter):
    nodesToBeIncluded = []

    for node in self.nodes:
      relations = [r for r in self.topology.relations if r.source == node]
      for relation in relations:
        if relationFilter(relation) and relation.target not in self.nodes:
          self.includeRelation(relation)
          nodesToBeIncluded.append(relation.target)                              # nodes will be included all together at the end to prevent the loop from growing.

    for node in nodesToBeIncluded:
      self.includeNode(node)


  def includeNode(self, n):
    assert self.topology.existsNode(n)
    if n not in self.nodes:
      self.nodes.append(n)

  def includeRelation(self, r):
    assert self.topology.existsRelation(r)
    self.relations.append(r)

  def excludeNode(self, n):
    self.nodes.remove(n)

  def excludeRelation(self, r):
    self.relations.remove(r)

  #Get all source and target nodes for "open" relations
  def mend(self):
    for r in self.relations:
      self.includeNode(r.target)
      self.includeNode(r.source)


  def union(self, other):                 # or
    view = View(self.topology)
    for n in self.nodes:
      view.includeNode(n)
    for n in other.nodes:
      view.includeNode(n)
    for r in self.relations:
      view.includeRelation(r)
    for r in other.relations:
      view.includeRelation(r)
    return view

  def symDifference(self, other):         # exclusive or
    view = View(self.topology)
    for n in self.nodes:
      if n not in other.nodes:
        view.includeNode(n)
    for n in other.nodes:
      if n not in self.nodes:
        view.includeNode(n)
    for r in self.relations:
      if r not in other.relations:
        view.includeRelation(r)
    for r in other.relations:
      if r not in self.relations:
        view.includeRelation(r)
    return view

  def intersection(self, other):          # and
    view = View(self.topology)
    for n in self.nodes:
      if n in other.nodes:
        view.includeNode(n)
    for r in self.relations:
      if r in other.rleations:
        view.includeRelation(r)
    return view



