class Topology:

  def __init__(self, nodeList = None, relationList = None):
    self.nodeList = nodeList or []
    self.relationList = relationList or[]

  def __str__(self):
    pass

  def __repr__(self):
    pass


  def existsNode(self, n):
    return n in self.nodeList

  def insertNode(self, n):
    if not n in self.nodeList:
      self.nodeList.append(n)

  def deleteNode(self, n):
    if n in self.nodeList:
      self.nodeList.remove(n)

  def existsRelation(self, r):
    return r in self.relationList

  def insertRelation(self, r):
    if not r in self.relationList:
      self.relationList.append(r)
    if not r.source in self.nodeList:
      self.nodeList.append(r.source)
    if not r.target in self.nodeList:
      self.nodeList.append(r.target)

  def deleteRelation(self, r):
    if r in self.relationList:
      self.relationList.remove(r)
