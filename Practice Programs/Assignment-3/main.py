# 3.With a given list [12,24,35,24,88,120,155,88,120,155], write a program to print this list after removing all duplicate values with original order reserved.
# Hint: Use set() to store a number of values without duplicates.


# ---------  Method - 1  ---------

def remove_duplicates(original_list):
    seen = set()
    result = []
    for item in original_list:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Given list
input_list = [12, 24, 35, 24, 88, 120, 155, 88, 120, 155]

# Remove duplicates
unique_list = remove_duplicates(input_list)

# Print the result
print(unique_list) # [12, 24, 35, 88, 120, 155]



# ------ Method - 2 -------

def remove_duplicates(original_list):
    # print(dict.fromkeys(original_list)) # {12: None, 24: None, 35: None, 88: None, 120: None, 155: None}
    return list(dict.fromkeys(original_list)) # [12, 24, 35, 88, 120, 155]

# Given list
input_list = [12, 24, 35, 24, 88, 120, 155, 88, 120, 155]

# Remove duplicates
unique_list = remove_duplicates(input_list)

# Print the result
print(unique_list) # [12, 24, 35, 88, 120, 155]
