from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

user_gemstones = db.Table(
    "user_gemstones",
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column(
        "gemstones_id", db.Integer, db.ForeignKey("gemstones.id"), primary_key=True
    ),
)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(55), unique=True, nullable=False)

    gemstones = db.relationship(
        "Gemstone", backref="user", cascade="all, delete-orphan"
    )
    reviews = db.relationship("Review", backref="user")


class Gemstone(db.Model):
    __tablename__ = "gemstones"

    id = db.Column(db.Integer, primary_key=True)
    gemstone_name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(55), nullable=False)
    reviews = db.relationship(
        "Review", backref="gemstone", cascade="all, delete-orphan"
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    gemstone_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
