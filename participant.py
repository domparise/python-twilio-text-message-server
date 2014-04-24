# Dom Parise - 4/13/14
# participant model
#

import math
from random import random
from datetime import datetime,timedelta,date

# -ln(RND)/p hours
def poisson(p):
    return -( math.log(random()) / p )

import time
from threading import Timer,Thread
from database import Database
from textmessenger import TextMessenger
db = Database()

class Participant:
    # initialize participants variables
    def __init__ (self, phone, twilio, num_today, start_date, lab_day, money_day): 
        ## need to check these variables when working with db
        self.phone = phone #
        self.txt = TextMessenger(twilio) # int
        self.num_today = num_today # int
        self.day = (datetime.now() - start_date).days #
        self.lab_day = lab_day # int
        self.money_day = money_day # int
        self.message_timer = 'gonna be a thread'
        self.nonresponse_timer = 'gonna be a thread'
 
    # returns time (in minutes) as the day's 'start time'
    def next_day_start_time (self): #tested
        minutes = 0.0
        if self.day <= 28: # weeks 1-4 # random time between 10am-4pm
            minutes = 600.0 + ( 360.0 * random() )
        elif self.day <= 35: # week 5 # 10am
            minutes = 600.0 
        elif self.day <= 42: # week 6 # random time between 10am-10pm
            minutes = 600.0 + ( 720.0 * random() )
        tmr = date.today() + timedelta(days=1)
        self.day += 1
        self.num_today = 0
        return datetime(year=tmr.year,month=tmr.month,day=tmr.day,hour=int(minutes/60),minute=int(minutes%60))

    # given the state of the participant in the study, determine next time to send 
    def next_message_time (self): 
        # if after 22:00, get next_day_start_time if not target date
        # otherwise, depending on num_sent, determine next w/ poisson
        now = datetime.now()
        now = datetime(year=now.year,month=now.month,day=now.day,hour=12) # altered datetime for testing
        next = self.add_poisson( now )
        if next.hour >= 22: # after 10pm
            return self.add_poisson( self.next_day_start_time() )
        else:
            if self.day < 28 and self.num_today < 6: # weeks 1-4
                return next
            elif self.day < 35 and self.num_today < 3: # week 5
                return next
            elif self.day >= 42: # week 6
                return self.next_day_start_time()
            else:
                return self.add_poisson( self.next_day_start_time() )

    # time is datetime
    def add_poisson(self,time):
        p = 0
        if self.day < 28:
            p = 1.5
        elif self.day < 35:
            p = 0.25
        return time + timedelta(minutes=(poisson(p)*60))

    def next_message (self):
        if isinstance(self.nonresponse_timer,Thread) and self.nonresponse_timer.is_alive():
            self.nonresponse_timer.cancel()
        if isinstance(self.message_timer,Thread) and self.message_timer.is_alive():
            self.message_timer.cancel()
        self.set_next_msg( self.next_message_time() )

    def send_text (self): #tested
        db.log(self.number, 'sent', 'default')
        self.txt.send_default_sms(self.number)

    def nonresponse (self): #not yet fully tested
        db.log(self.number, 'nonresponse', 'resetting_poisson_process')
        self.next_message()

    # spawns a thread to send a message a the given time
    def set_next_msg (self, time): #tested
        secs = (time - datetime.now()).total_seconds() 
        self.message_timer = Timer( secs, self.send_text)
        self.nonresponse_timer = Timer( (secs + 5400) , self.nonresponse) 
        self.message_timer.start()
        self.nonresponse_timer.start()

    def send_verification (self):
        db.log(self.number, 'sent', 'default')
        self.txt.send_verification(self.number)
