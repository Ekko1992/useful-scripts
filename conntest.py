#!/usr/local/bin python
import MySQLdb

def estconn():
	#connection to database
	conn = MySQLdb.connect(
		host = 'sql.vmaxx.tech',
		user = 'root',
		passwd = 'Xjtu123456',
		db = 'feature_registration',
		charset = 'utf8'
	)
	return conn

cur.execute("update tasks set status = \'Failed\' where xml_name like \'%" + xmlshort +"%\'" )
