class RBCdr:
    def __init__(self, src: str | None = None):
        self.src = src

    def to_dict(self) -> dict:
        data = {'src': self.src}
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
