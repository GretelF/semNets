from sys import maxsize


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
      relations.append((r, calculateRelationDistance(rel, r,  wAttr, wSource, wTarget, wType, wMissingAttribute, wDifferentStringValue)))

  relations = sorted(relations, key = lambda x: x[1])

  return relations


def calculateGraphDistance(graph1, graph2, node1, node2, iterationCount=10):
  assert iterationCount > 0, "Iteration count has to be greater than 0."

  relations1 = [r for r in graph1.relations if r.source == node1]
  relations2 = [r for r in graph2.relations if r.source == node2]

  rel1 = relations1[0]
  relations2 = matchRelations(rel1, node2, graph2, wAttr = 0.25, wSource = 0.25, wTarget = 0.25, wType = 0.25, wMissingAttribute = 0.25, wDifferentStringValue = 0.25)
  rel2 = relations2[0][0]

  currentBestErrorCount = relations2[0][1]
  for i in range(iterationCount):
    n1 = rel1.target
    n2 = rel2.target
    relations1 = [r for r in graph1.relations if r.source == n1]
    relations2 = [r for r in graph2.relations if r.source == n2]

    currentBestErrorCount += (abs(len(relations1)-len(relations2))) * 0.25

    if len(relations1) == 0 or len(relations2) == 0:
      return calculateGraphDistance_helper(graph1, graph2, node1, node2, currentBestErrorCount, 0, iterationCount)


    rel1 = relations1[0]
    relations2 = matchRelations(rel1, node2, graph2, wAttr = 0.25, wSource = 0.25, wTarget = 0.25, wType = 0.25, wMissingAttribute = 0.25, wDifferentStringValue = 0.25)
    rel2 = relations2[0][0]
    currentBestErrorCount += relations2[0][1]

  return calculateGraphDistance_helper(graph1, graph2, node1, node2, currentBestErrorCount, 0, iterationCount)


def calculateGraphDistance_helper(graph1, graph2, node1, node2, currentBestErrorCount, currentErrorCount, iterationCount = 10):
  if iterationCount == 0:
    return currentErrorCount

  iterationCount -= 1

  relations1 = [r for r in graph1.relations if r.source == node1]
  relations2 = [r for r in graph2.relations if r.source == node2]

  differenceInNumberOfRelations = abs(len(relations1) - len(relations2))

  # accumulates best error counts for each relation in relations1
  overallErrorCountForThisSubgraph = 0

  if len(relations1) == 0:
    return currentErrorCount + differenceInNumberOfRelations * 0.25


  for r1 in relations1:
    bestRelationFittingR1 = None
    bestErrorCountForR1 = maxsize

    #match relations in relations2 to r1
    relations2 = matchRelations(r1, node2, graph2, wAttr = 0.25, wSource = 0.25, wTarget = 0.25, wType = 0.25, wMissingAttribute = 0.25, wDifferentStringValue = 0.25)

    # if there are no relations to compare break
    if len(relations2) == 0:
      break

    for r2 in relations2:
      # r2[1] is the distance from r1 to r2
      localCurrentErrorCountForThisLoop = currentErrorCount + r2[1]
      errorCount = calculateGraphDistance_helper(graph1, graph2, r1.target, r2[0].target, currentBestErrorCount - localCurrentErrorCountForThisLoop, localCurrentErrorCountForThisLoop, iterationCount)
      #if the errorCount for R2 is smaller than the best one -> set errorCount as new best one
      if errorCount < bestErrorCountForR1:
        # subtract current error count to avoid adding it multiple times
        bestErrorCountForR1 = errorCount - currentErrorCount
        bestRelationFittingR1 = r2[0]

    #add the best found error count for r1 to overallErrorCountForThisSubgraph
    overallErrorCountForThisSubgraph += bestErrorCountForR1

  #add error for different numbers of relations and eventually the currentErrorCount for this stage
  return overallErrorCountForThisSubgraph + differenceInNumberOfRelations * 0.25 + currentErrorCount





