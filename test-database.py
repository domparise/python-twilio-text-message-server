from database import Database

db = Database()
db.create_and_empty_tables()

db.log(1234, 'test', 'content')

print db.fetch_logs()

db.new_participant(123456789, 987654321, '2014-05-04', '2014-06-05')

db.update_participant(123456789,"twilio_number", 1111111111)

print db.load_participants()

db.create_and_empty_tables()