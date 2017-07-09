"""
Matching algorithm for grader preferences for the students of E145
Required - an XLSX sheet version of the google sheet of the google form that was filled by them

ALGORITHM:
- read in the CSV sheet
- go row by row and make assignments => this is where assignments are done by first come first served
  - you can ALSO use a lottery to randomly assign people a number
- Assign to the first person. If first person is full, then assign to the second, and so on in their choice list
  * if you go beyond their 5th choice, then randomly assign to the remaining teams which are NOT in their exclusion list

EDGE CASES:
- if someone enters multiple choices, take the one with the latest timestamp
- if someone has not entered all 5 grader choices or all 3 exclusion choices
"""
import pandas

## DEBUGGING, PRINT VERBOSE STATEMENTS
VERBOSE = False

def log(message):
	# print this out only if VERBOSE == True
	if VERBOSE:
		print ' '.join([str(m) for m in message])

CSV_NAME = "2016_grading_preferences.csv"		# change to whatever's appropriate

# column names - these will be keys for the pandas dataframe
FIRST_CHOICE_TEXT = "Who is your first choice pair for PBP graders?"
SECOND_CHOICE_TEXT = "Who is your second choice?"
THIRD_CHOICE_TEXT = "Who is your third choice?"
FOURTH_CHOICE_TEXT = "Who is your fourth choice?"
FIFTH_CHOICE_TEXT = "Who is your fifth choice?"

GRADER_CHOICE_LIST = [FIRST_CHOICE_TEXT, SECOND_CHOICE_TEXT, THIRD_CHOICE_TEXT, FOURTH_CHOICE_TEXT, FIFTH_CHOICE_TEXT]

FIRST_EXCLUSION_TEXT = "First team you want EXCLUDED"
SECOND_EXCLUSION_TEXT = "Second team you want EXCLUDED"
THIRD_EXCLUSION_TEXT = "Third team you want EXCLUDED"

EXCLUDED_GRADERS_LIST = [FIRST_EXCLUSION_TEXT, SECOND_EXCLUSION_TEXT, THIRD_EXCLUSION_TEXT]

SUID = "What is your SUID?"
STUDENT_NAME = "What is your name?"

DEFAULT_STUDENT_LIMIT = 5 # the default limit on the number of students for a particular grader team

# this is a list of the choices for graders, MUST BE FILLED BEFOREHAND
# mapping grader strings => {"students" : list of students, "limit": the upper limit of the number of students they can take}
GRADERS = {
	"Team 1: Tom and Griffin" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 2: Tom and Gautam" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 3: Tom and Sarah" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 4: Rebeca and Griffin" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 5: Rebeca and Gautam" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 6: Rebeca and Sarah" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 7: Griffin and Gautam" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 8: Griffin and Sarah" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 9: Gautam and Sarah" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 10: AnnaMaria Konya Tannon and Roxana Dantes" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 11: Wilson Farrar and Griffin" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 12: Wilson Farrar and Gautam" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 13: Wilson Farrar and Sarah" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 14: Yusuf Celik and Griffin" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 15: Yusuf Celik and Gautam" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT},
	"Team 16: Yusuf Celik and Sarah" : {"students" : [], "limit" : DEFAULT_STUDENT_LIMIT}
}

# read in data
data = pandas.read_csv(CSV_NAME)

# OPTION 1: randomize 
# ref: https://stackoverflow.com/questions/29576430/shuffle-dataframe-rows
data = data.sample(frac=1).reset_index(drop=True)	

# OPTION 2: go in existing order (first-come first-served)
# in this case, comment out previous line

# PRE-ASSIGNMENTS
# In the case that some students have been preferentially
# allotted to certain grading teams, then they can be entered here

for index, row in data.iterrows():
	choice_index = 0	# pointer for their choice index
	assignment_completed = False	# used to check if this student was assigned preferred grader. If not, 
	NUMBER_OF_CHOICES_SPECIFIED = sum([1 for j in range(len(GRADER_CHOICE_LIST)) if not pandas.isnull(row[GRADER_CHOICE_LIST[j]])])	# number of choices this student has specified, upto a max possible of 5

	# while you still have specified choices left, 
	# iterate over the choices specified
	# and see if you still have spots left
	while choice_index < NUMBER_OF_CHOICES_SPECIFIED:
		if pandas.isnull(row[GRADER_CHOICE_LIST[choice_index]]):
			# if this choice is null, we've reached the end of the choices. leave the loop.
			break

		# keep incrementing till you have a grader with spots left
		if len(GRADERS[row[GRADER_CHOICE_LIST[choice_index]]]["students"]) > GRADERS[row[GRADER_CHOICE_LIST[choice_index]]]["limit"]:
			# this grader goes NOT have spots left. Try next.
			choice_index += 1
		else:
			# this grader HAS spots left. assign to this, and move onto next student.
			GRADERS[row[GRADER_CHOICE_LIST[choice_index]]]["students"].append((row[SUID], row[STUDENT_NAME]))

			log(["Assigned", index, ".", row[STUDENT_NAME], "to grader", row[GRADER_CHOICE_LIST[choice_index]]])
			assignment_completed = True
			break

	if not assignment_completed:
		# if you've reached here, that means none of the top 5 choices had any spots left
		# create a set of the remaining graders, excluding:
		# 1. the ones the student doesn't want
		# 2. the ones who don't have spots left
		# 
		# assign randomly to one of these.

		log([index, ".", row[STUDENT_NAME], "will have to have some random grader assigned!"])

		EXCLUDED_GRADERS = [GRADERS[row[EXCLUDED_GRADERS_LIST[j]]] for j in range(len(EXCLUDED_GRADERS_LIST)) if not pandas.isnull(row[EXCLUDED_GRADERS_LIST[j]])]
		EXCLUDED_GRADERS += [grader for grader in GRADERS if len(GRADERS[grader]["students"]) > GRADERS[grader]["limit"]]
		log(["no of choices specified:", NUMBER_OF_CHOICES_SPECIFIED])
		log(["no of exclusions specified:", len(EXCLUDED_GRADERS)])

		REMAINING_GRADERS_LIST = set([grader for grader in GRADERS.keys() if grader not in EXCLUDED_GRADERS])

print "COMPLETED ASSIGNMENTS! Here's the count:"
total = 0
for grader in GRADERS.keys():
	current_count = len(GRADERS[grader]["students"])
	total += current_count
	print grader, ":", current_count

print "total students =", total