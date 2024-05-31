# Implementation of range queries on data

# Function to perform range queries on floating-point numbers
def el_query(lst, start, end):
    return (lst[end]-lst[start]) * 3561633.986


def index_diff_query(lst, index):
    # Check if the index is within the bounds of the list
    if 0 < index < len(lst):
        # Return the difference between the element at the specified index and the previous element
        return (lst[index] - lst[index - 1])*3561633.986
    elif index == 0:
        # Handle the case where the index is 0
        # Depending on your use case, you might want to return None or a specific message
        return "N/A (No previous index)"
    else:
        # Handle the case where the index is out of bounds
        return "Index out of bounds"
    

def index_query(lst, index):
    if 0 <= index < len(lst):
        return lst[index]*3561633.986
    

def sum_of_differences_in_range(lst, start, end):
    # Calculate differences between consecutive elements
    differences = [lst[i] - lst[i - 1] for i in range(1, len(lst))]
    
    # Filter differences that fall within the specified range and sum them
    sum_diffs = sum(diff for diff in differences if start <= diff <= end)
    
    return sum_diffs*3561633.986



# Reading the list from the file, assuming it contains floating-point numbers
with open('Data/B_t_filtered.txt', 'r') as file:
    list_from_file = [float(line.strip()) for line in file]




# Example range query: elements between 0.1 and 0.2 (inclusive)
result1 = el_query(list_from_file, 11, 20)
result2 = index_diff_query(list_from_file, 11)
result3 = index_query(list_from_file, 11)
result4 = index_query(list_from_file, 10)
result5 = sum_of_differences_in_range(list_from_file, 0.1, 0.2)


print("Query result1:", result1)
print("Query result2:", result2)
print("Query result3:", result3)
print("Query result4:", result4)
print("Query result5:", result5)

