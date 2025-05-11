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
    __tablename__ = 'gdz'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.String(
        50), sql.ForeignKey("users.username"))
    description = sql.Column(sql.String(250), nullable=False)
    textbook = sql.Column(sql.String(250), nullable=False)
    exercise =sql.Column(sql.String(25), nullable=False)
    subject = sql.Column(sql.String(250), nullable=False)
    category =  sql.Column(sql.String(250), nullable=False)
    content = sql.Column(sql.String(100), nullable=False)
    content_text = sql.Column(sql.String(1000), nullable=False)
    rating = sql.Column(sql.Integer, default=0)
    is_elite = sql.Column(sql.Boolean, default=False, nullable=False)

    user = orm.relationship("User", back_populates="GDZ")

class Purchase(db.Base):
    __tablename__ = 'purchases'
    id = sql.Column(sql.Integer, primary_key=True)
    buyer_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    gdz_id = sql.Column(sql.Integer, sql.ForeignKey('posts.id'))

