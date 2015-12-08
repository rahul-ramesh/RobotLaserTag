import os

def snapshot():
	os.system("rm backup.db.sqlite3")
	os.system("cp ../db.sqlite3 backup.db.sqlite3")
	h = httplib2.Http(".cache")
	url_1 = "http://54.218.43.192/robot_tag/1/command/"
	url_2 = "http://54.218.43.192/robot_tag/1/command/"
	# parse and store to log
