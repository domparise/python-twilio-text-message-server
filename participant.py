# Dom Parise - 4/13/14
# participant model
#

import math
from random import random
from datetime import datetime,timedelta,date

# -ln(RND)/p hours
def poisson(p):
    return -( math.log(random()) / p )

# time is datetime
def add_poisson(p,time):
    return time + timedelta(minutes=(poisson(p)*60))

def p_value (day):
    if day < 28: # weeks 1-4
        return 1.5
    else: # week 5
        return 0.25

import time
from threading import Timer
from database import Database
db = Database()

class Participant:
    # initialize participants variables
    def __init__ (self, phone_number, lab_day, money_day, start_date, txt_messenger): #tested
        ## need to check these variables when working with db
        self.number = phone_number #
        self.day = (datetime.now() - start_date).days #
        self.num_today = 0 # 
        self.lab_day = lab_day.date() # date
        self.money_day = money_day.date() # date
        self.txt = txt_messenger
        self.on = False
        self.expecting = False

    # returns time (in minutes) as the day's 'start time'
    def next_day_start_time (self): #tested
        minutes = 0.0
        if self.day < 28: # weeks 1-4 # random time between 10am-4pm
            minutes = 600.0 + ( 360.0 * random() )
        elif self.day < 35: # week 5 # 10am
            minutes = 600.0 
        elif self.day < 42: # week 6 # random time between 10am-10pm
            minutes = 600.0 + ( 720.0 * random() )
        tmr = date.today() + timedelta(days=1)
        self.day += 1
        self.num_today = 0
        return datetime(year=tmr.year,month=tmr.month,day=tmr.day,hour=int(minutes/60),minute=int(minutes%60))

    # given the state of the participant in the study, determine next time to send 
    # real nasty logic, this can be improved
    def next_message (self): #not fully tested, but components tested
        # if after 22:00, get next_day_start_time if not target date
        # otherwise, depending on num_sent, determine next w/ poisson
        try:
            self.nonresponse_timer.cancel()
            self.message_timer.cancel()
        except:
            print 'No timer to cancel'
        now = datetime.now()
        next = add_poisson( p_value(self.day), now)
        if next.hour >= 22: # after 10pm
            if not self.tmr_is_target_day():
                self.set_next_msg( add_poisson(p_value(self.day), self.next_day_start_time()) )
        else:
            if self.day < 28: # weeks 1-4
                if self.num_today < 6:
                    self.set_next_msg(next)
                elif self.tmr_is_target_day():
                    return
                else:
                    self.set_next_msg( add_poisson( p_value(self.day), self.next_day_start_time() ))
            elif self.day < 35: # week 5
                if self.num_today < 3:
                    self.set_next_msg(next)
                elif self.tmr_is_target_day(): 
                    return
                else:
                    self.set_next_msg(add_poisson( p_value(self.day), self.next_day_start_time() ))
            elif not self.tmr_is_target_day(): # week 6
                self.set_next_msg( self.next_day_start_time() )
        return

    def send_text (self): #tested
        db.log(self.number, 'sent', 'default')
        self.txt.send_default_sms(self.number)
        self.expecting = True

    def nonresponse (self): #not yet fully tested
        db.log(self.number, 'nonresponse', 'resetting_poisson_process')
        self.message_timer.cancel()
        self.next_message()

    # spawns a thread to send a message a the given time
    def set_next_msg (self, time): #tested
        secs = (time - datetime.now()).total_seconds() 
        self.message_timer = Timer( secs, self.send_text).start()
        self.nonresponse_timer = Timer( (secs + 5400) , self.nonresponse).start() 

    def tmr_is_target_day (self): #tested
        tmr = date.today() + timedelta(days=1)
        if tmr == self.lab_day or tmr == self.money_day:
            return True
        return False

    def send_verification (self):
        db.log(self.number, 'sent', 'default')
        self.txt.send_verification(self.number)

