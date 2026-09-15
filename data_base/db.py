import psycopg2

connection = psycopg2.connect(
    host="localhost", database="store", user="store", password="store"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM PRODUCTS")

rows = cursor.fetchall()

for i in rows:
    print(i)

cursor.close()
connection.close()
