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

# participant (phone,twilio,num_today,start_date,lab_day,money_day)
# 

class Database:

    # assumes valid input
    def new_participant(self, phone, twilio, lab_day, money_day):
        sql_wrap('insert into participant (phone,twilio,lab_day,money_day) values (?,?,?,?)',(phone, twilio, lab_day, money_day,))
        self.log(phone,'participant_joined','-')

    # 
    def load_participants(self):
        # initialize participants
        res = fetch_wrap('select phone,twilio,num_today,start_date,lab_day,money_day from participant')
        participants = list()
        for p in res:
            participants.append(p)
        return participants

    #
    def update_participant(self, number, field, value):
        # this is a really bad way to do an update like this, but these calls only come from code, so we probably dont need to worry about sql injections 
        sql_wrap('update participant set '+str(field)+' = ? where phone = ?',(value,number,))

    #
    def log(self, phone, event, content):
        # timestamp now, phone, event [sent|response], content
        sql_wrap('insert into log (phone, event, content) values (?,?,?)', (phone, event, content,))

    def fetch_logs(self):
        res = fetch_wrap('select timestamp,phone,event,content from log')
        logs = list()
        for log in res:
            logs.append({
                'timestamp': log[0],
                'phone': log[1],
                'event': log[2],
                'content': log[3]
            })
        return logs

    def log_email(self,addr,amount_seen):
        sql_wrap('insert into email (email,amount_seen) values (?,?)', (addr, amount_seen,))

    def fetch_email(self):
        res = fetch_wrap('select email,amount_seen,timestamp from email')
        logs = list()
        for log in res:
            logs.append({
                'email': log[0],
                'amount_seen': log[1],
                'timestamp': log[2]
            })
        return logs

    #
    def create_and_empty_tables(self):
        conn = sqlite3.connect(config_vars.db_name)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS participant')
        c.execute('DROP TABLE IF EXISTS log')
        c.execute('DROP TABLE IF EXISTS email')
        c.execute('CREATE TABLE participant ( phone int primary key, twilio int, num_today int default 0, start_date date default current_date, lab_day int, money_day int)')
        c.execute('CREATE TABLE log (timestamp datetime default current_timestamp, phone int, event text, content text)')
        c.execute('CREATE TABLE email (email text primary key, amount_seen real, timestamp datetime default current_timestamp)')
        conn.commit()
        c.close()
        conn.close()
