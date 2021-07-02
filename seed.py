from app import app
from models import db, Item, User

db.drop_all()
db.create_all()

u1 = User.register("jarredbaird@gmail.com", "jarred")
u1.google_email_address = "jarredbaird@gmail.com"
u2 = User.register("eviluser@gmail.com", "evilpassword")
db.session.add_all([u1, u2])
db.session.commit()


i1 = Item(
    i_title="meh, someday I'll workout",
    u_id = 1
)

i2 = Item(
    i_title="Gotta do it",
    u_id = 1
    )

i3 = Item(
    i_title="Shouldn't be able to see this",
    u_id = 2
)

db.session.add_all([i1, i2, i3])
db.session.commit()