import sys
import os.path
import csv
import sqlalchemy as db

def main():
    if len(sys.argv) != 2:
        print("Command should be in the form: `python3 build_csv.py DATABASE_FILENAME`")
        exit()
    db_filename = sys.argv[1]

    if not os.path.isfile(db_filename):
        print("Could not find database file ", db_filename, ".")
        exit()

    engine = db.create_engine("sqlite:///" + db_filename)
    conn = engine.connect()
    tables = conn.execute("SELECT name \
                         FROM sqlite_master \
                         WHERE type='table'")

    for table_name in tables:
        csv_file = open("data/" + table_name[0] + ".csv", "w")
        csv_fout = csv.writer(csv_file)

        header = [column[1] for column in conn.execute("PRAGMA table_info({})".format(table_name[0])).fetchall()]
        rows = conn.execute("SELECT * FROM {}".format(table_name[0])).fetchall()

        csv_fout.writerow(header)
        csv_fout.writerows(rows)
        csv_file.close()

    conn.close()

if __name__ == '__main__':
    main()
