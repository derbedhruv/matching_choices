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

GRADERS_LIST = []

# read in data
data = pandas.read_csv(CSV_NAME)

# OPTION 1: randomize 
data = data.sample(frac=1).reset_index(drop=True)

# OPTION 2: go in existing order (first-come first-served)
# in this case, comment out previous line

# PRE-ASSIGNMENTS
# In the case that some students have been preferentially
# allotted to certain grading teams, then they can be entered here

for index, row in df.iterrows():

