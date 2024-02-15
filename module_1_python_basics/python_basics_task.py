# import necessary modules
# random is used to create random numbers and mean is for calculating average
import random
from statistics import mean

# create a list of 100 random numbers from 0 to 1000 with help of random.sample() method
numbers_list = random.sample(range(0, 1000), 100)

# print to see the list created in last step
print(numbers_list)

# loop over the indexes of the numbers_list
for index in range(0, len(numbers_list)):
    # for each index, loop over the remaining indexes of the numbers_list
    for m in range(index + 1, len(numbers_list)):
        # compare the number at current index with the number at next index
        if numbers_list[index] >= numbers_list[m]:
            # if current number is greater than or equal, swap their positions
            numbers_list[index], numbers_list[m] = numbers_list[m], numbers_list[index]

# when for loop is finished print the sorted list
print("Sorted list: ", numbers_list)

# initialize empty lists for even and odd numbers to write there results of sorting
list_even_numbers = []
list_odd_numbers = []

# for loop to sort the list of numbers for even and odd
# iterate through list of numbers
for i in numbers_list:
    # evaluate if the remainder of dividing a given number is 0
    if i % 2 == 0:
        # if yes this is an even number, append the empty list for even numbers with this number
        list_even_numbers.append(i)
        # if remainder is not 0
    else:
        # it means that this is an odd number, append the empty list for odd numbers with it
        list_odd_numbers.append(i)

# calculate the average for both lists with help of mean() function from the python statistics library
avg_even = mean(list_even_numbers)
avg_odd = mean(list_odd_numbers)

# print both averages
print("Average for even numbers: ", avg_even)
print("Average for odd numbers: ", avg_odd)