import sys
import argparse
import semNets
from semNets.Primitives import Node, Relation, RelationType, RelationAttributeType, Attribute
from semNets.Topology import Topology
from semNets.View import View

import uuid

class Environment:
  instances = {}

  def __init__(self):
    self.vars = {}
    self.uuid = uuid.uuid4()
    Environment.instances[self.uuid] = self

  def define(self, name, object):
    self.vars[name] = object

  def tryGetVar(self, name):
    return self.vars.get(name, None)

  def hasVar(self, name):
    return self.tryGetVar(name) is not None

  def __eq__(self, other):
    return self.uuid == other.uuid

usecases = \
  {
    "createView" : semNets.View.View.__init__,
  }

commands = {}

def cmd(name):
  def wrapper(func):
    commands[name] = func
    return func
  return wrapper

@cmd("compareGraphs")
def compareGraphs(env, graph1, graph2, node1, node2, iterations = None):
  g1 = env.vars[graph1]
  g2 = env.vars[graph2]
  n1 = Node(node1)
  n2 = Node(node2)
  dist = semNets.GraphDistance.calculateGraphDistance(g1, g2, n1, n2, iterations)

  #todo return dist


@cmd("createTopology")
def createTopology(env, name, parent = None):
  p = env.vars[parent] if parent is not None else None
  topology = Topology(p)
  env.define(name, topology)

  #Todo: return True or something

@cmd("createNode")
def createNode(env, name):
  #todo: is this needed? or should it be chained with an addNode function for topologies and views?
  #todo: do we have to add the node to the environment?
  node = Node(name)
  env.define(name, node)

  #todo: return True or something

@cmd("createRelation")
def createRelation(env, type, source, target):
  relationtype = RelationType(type)
  relation = Relation(type, Node(source), Node(target))
  # todo: do relations need to be saved in the environment?
  # todo: + what name should they get?

  #todo: return True or something

@cmd("relationCreateAttribute")
def relationCreateAttribute(env, topology, relationType, source, target, attributeType, value, attributes = None):
  tmpRelation = Relation(RelationType(relationType), Node(source), Node(target))
  for type, value in attributes:
    tmpRelation.createAttribute(RelationAttributeType(type), value)
  t = env.vars[topology]
  assert t is not None
  r = t.tryGetRelation(tmpRelation)
  assert r is not None
  r.createAttribute(RelationAttributeType(attributeType), value)

  #todo: return True or something

@cmd("relationHasAttribute")
def relationHasAttribute(env, topology, type, source, target, attributeType, value):
  tmpRelation = Relation(RelationType(type), Node(source), Node(target))
  attr = Attribute(RelationAttributeType(attributeType), value)
  t = env.vars[topology]
  assert t is not None
  r = t.tryGetRelation(tmpRelation)
  assert r is not None
  result = r.hasAttribute(attr)

  #todo return result

@cmd("relationGetAttributeValue")
def relationGetAttributeValue(env, topology, type, source, target, attributeType):
  tmpRelation = Relation(RelationType(type), Node(source), Node(target))
  t = env.vars[topology]
  assert t is not None
  r = t.tryGetRelation(tmpRelation)
  assert r is not None
  value = r.getAttributeValue(RelationAttributeType(attributeType))
  #todo: return value

@cmd("relationHasAttributeOfType")
def relationHasAttributeOfType(env, topology, type, source, target, attributeType):
  tmpRelation = Relation(RelationType(type), Node(source), Node(target))
  t = env.vars[topology]
  assert t is not None
  r = t.tryGetRelation(tmpRelation)
  assert r is not None
  result = r.hasAttributeOfType(RelationAttributeType(attributeType))

  #todo return result

@cmd("loadTopology")
def loadTopology(env, topology, data):
  t = env.vars[topology]
  t.load(data)
  #todo return True or something

@cmd("setParentOfTopology")
def setParentOfTopology(env, topology, parent):
  t = env.vars[topology]
  p = env.vars[parent]
  assert p is not None
  assert t is not None

  t.setParent(p)

  #todo return True or something

@cmd("existsNodeInTopology")
def existsNodeInTopology(env, topology, node):
  t = env.vars[topology]
  n = Node(node)
  result = t.existsNode(n)

  #todo return result

@cmd("existsRelationInTopology")
def existsRelationInTopology(env, topology, type, source, target):
  t = env.vars[topology]
  relation = Relation(RelationType(type), Node(source), Node(target))
  result = t.existsRelation(relation)

  #todo return result

@cmd("insertNodeInTopology")
def insertNodeInTopology(env, topology, node):
  t = env.vars[topology]
  n = Node(node)
  t.insertNode(n)

  #todo return True or something

@cmd("insertRelationInTopology")
def insertNodeInTopology(env, topology, type, source, target):
  t = env.vars[topology]
  relation = Relation(RelationType(type), Node(source), Node(target))
  t.insertRelation(relation)

  #todo return True or something

@cmd("deleteNodeInTopology")
def deleteNodeInTopology(env, topology, node):
  t = env.vars[topology]
  n = Node(node)
  t.deleteNode(n)

  #todo return True or something to indicate success

@cmd("deleteRelationInTopology")
def deleteRelationInTopology(env, topology, type, source, target):
  t = env.vars[topology]
  relation = Relation(RelationType(type), Node(source), Node(target))
  t.deleteRelation(relation)

  #todo return True or something to indicate success

@cmd("includeNodeInView")
def includeNodeInView(env, view, node):
  v = env.vars[view]
  n = Node(node)
  v.includeNode(n)
  #todo: return True or something

@cmd("includeRelationInView")
def includeRelationInView(env, view, type, source, target):
  v = env.vars[view]
  r = Relation(RelationType(type), Node(source), Node(target))
  v.includeRelation(r)
  #todo: return True or something

@cmd("excludeNodeInView")
def excludeNodeInView(env, view, node):
  v = env.vars[view]
  n = Node(node)
  v.excludeNode(n)
  #todo: return True or something

@cmd("excludeRelationInView")
def excludeRelationInView(env, view, type, source, target):
  v = env.vars[view]
  r = Relation(RelationType(type), Node(source), Node(target))
  v.excludeRelation(r)
  #todo: return True or something

@cmd("mendView")
def mendView(env, view):
  v = env.vars[view]
  v.mend()
  #todo: return True or something

@cmd("union")
def union(env, view1, view2, resultView):
  v1 = env.vars[view1]
  v2 = env.vars[view2]

  v3 = v1.union(v2)
  env.define(resultView, v3)

@cmd("symDifference")
def symDifference(env, view1, view2, resultView):
  v1 = env.vars[view1]
  v2 = env.vars[view2]

  v3 = v1.symDifference(v2)
  env.define(resultView, v3)

@cmd("intersection")
def intersection(env, view1, view2, resultView):
  v1 = env.vars[view1]
  v2 = env.vars[view2]

  v3 = v1.intersection(v2)
  env.define(resultView, v3)

@cmd("nodeFilter")
def nodeFilter(env, subgraph, resultgraph, conditions):
  filter = semNets.NodeFilter.translate(conditions)
  view = env.vars[subgraph]
  resultView = View(view.topology)

  for node in view.nodes:
    if filter(node):
      resultView.includeNode(node)

  for relation in view.relations:
    if relation.source in resultView.nodes and relation.target in resultView.nodes:
      resultView.includeRelation(relation)

  env.define(resultgraph, resultView)

  #todo: return True or something to indicate success

@cmd("expandView")
def expandView(env, subgraph, conditions):
  filter = semNets.RelationFilter.translate(conditions)
  view = env.vars[subgraph]
  view.expand(filter)

  #todo: return True or something

@cmd("findPath")
def findPath(env, topology, source, target, allowedRelationTypes = None, iterations = None):
  t = env.vars[topology]
  path = t.findPath(Node(source), Node(target), allowedRelationTypes, iterations)
  #todo: allowedRelationTypes is list of strings. has to be list of RelationType!!!

  #todo: prepare path list for json encoding and return

@cmd("existsPath")
def existsPath(env, topology, source, target, allowedRelationTypes = None, iterations = None):
  t = env.vars[topology]
  result = t.existsPath(Node(source), Node(target), allowedRelationTypes, iterations)
  #todo: allowedRelationTypes is list of strings. has to be list of RelationType!!!

  #todo: return result



def dispatch(data):
  assert "env" in data
  env = Environment.instances.get(data.pop("env"), None)
  assert env is not None

  for cmdname, args in data:
    thecmd = commands.get(cmdname, None)
    assert thecmd is not None
    thecmd(env, **args)




def main():
  pass


if __name__ == "__main__":
  main()
