# Dom Parise - 4/13/14
# email sending module
#
import config_vars
import smtplib
from threading import Timer
from datetime import datetime
from database import Database

class Emailer:

	def email_to(self, to_addr, url):
		smtpserver = smtplib.SMTP('smtp.gmail.com',587)
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo
		smtpserver.login(config_vars.gmail_user, config_vars.gmail_pwd)
		header = 'To:' + to_addr + '\n' + 'From: ' + config_vars.gmail_user + '\n' + 'Subject:'+ config_vars.gmail_subject +' \n'
		msg = header + '\n '+ config_vars.gmail_text +' \n\n' + url + ' \n\n'
		smtpserver.sendmail(config_vars.gmail_user, to_addr, msg)
		smtpserver.close()
		db = Database()
		db.log_email(to_addr,'sent')

	def email(self, time, to_addr, url):
		secs = (time - datetime.now()).total_seconds()
		Timer(secs, self.email_to, (to_addr,url) ).start()