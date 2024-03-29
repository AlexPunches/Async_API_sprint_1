"""Модель аккаунтов в соцсетях."""
import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres import db
from models import BaseModel, User


class SocialAccount(BaseModel):
    """Модель соцаккаунта с привязкой к юзеру."""

    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                   unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'),
                        nullable=False)
    user = db.relationship(User, backref=db.backref('social_accounts',
                                                    lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (db.UniqueConstraint('social_id', 'social_name',
                                          name='social_pk'), )

    def __repr__(self):
        """repr()."""
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
