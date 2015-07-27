import sys
import getopt
import semNets


usecases = \
  {
    "createTopology" : semNets.Topology.Topology.__init__,
    "relationFilter" : semNets.RelationFilter.translate,
    "nodeFilter" : semNets.NodeFilter.translate,
    "compareGraphs" : semNets.GraphDistance.calculateGraphDistance,
    "setParentOfTopology" : semNets.Topology.Topology.setParent,
    "existsNodeInTopology" : semNets.Topology.Topology.existsNode,
    "existsRelationInTopology" : semNets.Topology.Topology.existsRelation,
    "deleteNodeInTopology" : semNets.Topology.Topology.deleteNode,
    "deleteRelationInTopology" : semNets.Topology.Topology.deleteRelation,
    "insertNodeInTopology" : semNets.Topology.Topology.insertNode,
    "insertRelationInTopology" : semNets.Topology.Topology.insertRelation,
    "loadTopology" : semNets.Topology.Topology.load,
    "findPath" : semNets.Topology.Topology.findPath,
    "existsPath" : semNets.Topology.Topology.existsPath,
    "includeNodeInView" : semNets.View.View.includeNode,
    "includeRelationInView" : semNets.View.View.includeRelation,
    "excludeNodeInView" : semNets.View.View.excludeNode,
    "excludeRelationInView" : semNets.View.View.excludeRelation,
    "mendView" : semNets.View.View.mend,
    "union" : semNets.View.View.union,
    "symDifference" : semNets.View.View.symDifference,
    "intersection" : semNets.View.View.intersection,
    "expandView" : semNets.View.View.expand,
    "RelationCreateAttribute" : semNets.Primitives.Relation.createAttribute,
    "RelationHasAttribute" : semNets.Primitives.Relation.hasAttribute,
    "RelationGetAttributeValue" : semNets.Primitives.Relation.getAttributeValue,
    "RelationHasAttributeOfValue" : semNets.Primitives.Relation.hasAttributeOfType
  }

def main():
  pass


if __name__ == "__main__":
  main()


def getJsonString():
  pass

def processJsonString():
  pass
