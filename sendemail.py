#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#return 0 if success, -1 if not
def send_email(subject, receivers, ccers, content):
	mail_host="smtp.ym.163.com" 
	mail_user="robot1@vmaxx.tech"  
	mail_pass="" 
	sender = 'robot1@vmaxx.tech'

	message = MIMEText(content, 'plain', 'utf-8')

	message['From'] = Header(sender)
	message['To'] =  Header(','.join(receivers))
	message['Cc'] = Header(','.join(ccers))

	message['Subject'] = Header(subject, 'utf-8')
	receivers.extend(ccers)
	 
	try:
		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 25)    
		smtpObj.login(mail_user,mail_pass)  
		smtpObj.sendmail(sender, receivers, message.as_string())
		print "email successfully sent"
		return 0
	except smtplib.SMTPException:
		print "error while sending the email"
		return -1

if __name__ == '__main__':
	subject = 'Python SMTP test'
	receivers = ['xhzhao@vmaxx.tech','jliu@vmaxx.tech']
	ccers = ['wlhuang@vmaxx.tech']
	content = "hey guys, i got this worked!"
	success = send_email(subject, receivers, ccers, content)
