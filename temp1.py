from itertools import chain, combinations

def get_subsets(lst):
    return list(chain.from_iterable(combinations(lst, r) for r in range(1,len(lst) + 1)))

def find_combinations(subsets):
    full_set = set().union(*subsets)
    
    def dfs(index, current_combination, remaining_elements):
        if not remaining_elements:
            combinations.append(current_combination)
            return

        for i in range(len(subsets)-1,index-1, -1):
            new_combination = current_combination + [subsets[i]]
            new_remaining = remaining_elements - set(subsets[i])
            dfs(i + 1, new_combination, new_remaining)

    combinations = []
    dfs(0, [], full_set)

    return combinations

# Example usage
my_list = ["a", "b", "c"]
subsets = get_subsets(my_list)

combinations = find_combinations(subsets)

# Print the result
for combination in combinations:
    print(list(combination))

print(len(combinations))