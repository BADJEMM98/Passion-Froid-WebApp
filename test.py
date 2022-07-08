import mysql.connector
from mysql.connector import errorcode

SQL_SERVER = 'passion-mysql-server.mysql.database.azure.com'
SQL_DB = 'passiondb'
USERNAME = 'passionadmin'
PASSWORD = 'MonikMik17!'
list_tags = ('arbre','mangue')

recherche = "SELECT images.bloblink from images INNER JOIN ( SELECT A.id_image FROM tag_image A INNER JOIN \
            ( SELECT id FROM tags WHERE name IN"+ str(list_tags)+") AS B ON A.id_tag = B.id GROUP BY A.id_image \
            HAVING COUNT(*) = "+ str(len(list_tags))+") AS C ON images.id = C.id_image;"
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
    # cursor.execute("CREATE TABLE tags (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(50) );")
    # cursor.execute("CREATE TABLE tag_image (id_image INT NOT NULL, id_tag INT NOT NULL, PRIMARY KEY(id_image, id_tag));")
    # cursor.execute("ALTER TABLE tag_image ADD CONSTRAINT FOREIGN KEY (id_image) REFERENCES images(id);")
    # cursor.execute("ALTER TABLE tag_image ADD CONSTRAINT FOREIGN KEY (id_tag) REFERENCES tags(id);")
    # cursor.execute("INSERT INTO images (name,bloblink) VALUES ('banane.jpeg','www/tmp/blob1');")
    # cursor.execute("INSERT INTO images (name,bloblink) VALUES ('ananas.jpeg','www/tmp/blob1');")
    # cursor.execute("INSERT IGNORE INTO tags (name) VALUES ('arbre');")
    # cursor.execute("INSERT INTO tag_image (id_image,id_tag) VALUES (1,5);")
    # cursor.execute("INSERT INTO tag_image (id_image,id_tag) VALUES (1,3);")
    # cursor.execute("INSERT INTO tag_image (id_image,id_tag) VALUES (3,2);")
    # cursor.execute("INSERT INTO tag_image (id_image,id_tag) VALUES (4,5);")
    # cursor.execute("INSERT INTO tag_image (id_image,id_tag) VALUES (5,4);")
    

    # print("Finished inserting row.")
    # cursor.execute("SELECT LAST_INSERT_ID();")
    # rows = cursor.fetchall()
    # print(rows)
    # cursor.execute("")
    # cursor.execute("SELECT * FROM tags;")
    # cursor.execute("SELECT DISTINCT id_image, id_tag FROM tag_image WHERE id_tag=5")

    cursor.execute(recherche)
    rows = cursor.fetchall()
    for row in rows:
        print("Data row = (%s, %s)" %(str(row[0]), str(row[1]))) #, str(row[2])))

    # print("Finished creating table.")

    # Cleanup
    cnxn.commit()
    cursor.close()
    cnxn.close()
    print("Done.")

