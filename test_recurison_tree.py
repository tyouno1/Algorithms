def all_subsets(given_array):
	subset = len(given_array) * [None]
	helper(given_array, subset, 0)

def print_set(subset):
	print [x for x in subset if x is not None]

def helper(given_array, subset, i):
	if i == len(given_array):
		print subset
		print_set(subset)
	else:
		subset[i] = None
		helper(given_array, subset, i+1)
		subset[i] = given_array[i]
		helper(given_array, subset, i+1)

if __name__ == '__main__':
	all_subsets([1,2])
