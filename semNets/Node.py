class Node :
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return "N['{}']".format(self.name)

  def __repr__(self):
    return "Node(name = {})".format(repr(self.name))
