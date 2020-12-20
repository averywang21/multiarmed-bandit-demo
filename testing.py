from flaskblog import create_app
app = create_app()
app.app_context().push()

from flaskblog import db
from flaskblog.models import User, Machine
from flaskblog import bcrypt

db.drop_all()
db.create_all()

user0 = User(id=1, username='averyw09521', email='averyw09521@gmail.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8'))
user1 = User(id=2, username='emily', email='emily@gmail.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8'))

games = [([0.2, 0.3, 0.7, 0.6], 10), ([0.2, 0.2, 0.9], 100)]
users = [1, 2]

db.session.add(user0)
db.session.add(user1)
db.session.commit()

for game_id, (probs, attempts) in enumerate(games):
    for user in users:
        for machine_id, machine_prob in enumerate(probs):
            machine = Machine(user_id=user, machine_number=machine_id, game_number=game_id, true_prob = machine_prob, max_attempts=attempts)
            db.session.add(machine)

db.session.commit()