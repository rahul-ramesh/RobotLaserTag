import os
import httplib2

def restore():
	## this implements passive replication for the server in case of data loss
	if not(os.path.exists(db.sqlite)):
		os.system("cp backup.db.sqlite3 ../db.sqlite3")
		os.system("chmod 777 ../db.sqlite3")
		log = open('log.txt', 'rw')
		
		# add command for team 1
		cmd_1 = f.readline().split(" ")
		h = httplib2.Http(".cache")
		url_1 = "http://54.218.43.192/robot_tag/1/add_command/" + cmd_1[1]
		
		cmd_2 = f.readline().split(" ")
		url_2 = "http://54.218.43.192/robot_tag/1/add_command/" + cmd_2[1]
		
		h.request(url_1)
		h.request(url_2)


restore()
