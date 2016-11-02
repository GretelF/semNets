from semNets.Primitives import Node, Relation, RelationType, RelationAttributeType, NodeAttributeType
from sys import maxsize

class Topology:

  def __init__(self, parent = None):
    self.nodes = []
    self.relations = []
    self.parent = parent

  def __str__(self):
    #TODO
    return "Topology"

  def __repr__(self):
    #TODO
    return "Topology"

  def setParent(self, parent):
    self.parent = parent

  def existsNode(self, n):
    flag = False
    if self.parent != None:
      flag = self.parent.existsNode(n)
    return flag or n in self.nodes

  def existsNodeByName(self, name):
    parentflag = False
    selfflag = False
    if self.parent != None:
      parentflag = self.parent.existsNodeByName(name)
    for node in self.nodes:
      if node.name == name:
        selfflag = True
        break
    return parentflag or selfflag

  def getNodeByName(self, name):
    for node in self.nodes:
      if node.name == name:
        return node
    if self.parent.existsNodeByName(name):
      return self.parent.getNodeByName(name)
    return None

  def insertNode(self, n):
    assert n not in self.nodes, "{} already in {}.".format(repr(n), repr(self))
    self.nodes.append(n)

  def deleteNode(self, n):
    if n in self.nodes:
      self.nodes.remove(n)

  def existsRelation(self, r):
    return r in self.relations

  def existsRelationIncludingParents(self, r):
    flag = False
    if self.parent != None:
      flag = self.parent.existsRelationIncludingParents(r)
    return flag or r in self.relations

  def insertRelation(self, r):
    assert self.existsNode(r.target), "{} not in {}.".format(repr(r.target), repr(self))
    assert self.existsNode(r.source), "{} not in {}.".format(repr(r.source), repr(self))
    self.relations.append(r)

  def deleteRelation(self, r):
    if r in self.relations:
      self.relations.remove(r)

  def tryGetRelation(self, r):
    #todo: what if there are two relations that are equal to r?
    for relation in self.relations:
      if relation == r:
        return relation

  def validate(self):
    '''
    This function validates the topology. It checks, whether the topology contains one connected graph or not.
    :return:
    '''
    pass                                        # TODO ?????

  def getAllRelations(self):
    if self.parent is None:
      return self.relations
    else:
      return self.relations.append(self.parent.getAllRelations())

  def load(self, data):
    '''
    This function loads a topology from a dictionary.
    All previous nodes and relations, if existing, are wiped out.
    '''
    self.nodes.clear()
    self.relations.clear()

    attributetypes = data.get("attributetypes")
    relationtypes = data.get("relationtypes")
    for node in data.get("nodes"):                                                              # load nodes
      self.nodes.append(Node(node))
    if "node_attributes" in data:
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
    relationlist = self.getAllRelations()

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

      nodes.extend(newNodesBuffer)
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

    relationlist = self.getAllRelations()


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
            newNodesBuffer[relTarget] = relSource

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
          curNode = nodes[curNode]
        path.append(source)
        path = path[::-1]
        return path, i

    #if after all iterations target is not found: return None
    return [], -1

  def toJSON(self):
    '''
      a function to bring topologies and views into the comact json format.
    '''
    dict = {}
    dict["nodes"] = []
    dict["relationtypes"] = []
    dict["attributetypes"] = []
    dict["relations"] = []
    dict["relation_attributes"] = []

    for node in self.nodes:
      dict["nodes"].append(str(node))

    for relation in self.relations:
      if str(relation.type) not in dict["relationtypes"]:
        dict["relationtypes"].append(str(relation.type))

      rel = [dict["relationtypes"].index(str(relation.type)), dict["nodes"].index(str(relation.source)),
             dict["nodes"].index(str(relation.target))]
      dict["relations"].append(rel)

      for attribute in relation.attributes:
        if str(attribute.type) not in dict["relation_attributes"]:
          dict["attributetypes"].append(str(attribute.type))

        attr = [dict["attributetypes"].index(str(attribute.type)), dict["relations"].index(rel), str(attribute.value)]
        dict["relation_attributes"].append(attr)

    return dict


  def toJsonNamedTriples(self):
    '''
      a function to bring topologies and views into the comact json format with named triples.
    '''
    dict = {}
    dict["nodes"] = []
    dict["relationtypes"] = []
    dict["attributetypes"] = []
    dict["relations"] = []
    dict["relation_attributes"] = []

    for node in self.nodes:
      dict["nodes"].append(str(node))

    for relation in self.relations:
      if str(relation.type) not in dict["relationtypes"]:
        dict["relationtypes"].append(str(relation.type))

      rel = [str(relation.type), str(relation.source), str(relation.target)]
      dict["relations"].append(rel)

      for attribute in relation.attributes:
        if str(attribute.type) not in dict["attributetypes"]:
          dict["attributetypes"].append(str(attribute.type))

        attr = [str(attribute.type), dict["relations"].index(rel), str(attribute.value)]
        dict["relation_attributes"].append(attr)

    return dict
