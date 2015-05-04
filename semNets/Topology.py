from semNets.Primitives import Node, Relation, RelationType, RelationAttributeType, NodeAttributeType

class Topology:

  def __init__(self):
    self.nodes = []
    self.relations = []

  def __str__(self):
    return "Topology"

  def __repr__(self):
    return "Topology"

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

  def load(self, data):
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
