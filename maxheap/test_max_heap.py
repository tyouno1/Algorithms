import heapq
import math

class MaxHeap(object):
    def __init__(self, initial=None, key=lambda x:x):
        self.key = key
        if initial:
            self._data = [(-1 * key(item), item) for item in initial]
            heapq.heapify(self._data)
        else:
            self._data = []

    def push(self, item):
        heapq.heappush(self._data, (-1 * self.key(item), item))

    def pop(self):
        return heapq.heappop(self._data)[1]

    def replace(self, item):
        heapq.heapreplace(self._data, (-1 * self.key(item), item))

    def getMax(self):
        if self._data:
            return self._data[0][1]
        else:
            return []
        

#import math
#points = [(-2,-4),(0,2),(-1,0),(3,-5),(-2,-3),(3,2)]
#points_with_d = [{"coordinate":p,"distincce": math.sqrt(p[0]*p[0]+p[1]*p[1])} for p in points] 
#k=3
#h = MaxHeap(points_with_d[:k], key=lambda x:x['distincce'])
#print h.getMax()
#for _ in xrange(k):
#    print h.pop()



def closet(points, k):
    # using points, create points_with_d
    points_with_d = [{"coordinate":p,"distince": math.sqrt(p[0]*p[0]+p[1]*p[1])} for p in points]     
    # using points_with_d, create a max_heap with the first k items
    MH = MaxHeap(points_with_d[:k],key=lambda x:x['distince'])
    # call this max heap MH
    for p in points_with_d[k:]:
        if p['distince'] < MH.getMax()['distince']:
            # replace MH's current max point with p
            MH.replace(p)
    # print all points in MH
    for _ in xrange(k):
        print MH.pop()

if __name__ == '__main__':
    points = [(-2,-4),(0,2),(-1,0),(3,-5),(-2,-3),(3,2)]
    closet(points,3)
