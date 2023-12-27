import sqlite3


class Data:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER,
                    name TEXT,
                    math_task INTEGER,
                    device_flash INTEGER,
                    device_exam INTEGER,
                    teor_flash TNTEGER,
                    teor_exam INTEGER,
                    form_flash INTEGER,
                    form_exam INTEGER,
                    task1 INTEGER,
                    task2 INTEGER,
                    task3 INTEGER,
                    task4 INTEGER,
                    task5 INTEGER,
                    task6 INTEGER,
                    task7 INTEGER,
                    task8 INTEGER,
                    task9 INTEGER
                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id_task INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    answer TEXT
                )''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS flashcard (
                    id_flashcard INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    answer TEXT,
                    id_member INTEGER
                )''')

    def add_user(self, user_id: int, username: str):
        results = self.cursor.execute(f"SELECT * FROM users WHERE id={user_id}").fetchall()
        if not results:
            self.cursor.execute(f"INSERT INTO users (id, name, math_task, device_flash, device_exam, "
                                f"teor_flash, teor_exam, form_flash, form_exam, task1, task2, task3, "
                                f"task4, task5, task6, task7, "
                                f"task8, task9) VALUES ({int(user_id)}, '{username}', "
                                f"0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
            self.conn.commit()

    def get_stats(self, user_id: int):
        results = self.cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
        results = results.fetchall()
        return results

    def add_stats(self, user_id: int, lesson: str):
        query = f"UPDATE users SET `{lesson}` = `{lesson}` + 1 WHERE id = ?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def get_users_proc(self, user_id: int):
        result = self.cursor.execute(f"SELECT * FROM users").fetchall()
        res_user = self.cursor.execute(f"SELECT * FROM users WHERE id={user_id}").fetchall()
        count = 0
        count_users = len(result)-1
        s_user = res_user[0][2] + res_user[0][3] + res_user[0][4] + \
                 res_user[0][5] + res_user[0][6] + res_user[0][7] + res_user[0][8]
        for i in range(len(result)):
            if result[i] != res_user[0]:
                s = 0
                s += result[i][2] + result[i][3] + result[i][4] + result[i][5] + \
                     result[i][6] + result[i][7] + result[i][8]
                if s_user > s:
                    count += 1
        if count_users == 0:
            return 100
        else:
            res = count / count_users
            r = round(res, 2) * 100
            return int(r)