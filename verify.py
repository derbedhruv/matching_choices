"""
	Verify that all the grader assignments are
	consistent with the students' preferences

	Read in the assigned graders one by one and verify that they
	are NOT in the excluded list.
"""
import pandas, os
from matching_algo import *

# start here
if __name__ == "__main__":
	preferences = data
	assignments = pandas.read_excel(OUTPUT_FILENAME2)

	STUDENTS_WHO_GOT_THEIR_TOP5CHOICES = 0
	STUDENTS_WHO_GOT_RANDOM_GRADERS = 0
	STUDENTS_WHO_GOT_BAD_GRADERS = 0
	STUDENTS_COUNT = 0

	for index, student in assignments.iterrows():
		STUDENTS_COUNT += 1

		assigned_grader = student["Assigned grader"]
		student_email = student["Email"].split("@stanford.edu")[0]
		student_choice_row = preferences.loc[preferences["What is your SUNetID?"] == student_email]

		if len(student_choice_row) == 0:
			# this student didn't fill the preference form
			continue

		grader_top5 = [student_choice_row[g].tolist()[0] for g in GRADER_CHOICE_LIST]
		excluded_graders = [student_choice_row[g].tolist()[0] for g in EXCLUDED_GRADERS_LIST]

		if (assigned_grader in grader_top5):
			STUDENTS_WHO_GOT_THEIR_TOP5CHOICES += 1
		else:
			STUDENTS_WHO_GOT_RANDOM_GRADERS += 1

		if (assigned_grader in excluded_graders):
			STUDENTS_WHO_GOT_BAD_GRADERS += 1
			print "ERROR:", student["Student Name"], "got a grader who they didn't want!!!"

	# All done. Print stats
	print STUDENTS_COUNT, "students in total"
	print STUDENTS_WHO_GOT_THEIR_TOP5CHOICES, "students got one of their top 5 graders"
	print STUDENTS_WHO_GOT_RANDOM_GRADERS, "students got a random grader"
	print STUDENTS_WHO_GOT_BAD_GRADERS, "got a grader they didn't want"