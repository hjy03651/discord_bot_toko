from dbclass_events import DatabasesEvents
import random
# from dbclass_main import Databases


class ManageEvents(DatabasesEvents):
    def __init__(self):
        super().__init__()

    def new_participation(self, event_name, student_name, weights=1):
        sql = f"insert into events.{event_name} values ('{student_name}', {weights});"
        self.cursor.execute(sql)
        self.db.commit()

    def increase_weights(self, event_name, student_name, weights=1):
        sql = f"select weights from events.{event_name} where student_name = '{student_name}';"
        self.cursor.execute(sql)
        weight = self.cursor.fetchall()[0][0]

        sql = f"update events.{event_name} set weights = {weight + weights}\
                where student_name = '{student_name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def get_random(self, event_name, number):
        sql = f"select * from events.{event_name};"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        participants, weights = map(list, zip(*result))

        win = []
        while len(win) < number:
            new_winner = random.choices(participants, weights)[0]
            if new_winner not in win:
                win.append(new_winner)

        return win

    def delete_all(self, event_name):
        sql = f"delete from events.{event_name} where weights > 0;"
        self.cursor.execute(sql)
        self.db.commit()
