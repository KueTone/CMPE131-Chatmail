from app import myapp_obj, db
from app.models import User, Post
myapp_obj.app_context().push()

johnathon = User(username = 'kuetone',
                email='sammyshark@example.com',
                name='Johnathon',

                age = 20,
                bio='Marine biology student')
johnathon.set_password('password')
db.session.add(johnathon)

alicia = User(username = 'al',
                email='alicia@hotmail.com',
                name='alicia',

                age = 19,
                bio='aviation')
alicia.set_password('word')
db.session.add(alicia)

u = User(username = 'ExampleUser',
         email = 'user@example.com', 
         name = 'Who-ser', 

         age = 10, 
         bio = "This is an example of a user's profile and information")
u.set_password('pass')
db.session.add(u)

u2 = User(username = 'DeleteUserEx',
         email = 'user@example.com', 
         name = 'user', 

         age = 10, 
         bio = "Delete this user")
u2.set_password('delete')
db.session.add(u2)

u = User(username = 'kenneth0810',
         email = 'user@example.com', 
         name = 'Who-ser', 

         age = 10, 
         bio = "This is an example of a user's profile and information")
u.set_password('pass')
db.session.add(u)

email1 = Post(body = 'asdfjk l;qwe ruiopzx cvnm,.',
              author_id = 1, receive_id = 2)
db.session.add(email1)

email2 = Post(body = 'What are you here to?',
              author_id = 1, receive_id = 2)
db.session.add(email2)
email3 = Post(body = 'Big word register babes.', author_id = 2, receive_id = 1)
db.session.add(email3)

email4 = Post(body = 'What have you done??!??',
              author_id = 2 , receive_id = 1)
db.session.add(email4)

email5 = Post(body = 'Why am I here??!??', author_id=2, receive_id=1)
db.session.add(email5)

email6 = Post(body = 'This post is an example of receiving from a users deleted account', author_id=4, receive_id=1)
db.session.add(email6)

email7 = Post(body = 'This post is an example of sending to a users deleted account', author_id=1, receive_id=4)
db.session.add(email7)


db.session.commit()