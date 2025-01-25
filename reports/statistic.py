def formated_time(time)-> str:
    return "{:02}:{:02}:{:02}".format(
    int(time) // 3600,             # Часы
    (int(time) % 3600) // 60,      # Минуты
    int(time) % 60                 # Секунды
)

class Statistic:
    def __init__(self, list_of_records, phone=None):
        self.list_of_records = list_of_records
        self.phone = phone

    def get_user_stat(self):
        total_calls = len(self.list_of_records)
        incoming_calls = len([r for r in self.list_of_records if r["dst"] == self.phone])
        outgoing_calls = len([r for r in self.list_of_records if r["src"] == self.phone])
        # Фильтруем записи, где длительность больше 0
        calls_with_duration = [r for r in self.list_of_records if r["billsec"] > 0]

        # Получаем количество таких звонков
        calls_with_duration_count = len(calls_with_duration)
        total_billsec = sum(r["billsec"] for r in self.list_of_records if r["src"] == self.phone or r["dst"] == self.phone)
        average_call_duration = total_billsec / calls_with_duration_count if calls_with_duration_count > 0 else 0

        return {
            "total_calls": total_calls,
            "incoming_calls": incoming_calls,
            "outgoing_calls": outgoing_calls,
            "calls_with_duration_count": calls_with_duration_count,
            "total_billsec": formated_time(total_billsec),
            "average_call_duration": formated_time(average_call_duration),
        }

    def get_group_stat(self):
        total_calls = sum(r.get("total_calls", 0) or 0 for r in self.list_of_records)
        incoming_calls = sum(r.get("incoming_calls", 0) or 0 for r in self.list_of_records)
        outgoing_calls = total_calls
        total_billsec = sum(r.get("total_duration", 0) or 0 for r in self.list_of_records)
        average_call_duration = total_billsec / total_calls if total_calls > 0 else 0
        return {
            "total_calls": total_calls,
            "incoming_calls": incoming_calls,
            "outgoing_calls": outgoing_calls,
            "total_billsec": formated_time(total_billsec),
            "average_call_duration": formated_time(average_call_duration),
        }

