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

SUID = 'What is your SUID?'

GRADERS = {}	# this is a list of the choices for graders
# mapping grader strings => {"students" : list of students, "limit": the upper limit of the number of students they can take}

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

for index, row in df.iterrows():
	choice_index = 0	# pointer for their choice index
	while(pandas.isnull(GRADERS[row[GRADER_CHOICE_LIST[choice_index]]]) and len(GRADERS[row[GRADER_CHOICE_LIST[choice_index]]]["students"]) >= GRADERS[row[GRADER_CHOICE_LIST[choice_index]]]["limit"]):
		# keep incrementing till you have a grader with spots left
		choice_index += 1
	if choice_index < 5:
		# one of their first 5 choices still has a spot
		# assign to them, finish
		GRADERS[row[GRADER_CHOICE_LIST[choice_index]]]["students"].append(row[SUID])
		continue
	# if you've reached here, that means none of the top 5 choices had any spots left
	# create a set of the remaining graders, exclude the ones the student doesn't want
	# assign to one of the remaining graders who still has spots open
	REMAINING_GRADERS_LIST = set([grader for grader in GRADERS.keys() if grader not in [GRADERS[row[GRADER_CHOICE_LIST[j]]] for j in range(5)]])

