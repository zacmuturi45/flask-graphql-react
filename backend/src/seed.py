from src import create_app
from src.models import db, User, Gemstone, Review, user_gemstones
from faker import Faker
import random

# faker is a library that generates random data, from usernames to colors to addresses. This saves us time during testing by providing us with fake bur realistic data.
fake = Faker()

gemstone_names = [
    "Ruby",
    "Emerald",
    "Tanzanite",
    "Aquamarine",
    "Alexandrite",
    "Labradorite",
    "Diamond",
    "Sapphire",
    "Citrine",
    "Tsavorite",
    "Quartz",
    "Lapis Lazuli",
    "Opal",
    "Topaz",
]


def create_fake_user():
    user = User(username=fake.user_name())
    return user


def create_fake_gemstone():
    gem = Gemstone(gemstone_name=random.choice(gemstone_names), color=fake.color_name())
    return gem


def seed():

    # Before adding new data, we first delete any existing data in all our tables to ensure we don't get duplicate entries. This is important when you want to reset our database and test things with a clean slate.
    db.session.query(user_gemstones).delete()
    db.session.query(User).delete()
    db.session.query(Gemstone).delete()
    db.session.query(Review).delete()

    # We create 10 fake users here by calling create_fake_user(), add them to the session, append them to the users list and commit them to the database
    users = []
    gems = []

    for _ in range(10):
        user = create_fake_user()
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # We do the same for the gemstones.
    for _ in range(50):
        gem = create_fake_gemstone()
        db.session.add(gem)
        gems.append(gem)
    db.session.commit()

    """ 
    *Associating Users with Gemstones and Reviews:- Here we create associations between our tables.
    * Each user is randomly assigned 1 to 5 gemstones. If a user doesn't already have the chosen gemstone, it is appended to their gemstone list.
    * For each gemstone a user owns, we create a review. The review content is generated using Faker's paragraph() method. We then assign the user_id and gemstone_id to the review to establish the relationships.
    """
    for u in users:
        for _ in range(random.randint(1, 5)):
            gem = random.choice(gems)

            if gem not in u.gems:
                u.gems.append(gem)

            review = Review(content=fake.paragraph(), user_id=u.id, gemstone_id=gem.id)
            db.session.add(review)
    db.session.commit()


"""
* Finally, we ensure this script runs when executed directly.
* This block of code ensures that when we run this file, it initializes the Flask app, sets up the database context, and calls the seed() function to populate our database.
"""
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
