# task 1
import random

# create random number of dictionaries and save it as a variable to use it in the for loop
number_of_dicts = random.randint(2, 10)
print("Randomly generated number of dictionaries that will be stored in the list: ", number_of_dicts)

# initialize empty list for dictionaries that we are going to append in the for loop
list_of_dicts = []

# use for loop to create the number of dictionaries defined above as number_of_dicts variable
for i in range(number_of_dicts):
    dict_keys = random.randint(1,26)
    print("Random number of keys in a dictionary in the current run of for loop:", dict_keys)
    temp_dict = {}
    # for loop to generate key:value pairs in the dict with random letters and numbers
    for n in range(dict_keys):
        key = chr(random.randint(ord('a'), ord('z')))
        value = random.randint(0, 100)
        temp_dict.update({key: value})
    list_of_dicts.append(temp_dict)

print("Final list with dictionaries: ", list_of_dicts)

# task 2
new_dict = {}

# initialize empty list for keys which repeat in more than one dictionary in the list with dictionaries
keys_with_max_values_list = []

dict_index = 1

# loop through dictionaries in list and through each key, value pair in the dict to check if key repeats across dicts
# create a list with keys that are repeated in dicts and new dictionary with key and value as tuple that consists of number and index where this number was found
for dictionary in list_of_dicts:
    for key, value in dictionary.items():
        if key in new_dict:
            if value > new_dict[key][0]:
                new_dict[key] = (value, dict_index)
            keys_with_max_values_list.append(key)
        else:
            new_dict[key] = (value, dict_index)
    dict_index += 1

print("List of keys which repeat in dictionaries: ", keys_with_max_values_list)
print("Current new dictionary: ", new_dict)

final_dict = {}

# create a list of keys of the new_dictionary to compare it with keys_with_max_values_list in for loop
keys = list(new_dict.keys())
print("List with keys from new_dict dictionary: ", keys)

# loop through list of keys and update the keys found in keys_with_max_values_list
for key in keys:
    # unpack the tuple in new_dict into 2 separate variables (value, index) and remove the item variable and return the value
    value, index = new_dict.pop(key)
    if key in keys_with_max_values_list:
        key = f"{key}_{index}"
    final_dict.update({key: value})

print("Final new dictionary (unsorted): ", final_dict)

# sort final_dict by keys using dictionary comprehension to create new final_dict_sorted
final_dict_sorted = {k: final_dict[k] for k in sorted(final_dict)}
print("Final new dictionary (sorted): ", final_dict_sorted)
