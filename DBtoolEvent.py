from DBclass import Databases
import random


class ManageEvents(Databases):
    def __init__(self):
        super().__init__()

    # for midterm ============================================================
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

        participants, weights = [list(col) for col in zip(*result)]

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

    # for halloween (w/ @kagerou_kawaii__) ==================================
    def get_max(self, name, length):
        sql = f"select length from events.halloween2024 where student_name = '{name}';"
        self.cursor.execute(sql)
        maximum = self.cursor.fetchall()

        if not maximum:
            sql = f"insert into events.halloween2024 values ('{name}', {length}, 0);"
            self.cursor.execute(sql)
            self.db.commit()
            return length
        else:
            maximum = max(length, maximum[0][0])
            sql = f"update events.halloween2024 set length = {maximum} where student_name = '{name}';"
            self.cursor.execute(sql)
            self.db.commit()
            return maximum

    def size_up_pumpkins(self, name):
        sql = f"select jackolantern, row_number\
                from(select *, row_number() over (order by length desc)\
                as row_number from events.halloween2024) subquery\
                where student_name = '{name}';"
        self.cursor.execute(sql)
        temp = self.cursor.fetchall()

        if not temp:
            jack, rank = 0, 65537
        elif temp[0][1] < 6:
            jack, rank = temp[0]
        else:
            jack, rank = temp[0][0], 65537

        worm = 0.37 ** (rank-1)

        return [0.88 ** jack, 0.92 ** jack, 1.3 ** jack, worm]

    def get_items(self, name):
        sql = f"select clover, rotten from events.halloween2024\
                where student_name = '{name}';"
        self.cursor.execute(sql)

        if sql is None:
            return [0, 0]
        else:
            return self.cursor.fetchall()[0]

    def initialize_pumpkin(self):
        sql = f"delete from events.halloween2024 where length > 0;"
        self.cursor.execute(sql)
        self.db.commit()

    def get_rank(self):
        sql = f"select student_name, length from events.halloween2024 where student_name != '21/한재영'\
                order by length desc;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[:3]

    def get_all(self):
        sql = f"select student_name, length, jackolantern from events.halloween2024 order by length desc;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_my_rank(self, name):
        sql = (f"select row_number\
                from(select *, row_number() over (order by length desc)\
                as row_number from events.halloween2024 where student_name != '21/한재영') subquery\
                where student_name = '{name}';")
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def got_jack(self, name):
        sql = f"select jackolantern from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        num = self.cursor.fetchall()[0][0]

        sql = f"update events.halloween2024 set jackolantern = {num + 1} where student_name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def got_worm(self, name):
        sql = f"select length from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        length = self.cursor.fetchall()[0][0]
        ran = (round(random.uniform(0.01, 1.00), 2))

        sql = f"update events.halloween2024 set length = {length - ran} where student_name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def got_clover(self, name):
        sql = f"select clover from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        clover = self.cursor.fetchall()[0][0]

        sql = f"update events.halloween2024 set clover = {clover + 1} where student_name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def got_rotten(self, name):
        sql = f"select rotten from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        rotten = self.cursor.fetchall()[0][0]

        sql = f"update events.halloween2024 set rotten = {rotten + 1} where student_name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def get_lantern(self, name):
        sql = f"select jackolantern from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def get_xp(self, name, add):
        sql = f"select xp from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        xp = self.cursor.fetchall()[0][0]

        sql = f"update events.halloween2024 set xp = {xp + add} where student_name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def whatsyourxp(self, name):
        sql = f"select xp from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def minusyourxp(self, name, minus):
        sql = f"select xp from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        xp = self.cursor.fetchall()[0][0]

        sql = f"update events.halloween2024 set xp = {xp - minus} where student_name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def one_up(self, name):
        sql = f"select one_up from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        up = self.cursor.fetchall()[0][0]

        sql = f"update events.halloween2024 set one_up = {up + 1} where student_name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def get_one_up(self, name):
        sql = f"select one_up from events.halloween2024 where student_name = '{name}'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def get_all_mem(self):
        sql = f"select student_name from events.halloween2024;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()


event = ManageEvents()
