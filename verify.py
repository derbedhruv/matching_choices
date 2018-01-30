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
	preferences = pandas.read_csv(CSV_NAME, parse_dates=["Timestamp"])
	preferences = preferences.groupby(SUID).last().reset_index()

	assignments = pandas.read_excel(OUTPUT_FILENAME2)


