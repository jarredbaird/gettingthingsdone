from app import app
from models import db, Item

db.drop_all()
db.create_all()

i1 = Item(
    i_title="meh, someday I'll workout",
)

i2 = Item(
    i_title="Gotta do it",
    )

db.session.add_all([i1, i2])
db.session.commit()