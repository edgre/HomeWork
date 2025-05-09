import sqlalchemy as sql
import sqlalchemy.orm as orm
import passlib.hash as hash
import database as db

class User(db.Base):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    username = sql.Column(sql.String(50), unique=True, nullable=False)
    realname = sql.Column(sql.String(50), unique=False, nullable=False)
    password_hash = sql.Column(sql.String, nullable=False)

    GDZ = orm.relationship("GDZ", back_populates="user")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password_hash)


class GDZ(db.Base):
    __tablename__ = 'posts'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.String(
        50), sql.ForeignKey("users.username"))
    description = sql.Column(sql.String(250), nullable=False)
    textbook_and_exercise = sql.Column(sql.String(250), nullable=False)
    category = sql.Column(sql.String(250), nullable=False)
    grade =  sql.Column(sql.String(250), nullable=False)
    content = sql.Column(sql.String(10000), nullable=False)
    rating = sql.Column(sql.Integer, default=0)
    is_elite = sql.Column(sql.Boolean, default=0)

    user = orm.relationship("User", back_populates="GDZ")

