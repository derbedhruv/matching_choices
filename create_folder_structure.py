# create the required folder structure 
# for STLP graders to correct
# This will be uploaded to google drive
import pandas, os

BASE_FOLDER = './STLPs'

# read the document that has grader --> student name
GRADER_ASSIGNMENTS_FILE = "GEMWIN18_grader_assignments.xlsx"
xl = pandas.ExcelFile(GRADER_ASSIGNMENTS_FILE)
# GRADER_ASSIGNMENTS = pandas.read_excel(GRADER_ASSIGNMENTS_FILE)

if __name__ == "__main__":
	for grader in xl.sheet_names:
		print "creating folder", grader
		os.makedirs(os.path.join(BASE_FOLDER, grader))
		
		students = pandas.read_excel(xl, grader, header=1)["STUDENT NAME"].tolist()
		for student in students:
			os.makedirs(os.path.join(BASE_FOLDER, grader, student))

