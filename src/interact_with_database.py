import pymysql
import json


def extract_config(data):
    # Extracts the config for the given JSON file
    host = data["host"]
    user = data["user"]
    password = data["password"]
    db = data["db"]

    return host, user, password, db


def connect_to_db(JSON_FILE="database_config.json"):
    # Conn
    f = open(JSON_FILE)
    data = json.load(f)

    host, user, password, db = extract_config(data)
    conn = pymysql.connect(host=host, user=user, passwd=password, db=db)
    return conn


def write_to_db(conn, entry):
    cur = conn.cursor()
    sql = """insert into `Projects` (ProjectID, Title, URL, 
                                  NumberOfStars, NumberOfForks, NumberOfWatches,
                                  NumberOfContributors, NumberOfReleases, NumberOfUsers,
                                  NumberOfCommits, MyTimeStamp)
         values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cur.execute(sql, entry)
    conn.commit()


def return_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Projects")
    return cur.fetchall()


# conn = connect_to_db()
# entry = (810315203877, "go-ethereum", "https:// github.com/ethereum/go-ethereum",
#          40600, 15600, 15600, 862, 165, 9400, 13848, 1672226002)
# write_to_db(conn, entry)
