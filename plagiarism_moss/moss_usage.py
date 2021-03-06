import mosspy
from scraper import *
import sys
userid = 881220386

import os
import sys
sys.path.append("/plagiarism_moss")
from db_access import *



def check_plagiarism(c_id):
	base_code = '''#include <stdio.h>
	int main(int argc, char **argv){
		printf("Hello C World!!\\n");
		return 0;
	}'''
	'''
	TODO: Database fetch
	RETURN : A dictionary of all the codes : 
		key : USN
		value : code as a string

	'''
	# return value ( (q_id:USN) -> code)


	# adding a base file
	with open("plagiarism_moss/submission/base.c", "w") as text_file:
			text_file.write(base_code)


	submissions = get_plagiarism_code(c_id)
	print(submissions)

	if(submissions==None):
		res = set_plagiarism_report(c_id,[])
		return 
	for usn in submissions.keys():
		if not os.path.exists("submission/questions/"+str(usn[0])):
			os.makedirs("submission/questions/"+str(usn[0]))
		with open("submission/questions/"+str(usn[0])+"/"+str(usn[1])+".c", "w") as text_file:
			text_file.write(submissions[usn]['code'])

	#for each directory

	directory_list = [x[0] for x in os.walk("submission/questions")]
	print(directory_list)
	del directory_list[0]
	final_list = []

	for question in directory_list:
		files_list = [x[2] for x in os.walk(question)]
		print(files_list)
		for file in files_list[0]:
			with open(os.path.join(question, file),"r") as f:
				if len(f.readlines()) < 2:
					## If file exists, delete it ##
					if os.path.isfile(os.path.join(question, file)):
						print("removing files")
						os.remove(os.path.join(question, file))
					else:    ## Show an error ##
						print("Error: %s file not found" % os.path.join(question, file) ) 

	for question in directory_list:
		current_dict = {}
		q_id = question.split()[-1]
		current_dict['q_id'] = q_id 
		m = mosspy.Moss(userid, "c")
		# can add a base file(skeleton code which need not be compared)
		m.addBaseFile("plagiarism_moss/submission/base.c")
		# Submission Files
		print(question)
		m.addFilesByWildcard(str(question)+"/*.c")
		try:
			url = m.send() # Submission Report URL
			
			print ("Report Url: " + url)

			# Save report file
			m.saveWebPage(url, "submission/report.html")

			# Download whole report locally including code diff links
		except:
			print("caught exception")
			continue


		mosspy.download_report(url, "submission/report/", connections=8)

		output = scrape_display(url)
		current_dict['report']=output
		final_list.append(current_dict)
		print(final_list)
	res = set_plagiarism_report(c_id,final_list)
	if(res==1):
		print("done checking")


