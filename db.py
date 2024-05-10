import sqlite3 

conn = sqlite3.connect("index.db")
cursor = conn.cursor()


def main():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS add_kursDB(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(70) NOT NULL,
            price INT,
            info TEXT,
            master VARCHAR(15)
        );            
        """)
    conn.commit()
    
def add_dataDB(*args):
    sql = """INSERT INTO add_kursDB (name, price, info, master) VALUES (?, ?, ?, ?)"""
    print(args)
    conn.execute(sql, args)
    conn.commit()


def data_infoDB():
    data = conn.execute("SELECT * FROM add_kursDB").fetchall()
    resp = []
    print(data)
    for i in data:
        resp.append(i[1])
    return resp

def dataFull_infoDB():
    data = conn.execute("SELECT * FROM add_kursDB").fetchall()
    return data

if __name__ == "__main__":
    main()
    
# print(data_infoDB())
# print(conn.execute("SELECT * FROM add_kursDB").fetchall())
