import mysql.connector
from mysql.connector import errorcode
import pymysql

# server = 'your_server.database.windows.net'
SQL_SERVER = 'passion-mysql-server.mysql.database.azure.com'
SQL_DB = 'passiondb'
USERNAME = 'passionadmin'
PASSWORD = 'MonikMik17!'


try:
#    cnxn = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=SQL_SERVER, port=3306, database=SQL_DB, client_flags=[mysql.connector.ClientFlag.SSL],ssl_ca=SSL_CA, ssl_disabled=True)
   cnxn = pymysql.connect(host=SQL_SERVER,
                            port=3306,
                             user=USERNAME,
                             password=PASSWORD,                             
                             database=SQL_DB
                             )
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    cursor = cnxn.cursor()

    #Création de la table Images
    # cursor.execute("CREATE TABLE images (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50), bloblink VARCHAR(100) );")
    # cursor.execute("CREATE TABLE tags (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50) );")
    # cursor.execute("CREATE TABLE tag_image (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50) );")
    cursor.execute("INSERT INTO images (name,bloblink) VALUES ('manguier.jpeg','www/tmp/blob1');")
    print("Finished inserting row.")

    cursor.execute("SELECT * FROM images;")
    rows = cursor.fetchall()
    for row in rows:
        print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

    # print("Finished creating table.")

    # Cleanup
    cnxn.commit()
    cursor.close()
    cnxn.close()
    print("Done.")

