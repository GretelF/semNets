
def euclideanDistance(u, v):
  sumSq=0.0

  #add up the squared differences
  for i in range(len(u)):
    sumSq+=(u[i]-v[i])**2

  #take the square root of the result
  return (sumSq**0.5)

def calculateAttributeDistance(r1, r2, wMissingAttribute = 0.25, wDifferentStringValue = 0.25):
  dist = 0

  # attribute similarity
  selftypes = []
  selfvalues = []
  othertypes = []
  othervalues = []

  for attr in r1.attributes:
    if r2.hasAttributeOfType(attr.type):
      selftypes.append(attr.type)
      othertypes.append(attr.type)
      selfvalues.append(attr.value)
      othervalues.append(r2.getAttributeValue(attr.type))
    else:
      dist += wMissingAttribute

  for attr in r2.attributes:
    if not r1.hasAttributeOfType(attr.type):
      dist += wMissingAttribute

  # deal with the str values (-> add error weight to dist if different)
  for i in range(len(selfvalues)):
    if type(selfvalues[i]) is str or type(othervalues[i]) is str:
      if selfvalues[i] != othervalues[i]:
        dist += wDifferentStringValue
      selfvalues[i] = 0
      othervalues[i] = 0
  dist += euclideanDistance(selfvalues, othervalues)
  return dist

def calculateRelationDistance(r1, r2, wAttr = 0.25, wSource = 0.25, wTarget = 0.25, wType = 0.25, wMissingAttribute = 0.25, wDifferentStringValue = 0.25):
  dif = 0

  if r1.type != r2.type:
    dif += wType
  if r1.source != r2.source:
    dif += wSource
  if r1.target != r2.target:
    dif += wTarget
  dif += calculateAttributeDistance(r1, r2, wMissingAttribute, wDifferentStringValue) * wAttr
  return dif

def matchRelations(rel, node, graph, wAttr = 0.25, wSource = 0.25, wTarget = 0.25, wType = 0.25, wMissingAttribute = 0.25, wDifferentStringValue = 0.25):
  assert node in graph.nodes

  relations = []
  for r in graph.relations:
    if r.source == node:
      relations.append((r, calculateRelationDistance(rel, r,  wAttr = 0.25, wSource = 0.25, wTarget = 0.25, wType = 0.25, wMissingAttribute = 0.25, wDifferentStringValue = 0.25)))

  relations = sorted(relations, key = lambda x: x[1])

  for i in range(len(relations)):
    relations[i] = relations[i][0]

  return relations


