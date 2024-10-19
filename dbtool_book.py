from dbclass_main import Databases
from datetime import datetime
import psycopg2
import ids
# try: except has been abandoned


class ManageBook(Databases):
    def __init__(self):
        super().__init__()

    # for storage
    def store_goods(self, name, goods, date):
        """
        for storing goods; to add to psql
        :param name: the owner of the goods
        :param goods: what he/she stores
        :param date: when he/she stores
        :return: None
        """
        sql = f"insert into public.savings values ('{name}', '{goods}', '{date}');"
        self.cursor.execute(sql)
        self.db.commit()

    def move_out_goods(self, name):
        """
        for moving out the goods; to delete from psql
        :param name: the owner of the goods
        :return: None
        """
        sql = f"delete from public.savings where name = '{name}';"
        self.cursor.execute(sql)
        self.db.commit()

    def get_storage(self, name):
        """
        print the whole list of the goods he/she stored
        :param name: the owner of the goods
        :return: None
        """
        sql = f"select * from public.savings where name = '{name}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    # for books
    def insert_book_data(self, title, series, byname1, byname2, location, category, language):
        """
        Insert the data of the books in DB.
        :param title: title of the book. ch(50), not null.
        :param series: series of the book. double precision, not null.
        :param byname1: another name of the book. ch(10).
        :param byname2: yet another name of the book. ch(10).
        :param location: location of the book. ch(4), not null.
        :param category: category of the book. ch(5), not null.
        :param language: language of the book. ch(3), not null.
        :return: None
        """
        if not self.is_there_same_book(title, series, category, language):
            # in table "book"
            book_id = self.get_new_id(title, series)
            sql = f"insert into public.book values\
                    ('{book_id}', '{title}', {series}, '{byname1}', '{byname2}', '{location}', true);"
            self.cursor.execute(sql)
            self.db.commit()

            # in table "category"
            sql = f"insert into public.category values\
                    ('{book_id}', '{category}', '{language}');"
            self.cursor.execute(sql)
            self.db.commit()

    def get_info_by_id(self, book_id):
        """
        print the data of the id
        :param book_id: id of bookds.
        :return: the list of data
        """
        sql = f"select title, series from public.book\
                where book_id = '{book_id}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

    def read_book_data(self, input_str, num=None):
        """
        Read the data of the books.
        :param input_str: name of books.
        :param num: number of books.
        :return: new_result (location, title, series, rentability of the books)
        """
        if num is None:
            sql = f"select location, title, series, can_rent\
                    from public.book\
                    where title like '%{input_str}%' or byname1 like '%{input_str}%' or byname2 like '%{input_str}%'\
                    order by location, book_id;"
        else:
            if float(num).is_integer():
                num = int(num)
            else:
                num = round(float(num), 1)

            sql = f"select location, title, series, can_rent\
                    from public.book\
                    where (title like '%{input_str}%' or byname1 like '%{input_str}%' or byname2 like '%{input_str}%')\
                        and series = {num}\
                    order by location, book_id;"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        new_result = []
        for book in result:
            db_loc, db_name, db_num, db_rent = book
            if db_num.is_integer():
                new_result.append((db_loc.strip(), db_name.strip(), int(db_num), db_rent))
            else:
                new_result.append(book)

        return new_result

    def find_book_id(self, title, series):
        sql = f"select book_id from public.book\
                where title = '{title}' and series = {series};"

        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]

    def find_book_rentable(self, book_id):
        sql = f"select can_rent from public.book\
                where book_id = '{book_id}';"

        self.cursor.execute(sql)

        """if self.cursor.fetchall()[0][0] == 'true':
            return True
        else:
            return False"""
        return self.cursor.fetchall()[0][0]

    def is_there_same_book(self, title, series, category, language):
        """
        Detect whether the same book is already in the bookshelf.
        :param title: title of the book.
        :param series: series of the book.
        :param category: category of the book.
        :param language: language of the book.
        :return: result (detected data)
        """
        sql = f"select title, series, category, language\
                from public.book, public.category\
                where (title like '%{title}%' or byname1 like '%{title}%' or byname2 like '%{title}%') \
                and series = {series} and category = '{category}' and language = '{language}'\
                order by book.book_id;"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

    def is_there_same_title(self, title, category, language):
        sql = f"select title, series, category, language\
                from public.book, public.category\
                where (title like '%{title}%' or byname1 like '%{title}%' or byname2 like '%{title}%') \
                and category = '{category}' and language = '{language}'\
                order by book.book_id;"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

    def get_new_id(self, title, series):
        sql = "select book_id from public.book order by book_id desc;"
        self.cursor.execute(sql)
        max_id = self.cursor.fetchall()

        sql = f"select book_id from public.book where title = '{title}';"
        self.cursor.execute(sql)
        op = self.cursor.fetchall()

        if op:
            alpha_part = op[0][0][:3]
        else:
            alpha_part = ids.increment_alpha(max_id[0][0][:3])

        """if max_id[0][0][2] == '9':
            alpha_part = ids.increment_alpha(max_id[0][0][:2])"""

        if series < 10:
            num_part = '0' + str(int(series * 10))
        else:
            num_part = str(int(series * 10))

        new_id = alpha_part + num_part

        return new_id

    def update_book_data(self, column, input_str, book_id):
        """
        Change the data of the books.
        :param column: column of the relation of DB.
        :param input_str: info of the book which you want to change.
        :param book_id: the id of the book.
        :return: None
        """
        if column in ['category', 'language']:
            sql = f"update public.category set {column} = '{input_str}' "
        else:
            sql = f"update public.book set {column} = '{input_str}' "
        sql += f"where book_id = '{book_id}'; commit;"

        self.cursor.execute(sql)
        self.db.commit()

    def delete_book_data(self, book_id):
        """
        Delete the book.
        :param book_id: the id of the book.
        :return: None
        """
        sql = f"delete from public.book where book_id = '{book_id}';\
                delete from public.category where book_id = '{book_id}';"
        self.cursor.execute(sql)
        self.db.commit()

    def get_location(self, location):
        """
        Print the location.
        :param location: the location which you want to search.
        :return: new_result (the location of the book)
        """
        if location[-1] == '%':
            # search all
            where = f"location like '{location}'"
        else:
            where = f"location = '{location}'"

        sql = f"select location, title, series, can_rent\
                from public.book\
                where {where} order by location, title, series;"

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        new_result = []
        for book in result:
            area, book_name, num, rent = book
            if num.is_integer():
                new_result.append((area, book_name, int(num), rent))
            else:
                new_result.append(book)

        return new_result

    def rent_book(self, student_name, book_id, is_return=False):
        """
        Rent the book.
        :param student_name: the student's student name who rent the book.
        :param book_id: the id of the book which is rented.
        :param is_return: boolean.
        :return: None
        """
        date = str(datetime.now().date())

        sql = f"select student_num from public.reader where student_name = '{student_name}';"
        self.cursor.execute(sql)
        student_num = self.cursor.fetchall()[0][0]

        if is_return:
            self.update_book_data('can_rent', 'true', book_id)
            sql = f"delete from public.rent where book_id = '{book_id}';"
        else:
            self.update_book_data('can_rent', 'false', book_id)
            sql = f"insert into public.rent values\
                    ('{student_num}', '{book_id}', '{date}');"

        self.cursor.execute(sql)
        self.db.commit()

    def get_rent_list(self, name):
        sql = f"select student_num from public.reader where student_name = '{name}';"
        self.cursor.execute(sql)
        student_num = self.cursor.fetchall()[0][0]

        sql = f"select * from public.rent where student_num = '{student_num}';"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result

book = ManageBook()
print(book.get_rent_list('한재영'))