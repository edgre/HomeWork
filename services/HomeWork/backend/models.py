import sqlalchemy as sql
import sqlalchemy.orm as orm
import passlib.hash as hash
import sqlalchemy.ext.declarative as declarative

Base = declarative.declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    username = sql.Column(sql.String(50), unique=True, nullable=False)
    realname = sql.Column(sql.String(50), unique=False, nullable=False)
    password_hash = sql.Column(sql.String, nullable=False)
    user_rating = sql.Column(sql.Float, nullable=False, default=0.0)
    has_draft =sql.Column(sql.Boolean, nullable=False, default=False)


    GDZ = orm.relationship("GDZ", back_populates="user")
    purchases = orm.relationship("Purchase", back_populates="buyer")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.password_hash)

class Subjects(Base):
    __tablename__ = 'subjects'

    subject_name = sql.Column(sql.String(100), index=True)
    category = sql.Column(sql.String(100), nullable=False)
    paths = sql.Column(sql.String(100), primary_key=True, nullable=False)

class GDZ(Base):
    __tablename__ = 'gdz'

    id = sql.Column(sql.Integer, primary_key=True, index=True)
    owner_id = sql.Column(sql.Integer, sql.ForeignKey("users.id"))
    description = sql.Column(sql.String(100), nullable=False)
    full_description = sql.Column(sql.String(250), nullable=False)
    category =  sql.Column(sql.String(250), nullable=False)
    price = sql.Column(sql.Integer)
    content = sql.Column(sql.String(100), nullable=True)
    content_text = sql.Column(sql.String(1000), nullable=False)
    is_elite = sql.Column(sql.Boolean, default=False, nullable=False)

    user = orm.relationship("User", back_populates="GDZ")


class Purchase(Base):
    __tablename__ = 'purchases'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    buyer_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    gdz_id = sql.Column(sql.Integer, sql.ForeignKey('gdz.id'))

    buyer = orm.relationship("User", back_populates="purchases")
    gdz = orm.relationship("GDZ")

class GDZRating(Base):
    __tablename__ = 'gdz_ratings'
    __table_args__ = (
        sql.Index('ix_gdz_rating_gdz_id', 'gdz_id'),
    )
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    gdz_id = sql.Column(sql.Integer, sql.ForeignKey('gdz.id'))
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    value = sql.Column(sql.Float, nullable=False)
    created_at = sql.Column(sql.DateTime, nullable=False)

    gdz = orm.relationship("GDZ")
    user = orm.relationship("User")


class Codes(Base):
    __tablename__ = 'codes'
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    gdz_id = sql.Column(sql.Integer, sql.ForeignKey('gdz.id'))
    user_id = sql.Column(sql.Integer, sql.ForeignKey('users.id'))
    code = sql.Column(sql.String(1000), nullable=False)

    user = orm.relationship("User")
    gdz = orm.relationship("GDZ")
