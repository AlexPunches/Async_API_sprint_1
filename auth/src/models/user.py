"""SQLAlchemy-модель Пользователя для БД."""

import uuid

from flask_security import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from core.db import db
from models import BaseModel, roles_users


class User(BaseModel, UserMixin):
    """Модель пользователя.

    В проекте используем библиотеку flask-security-too
    базовый набор полей Пользователя зависит от нее
    https://flask-security-too.readthedocs.io/en/stable/models.html
    """

    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    login = db.Column(db.String, unique=True, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, lazy='subquery',
                            backref=db.backref('users', lazy='subquery'))

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    def __str__(self):
        """Вернуть в виде строки."""
        return self.login

    def __repr__(self):
        """Вернуть в виде строки."""
        return f'<User {self.email}>'

    def get_security_payload(self):
        """Верунть кастомный User Payload."""
        return {
            'id': self.id,
            'login': self.login,
            'email': self.email,
        }
