import os
import sqlalchemy as sa
from datetime import date
import sqlalchemy.orm as so
from typing import Optional
from flask_login import UserMixin
import pydenticon, hashlib, base64
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login
from app.enums import GenderEnum, BloodGroupEnum


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True, nullable=False)
    phone: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=False)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=False)
    
    profile: so.Mapped['Profile'] = so.relationship('Profile', back_populates='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gen_avatar(self, size=36, write_png=True):
        foreground = [ 
            "rgb(45,79,255)",
            "rgb(254,180,44)",
            "rgb(226,121,234)",
            "rgb(30,179,253)",
            "rgb(232,77,65)",
            "rgb(49,203,115)",
            "rgb(141,69,170)"
        ]
        background = "rgb(256,256,256)"

        digest = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        basedir = os.path.abspath(os.path.dirname(__file__))
        pngloc = os.path.join(basedir, 'usercontent', 'identicon', str(digest) + '.png')
        icongen = pydenticon.Generator(5, 5, digest=hashlib.md5, foreground=foreground, background=background)
        pngicon = icongen.generate(self.email, size, size, padding=(8, 8, 8, 8), inverted=False, output_format="png")
        if write_png:
            pngfile = open(pngloc, "wb")
            pngfile.write(pngicon)
            pngfile.close()
        else:
            return str(base64.b64encode(pngicon))[2:-1]
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Profile(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    dob: so.Mapped[date] = so.mapped_column(sa.Date, nullable=False)
    gender: so.Mapped[GenderEnum] = so.mapped_column(sa.Enum(GenderEnum), nullable=False)
    phone: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=False)
    state: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    zip_code: so.Mapped[str] = so.mapped_column(sa.String(10), nullable=False)
    blood_group: so.Mapped[BloodGroupEnum] = so.mapped_column(sa.Enum(BloodGroupEnum), nullable=False)

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, unique=True, nullable=False)
    user: so.Mapped['User'] = so.relationship('User', back_populates='profile')

    def __repr__(self):
        return '<Profile for User {}>'.format(self.user.username)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))