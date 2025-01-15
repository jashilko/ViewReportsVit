from sqlalchemy import text, MetaData, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_uniq, int_pk


class SiteUser(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str] = mapped_column(String(45))  # Максимум 64 символа
    password: Mapped[str] = mapped_column(String(100))  # Максимум 100 символа

    is_operator: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_teamlead: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_controller: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    phone_teamleader: Mapped[str] = mapped_column(String(45))  # Максимум 64 символа
    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        role = ''
        if self.is_admin:
            role = 'Админ'
        elif self.is_controller:
            role = 'Контролер'
        elif self.is_teamlead:
            role = 'Руководитель группы'
        else:
            role = 'Оператор'
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "is_operator": self.is_operator,
            "is_teamlead": self.is_teamlead,
            "is_controller": self.is_controller,
            "is_admin": self.is_admin,
            "phone_teamleader": self.phone_teamleader,
            "role": role
        }

class userman_users(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]