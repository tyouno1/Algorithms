import heapq
import math
def closet(points, k):
	# using points, create points_with_d
	points_with_d = [{"coordinate":p,"distincce": -1 * math.sqrt(p[0]*p[0]+p[1]*p[1])} for p in points]    	
	# using points_with_d, create a max_heap with the first k items
    MH = points_with_d[:k]
	heapq.heapify(MH)
	# call this max heap MH
	for p in points_with_d[k..n-1]:
		if p.distince < MH.getMax():
			# replace MH's current max point with p
	# print all points in MH

if __name__ == '__main__':
	points = [(-2,-4),(0,2),(-1,0),(3,-5),(-2,-3),(3,2)]
	closet(points,3)
