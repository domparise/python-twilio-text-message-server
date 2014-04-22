# Dom Parise - 4/13/14
# Response handling server module
# To install dependencies: sudo pip install Flask
#

# submit new user screen refresh back to submit new user
# write tutorial / walkthrough
# comment code

import config_vars
from database import Database
from participant import Participant
from textmessenger import TextMessenger
from datetime import datetime
from random import random

def is_valid_response(s):
    # make sure time is numeric text within 1-100 inclusive
    try:
        n = int(s)
        if n >= 1 and n <= 100 and not n%5 == 0:
            return True 
        else: return False
    except:
        return False

def valid_time(date_text): 
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except:
        return False

def valid_number(number):
    if len(str(number)) == 11:
        return int(number)
    return False


db = Database()
participants = dict()
participant_tuples = db.load_participants()
for i in range(len(participant_tuples)):
    cur_part = participant_tuples[i]
    txtr = TextMessenger(valid_number(cur_part[1]))
    participants[valid_number(cur_part[0])] = Participant(cur_part[0],valid_time(cur_part[2]),valid_time(cur_part[3]),valid_time(cur_part[4]),txtr)
    participants[valid_number(cur_part[0])].next_message()

print participants

## added to test receiving texts
# participants = dict()
# txt = TextMessenger(17348884244)
# participants[int(16169162477)] = Participant(16169162477,datetime.now(),valid_time('2014-05-03'),valid_time('2014-06-02'),txt)

from flask import Flask, request, Response, render_template
import twilio.twiml
app = Flask(__name__)

# todo: make sure next message doesnt trigger if user randomly texts valid input
#
#
@app.route('/receiver', methods=['POST'])
def respond_to_text():
    # Respond to incoming calls with a simple text message
    number = valid_number(request.form['From'][1:])
    request_text = request.form['Body']
    if number:
        db.log(number, 'received', request_text)
    if number in participants: # message received from a number we've recently messaged
        if is_valid_response(request_text): # valid response 
            participants[number].num_today += 1
            participants[number].expecting = False
            participants[number].next_message()
            return
        else: # invalid response, ask for a valid answer 
            resp = twilio.twiml.Response()
            resp.message(config_vars.invalid_sms_response)
            return str(resp)
    return

@app.route('/', methods=['GET'])
def display_all_data():
    return render_template('data.html')

@app.route('/sms', methods=['POST'])
def display_sms_data():
    if request.form['pwd'] == config_vars.interface_pwd:
        # display the main table
        data = db.fetch_logs()
        csv = 'time, phone_number, event, content\n'
        for datum in data:
            csv +=  str(datum[0]) + ', ' + str(datum[1]) + ', ' + str(datum[2]) + ', ' + str(datum[3]) + '\n'
        return Response(csv,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"});
    else return 'incorrect password'

@app.route('/new-participant', methods=['GET','POST'])
# display participant, and handle post new participant
def new_participant():
    if request.method == 'GET':
        return render_template('new-participant.html')
    else: # password = economics
        if request.form['pwd'] == config_vars.interface_pwd:
            # create new participant
            lab_day = valid_time(request.form['lab_day'])
            money_day = valid_time(request.form['money_day'])
            phone_number = valid_number(request.form['phone'])
            twilio_number = valid_number(request.form['twilio'])
            if lab_day and money_day and phone_number and twilio_number:
                txt = TextMessenger(twilio_number)
                participants[phone_number] = Participant(phone_number,datetime.now(),lab_day,money_day,txt)
                db = Database()
                db.new_participant(phone_number,twilio_number,request.form['lab_day'],request.form['money_day'])
                return render_template('new-participant.html')
        return 'invalid input'

@app.route('/participants')
    if request.form['pwd'] == config_vars.interface_pwd:
        # display the main table
        csv = 'time, phone_number, event, content\n'
        for participant in participants:
            csv +=  str(datum[0]) + ', ' + str(datum[1]) + ', ' + str(datum[2]) + ', ' + str(datum[3]) + '\n'
        return 
    else return 'incorrect password'

## need to implement showing current data
@app.route('/participant/<int:number>', methods=['GET','POST'])
def display_participant(number):
    # display participant info, and send messages
    if request.method == 'GET':
        if number in participants:
            return render_template('participant.html', number=number, twilio_number=participants[number].txt.from_number, lab_day=participants[number].lab_day, money_day=participants[number].money_day)
        else:
            return 'unknown phone number'
    else: # password = economics
        if request.form['pwd'] == config_vars.interface_pwd:
            if 'edit' in request.form: # show the edit form
                return render_template('edit-participant.html', number=number)
            elif 'verification' in request.form: # send verification text
                participants[number].send_verification()
            elif 'target' in request.form: # begin on target day
                today = datetime.today()
                time = datetime.strptime(request.form['target_time'],'%H:%M')
                when = datetime(year=today.year, month=today.month, day=today.day, hour=time.hour, minute=time.minute)
                participants[number].set_next_msg(when)     
            else:
                field = ''
                val = None
                if 'twilio_number' in request.form:
                    field = 'twilio_number'
                    val = request.form['twilio_number_val']
                    participants[number].txt = TextMessenger(val)
                elif 'lab_day' in request.form:
                    field = 'lab_day'
                    val = request.form['lab_day_val']
                    participants[number].lab_day = valid_time(val)
                elif 'money_day' in request.form:
                    field = 'money_day'
                    val = request.form['money_day_val']
                    participants[number].money_day = valid_time(val)
                db.update_participant(number, field, val)
            return 'success'
        else:
            return 'invalid input'


@app.route('/email', methods=['GET','POST'])
def handle_email():
    if request.method == 'GET':
        return render_template('input-email.html')
    else:
        rand = random()
        amt = ''
        if rand < 0.25:
            amt = '$1'
        elif rand >= 0.25 and rand < 0.50:
            amt = '$5'
        elif rand >= 0.50 and rand < 0.75:
            amt = '$25'
        elif rand >= 0.75:
            amt = '$125'
        db.log_email(request.form['email'],amt)
        return render_template('amount.html', amount=amt)

# need to implement database fetch email data
@app.route('/email-data')
    if request.form['pwd'] == config_vars.interface_pwd:
        # display the main table
        data = db.fetch_logs()
        csv = 'time, phone_number, event, content\n'
        for datum in data:
            csv +=  str(datum[0]) + ', ' + str(datum[1]) + ', ' + str(datum[2]) + ', ' + str(datum[3]) + '\n'
        return Response(csv,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"});
    else return 'incorrect password'


if __name__ == "__main__":
    try:
        app.run(debug=True,host='0.0.0.0',threaded=True)
    except (KeyboardInterrupt, SystemExit):
        cleanup_stop_thread();
        sys.exit()
        