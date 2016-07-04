import csv,mysql.connector


class CSV_TO_SQL:

	def __init__(self,database):
		self.__database = database

# accept a file and import it into mysql
	def insertIntoTable(self,f,course_run,uni ='university of Southampton'):
		_file = open(f)
		_reader = csv.reader(_file)
		head  = next(_reader)
		_filename, _extend = f.split('.')
		course , datatype = _filename.split('_')
		c = course.split('/')
		course = c[len(c) - 1]
		cursor = self.__database.cursor()
		delete = ''
		load = ''
	

		if 'comments' in datatype:
			col = ''
			setting = ''

			
			if(len(head) == 8):
				col = 	"(id,author_id,@parent_id,@step,@text,@timestamp,@moderated,@likes) "
				setting = "step = @step,week = SUBSTRING_INDEX(@step,'.',1),stepNumber = SUBSTRING_INDEX(@step,'.',-1),"\
				"text = @text,timestamp = @timestamp,Likes = @Likes, "''

			else:
				col = "(id,author_id,@parent_id,step,week,stepNumber,text,timestamp,@moderated,likes) "

			load = 'LOAD DATA LOCAL INFILE '"'" + f + "'"' REPLACE INTO TABLE Comments ' \
			"FIELDS TERMINATED BY ',' ENCLOSED BY "+  '\'"\''  \
			'IGNORE 1 LINES ' + col +\
			"Set parent_id = nullif(@parent_id,' '), "+ setting +"moderated = nullif(@moderated,' '),university = " + "'" + uni + "'," + "course = " + "'" + course + "'," + "course_run = " \
			+ str(course_run) + ";"
			

		elif 'enrolments' in datatype:
			
		
			load = 'LOAD DATA LOCAL INFILE '"'" + f + "'"' REPLACE INTO TABLE Enrolments ' \
			"FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' "  +  \
			'IGNORE 1 LINES ' \
			"(learner_id,enrolled_at,@unenrolled_at,role,@fully_participated_at,@purchased_statement_at,gender,country,age_range,highest_education_level,employment_status,employment_area) "\
			"Set unenrolled_at = nullif(@unenrolled_at,' '),fully_participated_at = nullif(@fully_participated_at,' '),purchased_statement_at = nullif(@purchased_statement_at,' '),university = " + "'" + uni + "'," + "course = " + "'" + course + "'," + "course_run = " \
			+ str(course_run)  + ";"  
			
			
		
		elif 'assignments' in datatype:	

			col = 	"(id,step,step_number,week_number,author_id,text,first_viewed_at,submitted_at,@moderated,review_count) "
			

			load = 'LOAD DATA LOCAL INFILE '"'" + f + "'"' REPLACE INTO TABLE Assignments ' \
			"FIELDS TERMINATED BY ',' ENCLOSED BY "+  '\'"\''  \
			'IGNORE 1 LINES '  + col + \
			"Set moderated = nullif(@moderated,' '),university = " + "'" + uni + "'," + "course = " + "'" + course + "'," + "course_run = " \
			+ str(course_run) + ";"  
			

		elif 'reviews' in datatype:

			col = '(id,step,week_number,step_number,reviewer_id,assignment_id,guideline_one_feedback,guideline_two_feedback,guideline_three_feedback,created_at)'
				

			load = 	'LOAD DATA LOCAL INFILE '"'" + f + "'"' REPLACE INTO TABLE Reviews ' \
			"FIELDS TERMINATED BY ',' ENCLOSED BY "+  '\'"\''  \
			'IGNORE 1 LINES '  + col  + \
			"Set university = " + "'" + uni + "'," + "course = " + "'" + course + "'," + "course_run = " \
			+ str(course_run) + ";"
			

		elif 'question' in datatype:


			load = 	'LOAD DATA LOCAL INFILE '"'" + f + "'"' REPLACE INTO TABLE Quiz ' \
			"FIELDS TERMINATED BY ',' ENCLOSED BY "+  '\'"\''  \
			'IGNORE 1 LINES ' + "(learner_id,quiz_question,week_number,step_number,question_number,response,submitted_at,@correct)" +\
			"Set correct = STRCMP(@correct,'TRUE') + 1, university = " + "'" + uni + "'," + "course = " + "'" + course + "'," + "course_run = " \
			+ str(course_run) + ";"
			

		elif 'activity' in datatype:

			col = ''
			setting = ''
			if(len(head) == 4):
				col = '(learner_id,@step,@first_visited_at,@last_completed_at)'				
				setting = "step = @step, week = SUBSTRING_INDEX(@step,'.',1),stepNumber = SUBSTRING_INDEX(@step,'.',-1)," \
				" first_visited_at = @first_visited_at, "
			else:
				col = '(learner_id,step,week,stepNumber,first_visited_at,@last_completed_at)'


			load = 'LOAD DATA LOCAL INFILE '"'" + f + "'"' REPLACE INTO TABLE Activity ' \
			"FIELDS TERMINATED BY ',' "  \
			"IGNORE 1 LINES " + col +\
			"Set " + setting + "last_completed_at = nullif(@last_completed_at,' '),university = " + "'" + uni + "'," + "course = " + "'" + course + "'," + "course_run = " \
			+ str(course_run) + ";" 
		
		
	
			
		cursor.execute(load)
		self.__database.commit()
		cursor.close()
		_file.close()
	
	