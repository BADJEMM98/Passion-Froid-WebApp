import mysql.connector
from mysql.connector import errorcode

# server = 'your_server.database.windows.net'
SQL_SERVER = 'passion-mysql-server.mysql.database.azure.com'
SQL_DB = 'passiondb'
USERNAME = 'passionadmin'
PASSWORD = 'MonikMik17!'


try:
  cnxn = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=SQL_SERVER, port=3306, database=SQL_DB)
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
    # cursor.execute("CREATE TABLE tags (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50) UNIQUE);")
    # cursor.execute("CREATE TABLE tag_image (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50) );")
    #cursor.execute("INSERT INTO images (name,bloblink) VALUES ('manguier.jpeg','www/tmp/blob1');")
    #print("Finished inserting row.")
    
    #cursor.execute("SELECT * FROM tags;")
    
    #cursor.execute("ALTER TABLE tags ADD CONSTRAINT unikname UNIQUE (name);")
    rows = cursor.fetchall()
    for row in rows:
      print(row)
       
    # Cleanup
    cnxn.commit()
    cursor.close()
    cnxn.close()
    print("Done.")

