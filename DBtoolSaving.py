from DBclass import Databases

# try: except has been abandoned


class ManageSaving(Databases):
    def __init__(self):
        super().__init__()

    def store_goods(self, name, goods, date):
        """
        for storing goods; to add to psql
        :param name: the owner of the goods
        :param goods: what he/she stores
        :param date: when he/she stores
        :return: None
        """
        sql = f"insert into savings.savings values ('{name}', '{goods}', '{date}');"
        self.cursor.execute(sql)
        self.db.commit()

    def move_out_goods(self, name):
        """
        for moving out the goods; to delete from psql
        :param name: the owner of the goods
        :return: None
        """
        sql = f"delete from savings.savings where name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def get_storage(self, name):
        """
        print the whole list of the goods he/she stored
        :param name: the owner of the goods
        :return: None
        """
        sql = f"select * from savings.savings where name = '{name}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


saving = ManageSaving()
