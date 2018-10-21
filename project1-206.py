import os
import filecmp
from dateutil.relativedelta import *
from datetime import date


def getData(file):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows
	in_file = open(file, "r")
	data_list = []
	# reads in first line and gets keys for dictionary
	first_line = in_file.readline()
	first_line = first_line.split(",")
	first_name = first_line[0]
	last_name = first_line[1]
	email = first_line[2]
	school_year = first_line[3]
	dob = first_line[4].strip('\n')
	# reads in rest of the lines and closes in file
	data = in_file.readlines()
	in_file.close()
	# loops through and adds dictionary to list
	for line in data:
		temp_dict = {}
		# splits data on comma and adds key value pairs
		new_data = line.split(",")
		temp_dict[first_name] = new_data[0]
		temp_dict[last_name] = new_data[1]
		temp_dict[email] = new_data[2]
		temp_dict[school_year] = new_data[3]
		temp_dict[dob] = new_data[4].strip('\n')
		data_list.append(temp_dict)
	return data_list

def mySort(data,col):
# Sort based on key/column
#Input: list of dictionaries and col (key) to sort on
	# sorts list of dictionaries based on key using lambda
	sorted_data = sorted(data, key=lambda k: k[col])
#Output: Return the first item in the sorted list as a string of just: firstName lastName
	# accesses first element and returns first and last name from dictionary
	name = sorted_data[0]['First'] + " " + sorted_data[0]['Last']
	return name


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
	students_in_class = []
	num_seniors = 0
	num_juniors = 0
	num_sophomores = 0
	num_freshman = 0
	for student in data:
		if student['Class'] == 'Senior':
			num_seniors = num_seniors + 1
		elif student['Class'] == 'Junior':
			num_juniors = num_juniors + 1
		elif student['Class'] == 'Sophomore':
			num_sophomores = num_sophomores + 1
		elif student['Class'] == 'Freshman':
			num_freshman = num_freshman + 1
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
	students_in_class.append(('Senior', num_seniors))
	students_in_class.append(('Junior', num_juniors))
	students_in_class.append(('Sophomore', num_sophomores))
	students_in_class.append(('Freshman', num_freshman))
	students_in_class.sort(key= lambda x: x[1], reverse=True)
	return students_in_class


def findMonth(a):
# Find the most common birth month from this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data
	month_dict = {}
	for student in a:
		temp = student['DOB'].split('/')
		birth_month = temp[0]
		if birth_month in month_dict:
			month_dict[birth_month] = month_dict[birth_month] + 1
		else:
			month_dict[birth_month] = 1
	months = sorted(month_dict.items(),key= lambda x:x[1], reverse=True)
	most_birthdays = (int)(months[0][0])
	return most_birthdays

	

def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as first,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written
	outfile = open(fileName, "w")
	sorted_data = sorted(a, key=lambda k: k[col])
	for student in sorted_data:
		output = student['First'] + "," + student['Last'] + "," + student["Email"]
		outfile.write(output + '\n')

	pass

def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.
	num_students = len(a)
	age_sum = 0
	today = date.today()
	today = today.strftime('%m-%d-%Y')
	today_list = today.split('-')
	current_year = int(today_list[2])
	current_month = int(today_list[0])
	current_day = int(today_list[1])
	for student in a:
		dob = student['DOB']
		dob = dob.split('/')
		month = (int)(dob[0])
		day = (int)(dob[1])
		year = (int)(dob[2])
		age = current_year - year
		if month >= current_month and day > current_day:
			age = current_year - year - 1
		age_sum = age_sum + age
	average_age = round(age_sum/ num_students)
	return average_age


################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB2.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
#data = getData('P1DataA.csv')
