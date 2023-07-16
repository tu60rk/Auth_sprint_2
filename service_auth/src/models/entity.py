import uuid
from datetime import datetime


from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from werkzeug.security import generate_password_hash

Base = declarative_base()


class BaseMixin:
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base, BaseMixin):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hash_password = Column(String(255), nullable=False)
    verified = Column(Boolean, nullable=False, server_default='False')
    is_active = Column(Boolean, nullable=False, server_default='True')

    def __init__(
            self,
            first_name: str,
            last_name: str,
            email: str,
            password: str
    ) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password = generate_password_hash(password)

    def __repr__(self) -> str:
        return f'<User {self.email}>'


class UserRoles(Base, BaseMixin):
    __tablename__ = 'usersroles'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'))


class Role(Base, BaseMixin):
    __tablename__ = 'roles'

    name = Column(String(15), nullable=False)
    description = Column(String(255), nullable=False)

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


class AccountHistory(Base, BaseMixin):
    __tablename__ = 'account_history'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    user_agent = Column(String(255), nullable=False, server_default='default UA')  # здесь потом должна быть функция получающая useragent


class RefreshToken(Base, BaseMixin):
    __tablename__ = 'refresh_tokens'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    user_token = Column(String(600), nullable=False, server_default='default UT')  # здесь потом должна быть функция получающая user_token
    is_active = Column(Boolean, nullable=False, server_default='False')
    user_agent = Column(String(255), nullable=False, server_default='default UA')  # здесь потом должна быть функция получающая useragent
