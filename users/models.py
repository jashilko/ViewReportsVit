from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_uniq, int_pk


class SiteUser(Base):
    id: Mapped[int_pk]
    phone_number: Mapped[str_uniq]
    password: Mapped[str]

    is_operator: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_teamlead: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_controller: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"