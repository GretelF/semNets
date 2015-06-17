from semNets.Primitives import Node, Relation, RelationType, RelationAttributeType, NodeAttributeType
from sys import maxsize

class Topology:

  def __init__(self, parent = None):
    self.nodes = []
    self.relations = []
    self.parent = parent

  def __str__(self):
    return "Topology"

  def __repr__(self):
    return "Topology"

  def setParent(self, parent):
    self.parent = parent

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
    # TODO: what about the parents relations?

  def insertRelation(self, r):
    assert r.target in self.nodes, "{} not in {}.".format(repr(r.target), repr(self))
    assert r.source in self.nodes, "{} not in {}.".format(repr(r.source), repr(self))
    self.relations.append(r)

  def tryGetOrInsertRelation(self, r):
    pass  # TODO???

  def deleteRelation(self, r):
    if r in self.relations:
      self.relations.remove(r)

  def validate(self):
    pass                                        # TODO ?????

  def load(self, data):
    self.nodes.clear()
    self.relations.clear()

    attributetypes = data.get("attributetypes")
    relationtypes = data.get("relationtypes")
    for node in data.get("nodes"):                                                              # load nodes
      self.nodes.append(Node(node))
    for node_attribute in data.get("node_attributes"):                                          # load node attributes
      at = NodeAttributeType(attributetypes[node_attribute[0]])
      index = node_attribute[1]
      value = node_attribute[2]
      self.nodes[index].createAttribute(at, value)
    for relation in data.get("relations"):                                                      # load relations
      rt = RelationType(relationtypes[relation[0]])
      source = self.nodes[relation[1]]
      target = self.nodes[relation[2]]
      self.relations.append(Relation(rt, source, target))
    for relation_attribute in data.get("relation_attributes"):                                  # load relation attributes
      at = RelationAttributeType(attributetypes[relation_attribute[0]])
      index = relation_attribute[1]
      value = relation_attribute[2]
      self.relations[index].createAttribute(at, value)

  def existsPath(self, source, target, allowedRelations = None, iterations = maxsize):
    '''
    check if a path from source to target exists.

    :param source: start of path
    :param target: end of path
    :param allowedRelations: RelationTypes that are allowed to be followed, default = all RelationTypes allowed
    :param iterations: number of steps in the search algorithm, default = maximum int
    :return: True if path is found, False if not.
    '''
    relationlist = self.relations.extend(self.parent.relations) if self.parent != None else self.relations
    #todo: recursive?! => recursive getAllRelations() function

    nodes = [source]
    newNodes = nodes.copy()
    newNodesBuffer = []

    for i in range(iterations):
      for node in newNodes:
        # get all relations where the current node is source and its type is in allowedRelations.
        # If allowedRelations is None the second condition is neglected
        relations = [r for r in relationlist if r.source == node and (allowedRelations is None or r.type in allowedRelations)]

        for rel in relations:
          if rel.target not in nodes:
            newNodesBuffer.append(rel.target)

      # no new nodes found.
      if len(newNodesBuffer) == 0:
        break

      nodes.append(newNodesBuffer)
      newNodes = newNodesBuffer.copy()
      newNodesBuffer.clear()

      if target in nodes:
        return True

    return False

  # pathfinding with breadth-first-search
  def findPath(self, source, target, allowedRelations = None, iterations = maxsize):
    '''
    Checks if a path from source to target exists, if yes: return it.

    :param source: start of the path
    :param target: end of the path
    :param allowedRelations: RelationTypes that are allowed to follow, default = all RelationTypes allowed
    :param iterations: number of steps in the search algorithm. default = maximum int

    :return: list of nodes in the found path and number of iterations needed. If no path is found: None and -1
    '''

    relationlist = self.relations.extend(self.parent.relations) if self.parent != None else self.relations


    path = []
    nodes = {source : None}
    newNodes = nodes.copy()
    newNodesBuffer = {}

    for i in range(iterations):
      for relSource in newNodes:
        # get all relations where the current node is source and its type is in allowedRelations.
        # If allowedRelations is None the second condition is neglected
        relations = [r for r in relationlist if r.source == relSource and (allowedRelations is None or r.type in allowedRelations)]

        for relation in relations:
          relTarget = relation.target
          # if the node is not already in the list of visited nodes:
          if relTarget not in nodes.keys():
            # the relations target is added with |source| as parent
            newNodesBuffer[relTarget] = [relSource]

      # no new nodes found
      if len(newNodesBuffer) == 0:
        break

      # add all nodes from newNodes to nodes.
      nodes.update(newNodesBuffer)
      newNodes = newNodesBuffer.copy()
      newNodesBuffer.clear()

      if target in nodes.keys():
        curNode = target
        while curNode != source:
          path.append(curNode)
          curNode = nodes[curNode][1]
        return path.reverse(), i

    #if after all iterations target is not found: return None
    return [], -1

