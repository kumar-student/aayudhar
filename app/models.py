import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(10))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin: so.Mapped[Optional[bool]] = so.mapped_column(sa.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))