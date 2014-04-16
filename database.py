# Dom Parise - 4/13/14
# Persistence layer
# 
import sqlite3
import config_vars

def sql_wrap(query,tupl):
    conn = sqlite3.connect(config_vars.db_name)
    c = conn.cursor()   
    c.execute(query,tupl)
    conn.commit()
    c.close()
    conn.close()

def fetch_wrap(query):
    conn = sqlite3.connect(config_vars.db_name)
    c = conn.cursor()   
    res = c.execute(query).fetchall()
    conn.commit()
    c.close()
    conn.close()
    return res

class Database:

    # assumes valid input
    def new_participant(self, phone_number, twilio_number, lab_target_day, money_target_day):
        # int, int, str_date, str_date, ie '2014-05-04'
        t = (phone_number, twilio_number, lab_target_day, money_target_day,)
        sql_wrap('insert into participant (phone_number,twilio_number,lab_day,money_day) values (?,?,?,?)', t)
        self.log(phone_number,'participant_joined','-')

    #
    def update_participant(self, number, field, value):
        # this is a really bad way to do an update like this, but these calls only come from code, so we probably dont need to worry about sql injections 
        sql_wrap('update participant set '+str(field)+' = ? where phone_number = ?',(value,number))

    #
    def log(self, number, event, content):
        # timestamp now, number, event [sent|response], content
        t = (number, event, content,)
        sql_wrap('insert into log (number, event, content) values (?,?,?)', (number, event, content) )

    #
    def fetch_logs(self):
        return fetch_wrap('select timestamp,number,event,content from log')

    # 
    def load_participants(self):
        # initialize participants
        return fetch_wrap('select phone_number,twilio_number,lab_day,money_day,start_date from participant')

    def log_email(self,addr,amount_seen):
        t = (addr, amount_seen,)
        sql_wrap('insert into email (email,amount_seen) values (?,?)',t)

    def hasnt_emailed(self, addr):
        conn = sqlite3.connect(config_vars.db_name)
        c = conn.cursor()   
        res = c.execute('select count(*) from email where email=?',(addr,)).fetchall()
        conn.commit()
        c.close()
        conn.close()
        if int(res[0][0]) == 1:
            return True
        else:
            return False

    #
    def create_and_empty_tables(self):
        conn = sqlite3.connect(config_vars.db_name)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS participant')
        c.execute('DROP TABLE IF EXISTS log')
        c.execute('DROP TABLE IF EXISTS email')
        c.execute('CREATE TABLE participant ( phone_number int primary key, twilio_number int, lab_day date, money_day date, start_date date default current_date)')
        c.execute('CREATE TABLE log (timestamp datetime default current_timestamp, number int, event text, content text)')
        c.execute('CREATE TABLE email (email text primary key, amount_seen real, timestamp datetime default current_timestamp)')
        conn.commit()
        c.close()
        conn.close()

#CREATE TABLE participant ( phone_number int primary key, twilio_number int, lab_day date, money_day date, start_date date default current_date);
#CREATE TABLE log (timestamp datetime default current_timestamp, number int, event text, content text);
