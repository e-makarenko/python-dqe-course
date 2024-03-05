import random


def create_random_dict(min_key_val=1, max_key_val=26, min_value=ord('a'), max_value=ord('z')):
    dict_keys = random.randint(min_key_val, max_key_val)
    return {chr(random.randint(min_value, max_value)): random.randint(0, 100) for _ in range(dict_keys)}


# function to find keys that appear more than once in all dicts
def find_duplicate_keys_and_their_max_values(list_of_dicts):
    new_dict = {}
    keys_with_max_values_list = []

    for dict_index, dictionary in enumerate(list_of_dicts, start=1):
        for key, value in dictionary.items():
            if key in new_dict:
                if value > new_dict[key][0]:
                    new_dict[key] = (value, dict_index)
                keys_with_max_values_list.append(key)
            else:
                new_dict[key] = (value, dict_index)
    return keys_with_max_values_list, new_dict


def create_final_dict(keys_with_max_values, new_dict):
    final_dict = {}

    for key in list(new_dict.keys()):
        value, index = new_dict.pop(key)
        if key in keys_with_max_values:
            key = f"{key}_{index}"
        final_dict.update({key: value})

    # sorting the final dictionary based on its keys
    final_dict_sorted = {key: final_dict[key] for key in sorted(final_dict)}

    return final_dict_sorted


if __name__ == "__main__":
    dicts_number = random.randint(2, 10)
    print("Randomly generated number of dictionaries that will be stored in the list: ", dicts_number)

    list_of_dictionaries = [create_random_dict() for _ in range(dicts_number)]
    print("\nList with dictionaries:", list_of_dictionaries)

    keys_with_max_values_list, new_dict = find_duplicate_keys_and_their_max_values(list_of_dictionaries)
    print("\nList of keys which repeat in dictionaries: ", keys_with_max_values_list)
    print("\nNew dictionary: ", new_dict)

    final_dictionary = create_final_dict(keys_with_max_values_list, new_dict)
    print("\nFinal new dictionary (sorted): ", final_dictionary)
