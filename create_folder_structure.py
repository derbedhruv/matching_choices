# create the required folder structure 
# for STLP graders to correct
# This will be uploaded to google drive
import pandas, os
from shutil import copyfile

BASE_FOLDER = './STLPs'
GRADING_TEMPLATE_FILE = 'GEMWIN18.STLP_gradesheet.xls'

student_names = {}
total_stlps = 0

# read the document that has grader --> student name
GRADER_ASSIGNMENTS_FILE = "GEMWIN18_grader_assignments.xlsx"
xl = pandas.ExcelFile(GRADER_ASSIGNMENTS_FILE)
# GRADER_ASSIGNMENTS = pandas.read_excel(GRADER_ASSIGNMENTS_FILE)

if __name__ == "__main__":
	for grader in xl.sheet_names:
		grader_folder_name = grader + " STLPs for GEMWIN18"
		os.makedirs(os.path.join(BASE_FOLDER, grader_folder_name))
		copyfile(GRADING_TEMPLATE_FILE, os.path.join(BASE_FOLDER, grader_folder_name, GRADING_TEMPLATE_FILE))
		
		students = pandas.read_excel(xl, grader, header=1)["STUDENT NAME"].tolist()
		print grader, ":", len(students), "students"
		for student in students:
			# create subdirectory with student name
			os.makedirs(os.path.join(BASE_FOLDER, grader_folder_name, student))
			student_names[student] = 1
			total_stlps += 1

	print "total students =", len(student_names.keys())
	print "total STLPs to be graded =", total_stlps
