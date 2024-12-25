from datetime import datetime


class RBCdr:
    def __init__(self, oper: str | None = None,
                 date_from: datetime | None = None,
                 date_to: datetime | None = None):
        self.oper = oper
        self.date_from = date_from
        self.date_to = date_to

    def to_dict(self) -> dict:
        data = {'oper': self.oper, 'date_from': self.date_from, 'date_to': self.date_to,}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
