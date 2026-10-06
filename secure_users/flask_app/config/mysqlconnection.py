import pymysql.cursors


class MySQLConnection:
    """
    Administra la conexión entre Python y MySQL.
    """

    def __init__(self, db):
        self.db = db

    def query_db(self, query, data=None):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database=self.db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

        with connection.cursor() as cursor:
            try:
                q = query.strip().lower()

                if data is not None:
                    print("Running Query:", cursor.mogrify(query, data))
                else:
                    print("Running Query:", query)

                cursor.execute(query, data)

                if q.startswith("select"):
                    return cursor.fetchall()

                if q.startswith("insert"):
                    return cursor.lastrowid

                return cursor.rowcount

            except Exception as e:
                print("Ups, algo ha salido mal :(", e)
                raise

            finally:
                connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)