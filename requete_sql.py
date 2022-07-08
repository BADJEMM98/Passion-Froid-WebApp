recherche = "SELECT images.bloblink from images INNER JOIN ( SELECT A.id_image FROM tag_image A INNER JOIN \
            ( SELECT id FROM tags WHERE name IN"+ str(list_tags)+") AS B ON A.id_tag = B.id GROUP BY A.id_image \
            HAVING COUNT(*) = "+ str(len(list_tags))+") AS C ON images.id = C.id_image;"