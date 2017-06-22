import sys
import inspect
import heapq, random


"""
 Utility classes
 
 Data structures useful for implementing SearchAgents 
"""

class Stack:
  """
   Data structure that implements a last-in-first-out (LIFO)
  queue policy. 
  """
  def __init__(self):
    self.list = []
    
  def push(self,item):
    """
        Push 'item' onto the stack
    """
    self.list.append(item)

  def pop(self):
    """
       Pop the most recently pushed item from
       the stack
    """
    return self.list.pop()

  def isEmpty(self):
    """
        Returns true if the stack is empty
    """
    return len(self.list) == 0

class Queue:
  """
    Data structure that implements a first-in-first-out (FIFO)
  queue policy. 
  """
  def __init__(self):
    self.list = []
  
  def push(self,item):
    """
      Enqueue the 'item' into the queue
    """
    self.list.insert(0,item)

  def pop(self):
    """
      Dequeue the earliest enqueued item still in the queue. This
      operation removes the item from the queue.
    """
    return self.list.pop()

  def isEmpty(self):
    """
        Returns true if the queue is empty.
    """
    return len(self.list) == 0
  
class PriorityQueue:
  """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.
  """
    
  def __init__(self):
    """
      heap: A binomial heap storing [priority,item]
      lists. 
      
      dict: Dictionary storing item -> [priorirty,item]
      maps so we can reach into heap for a given 
      item and update the priorirty and heapify
    """
    self.heap = []
    self.dict = {}
      
  def push(self,item,priority):
    """
        Sets the priority of the 'item' to
    priority. If the 'item' is already
    in the queue, then its key is changed
    to the new priority, regardless if it
    is higher or lower than the current 
    priority.
    """
    if item in self.dict:
      self.dict[item][0] = priority
      heapq.heapify(self.heap)
    else:
      pair = [priority,item]
      heapq.heappush(self.heap,pair)
      self.dict[item] = pair
      
  def getPriority(self,item):
    """
        Get priority of 'item'. If 
    'item' is not in the queue returns None
    """
    if not item in self.dict:
      return None
    return self.dict[item][0]
      
  def pop(self):
    """
      Returns lowest-priority item in priority queue, or
      None if the queue is empty
    """
    if self.isEmpty(): return None
    (priority,item) = heapq.heappop(self.heap)
    del self.dict[item]
    return item  
  
  def isEmpty(self):
    """
        Returns True if the queue is empty
    """
    return len(self.heap) == 0

class FasterPriorityQueue:
  """
    Implements a priority queue data structure.  This differs from the 
    PriorityQueue in that it allows multiple copies of the same object, 
    and doesn't support getPriority or changing priority.
  """
  
  def  __init__(self):  
    self.heap = []
    
  def push(self, item, priority):
      pair = (priority,item)
      heapq.heappush(self.heap,pair)

  def pop(self):
      (priority,item) = heapq.heappop(self.heap)
      return item
  
  def isEmpty(self):
    return len(self.heap) == 0

class Counter(dict):
  """
  A counter keeps track of counts for a set of keys.
  
  The counter class is an extension of the standard python
  dictionary type.  It is specialized to have number values  
  (integers or floats), and includes a handful of additional
  functions to ease the task of counting data.  In particular, 
  all keys are defaulted to have value 0.  Using a dictionary:
  
  a = {}
  print a['test']
  
  would give an error, while the Counter class analogue:
    
  >>> a = Counter()
  >>> print a.getCount('test')
  0
  
  returns the default 0 value. Note that to reference a key 
  that you know is contained in the counter, 
  you can still use the dictionary syntax:
    
  >>> a = Counter()
  >>> a['test'] = 2
  >>> print a['test']
  2
  
  The counter also includes additional functionality useful in implementing
  the classifiers for this assignment.  Two counters can be added,
  subtracted or multiplied together.  See below for details.  They can
  also be normalized and their total count and arg max can be extracted.
  """
  def incrementCount(self, key, count):
    """
    Increases the count of key by the specified count.  If 
    the counter does not contain the key, then the count for
    key will be set to count.
    
    >>> a = Counter()
    >>> a.incrementCount('test', 1)
    >>> a.getCount('hello')
    0
    >>> a.getCount('test')
    1
    """
    if key in self:
      self[key] += count
    else:
      self[key] = count
      
  def incrementAll(self, keys, count):
    """
    Increments all elements of keys by the same count.
    
    >>> a = Counter()
    >>> a.incrementAll(['one','two', 'three'], 1)
    >>> a.getCount('one')
    1
    >>> a.getCount('two')
    1
    """
    for key in keys:
      self.incrementCount(key, count)
            
  def setCount(self, key, count):
    """
    Sets the count of key to the specified count.
    """
    self[key] = count
    
  def getCount(self, key):
    """
    Returns the count of key, defaulting to zero.
    
    >>> a = Counter()
    >>> print a.getCount('test')
    0
    >>> a['test'] = 2
    >>> print a.getCount('test')
    2
    """
    if key in self:
      return self[key]
    else:
      return 0
  
  def argMax(self):
    """
    Returns the key with the highest value.
    """
    if len(self.keys()) == 0: return None
    all = self.items()
    values = [x[1] for x in all]
    maxIndex = values.index(max(values))
    return all[maxIndex][0]
  
  def sortedKeys(self):
    """
    Returns a list of keys sorted by their values.  Keys
    with the highest values will appear first.
    
    >>> a = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> a['third'] = 1
    >>> a.sortedKeys()
    ['second', 'third', 'first']
    """
    sortedItems = self.items()
    compare = lambda x, y:  sign(y[1] - x[1])
    sortedItems.sort(cmp=compare)
    return [x[0] for x in sortedItems]
  
  def totalCount(self):
    """
    Returns the sum of counts for all keys.
    """
    return sum(self.values())
  
  def normalize(self):
    """
    Edits the counter such that the total count of all
    keys sums to 1.  The ratio of counts for all keys
    will remain the same. Note that normalizing an empty 
    Counter will result in an error.
    """
    total = float(self.totalCount())
    for key in self.keys():
      self[key] = self[key] / total
      
  def divideAll(self, divisor):
    """
    Divides all counts by divisor
    """
    divisor = float(divisor)
    for key in self:
      self[key] /= divisor

  def __mul__(self, y ):
    """
    Multiplying two counters gives the dot product of their vectors where
    each unique label is a vector element.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['second'] = 5
    >>> a['third'] = 1.5
    >>> a['fourth'] = 2.5
    >>> a * b
    14
    """
    sum = 0
    x = self
    if len(x) > len(y):
      x,y = y,x
    for key in x:
      if key not in y:
        continue
      sum += x[key] * y[key]      
    return sum
      
  def __radd__(self, y):
    """
    Adding another counter to a counter increments the current counter
    by the values stored in the second counter.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> a += b
    >>> a.getCount('first')
    1
    """ 
    for key, value in y.items():
      self.incrementCount(key, value)   
      
  def __add__( self, y ):
    """
    Adding two counters gives a counter with the union of all keys and
    counts of the second added to counts of the first.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> (a + b).getCount('first')
    1
    """
    addend = Counter()
    for key in self:
      if key in y:
        addend[key] = self[key] + y[key]
      else:
        addend[key] = self[key]
    for key in y:
      if key in self:
        continue
      addend[key] = y[key]
    return addend
    
  def __sub__( self, y ):
    """
    Subtracting a counter from another gives a counter with the union of all keys and
    counts of the second subtracted from counts of the first.
    
    >>> a = Counter()
    >>> b = Counter()
    >>> a['first'] = -2
    >>> a['second'] = 4
    >>> b['first'] = 3
    >>> b['third'] = 1
    >>> (a - b).getCount('first')
    -5
    """      
    addend = Counter()
    for key in self:
      if key in y:
        addend[key] = self[key] - y[key]
      else:
        addend[key] = self[key]
    for key in y:
      if key in self:
        continue
      addend[key] = -1 * y[key]
    return addend
    
def raiseNotDefined():
  print "Method not implemented: %s" % inspect.stack()[1][3]    
  sys.exit(1)

def normalize(vectorOrCounter):
  """
  normalize a vector or counter by dividing each value by the sum of all values
  """
  normalizedCounter = Counter()
  if type(vectorOrCounter) == type(normalizedCounter):
    counter = vectorOrCounter
    total = float(counter.totalCount())
    if total == 0: return counter
    for key in counter.keys():
      value = counter.getCount(key)
      normalizedCounter.setCount(key, value / total)
    return normalizedCounter
  else:
    vector = vectorOrCounter
    s = float(sum(vector))
    return [el / s for el in vector]
                
def nSample(distribution, values, n):
  if sum(distribution) != 1:
    distribution = normalize(distribution)
  rand = [random.random() for i in range(n)]
  rand.sort()
  samples = []
  samplePos, distPos, cdf = 0,0, distribution[0]
  while samplePos < n:
    if rand[samplePos] < cdf:
      samplePos += 1
      samples.append(values[distPos])
    else:
      distPos += 1
      cdf += distribution[distPos]
  return samples
    
def sample(distribution, values):
  if sum(distribution) != 1:
    distribution = normalize(distribution)
  choice = random.random()
  i, total= 0, distribution[0]
  while choice > total:
    i += 1
    total += distribution[i]
  return values[i]

def getProbability(value, distribution, values):
  """
    Gives the probability of a value under a discrete distribution
    defined by (distributions, values).
  """
  total = 0.0
  for prob, val in zip(distribution, values):
    if val == value:
      total += prob
  return total
    
def manhattanDistance( xy1, xy2 ):
  """
  Returns the Manhattan distance between points xy1 and xy2
  """
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def chooseFromDistribution( distribution ):
  r = random.random()
  base = 0.0
  for prob, element in distribution:
    base += prob
    if r <= base: return element
    
def nearestPoint( pos ):
  """
  Finds the nearest grid point to a position (discretizes).
  """
  ( current_row, current_col ) = pos

  grid_row = int( current_row + 0.5 ) 
  grid_col = int( current_col + 0.5 ) 
  return ( grid_row, grid_col )     

def sign( x ):
  """
  Returns 1 or -1 depending on the sign of x
  """
  if( x >= 0 ):
    return 1
  else:
    return -1

def arrayInvert(array):
  """
  Inverts a matrix stored as a list of lists.
  """
  result = [[] for i in array]
  for outer in array:
    for inner in range(len(outer)):
      result[inner].append(outer[inner])
  return result

def matrixAsList( matrix, value = True ):
  """
  Turns a matrix into a list of coordinates matching the specified value
  """
  rows, cols = len( matrix ), len( matrix[0] )
  cells = []
  for row in range( rows ):
    for col in range( cols ):
      if matrix[row][col] == value:
        cells.append( ( row, col ) )
  return cells