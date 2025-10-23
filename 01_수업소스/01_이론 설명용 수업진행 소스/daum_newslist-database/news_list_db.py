
def insert_news_list(cursor, title:str, link:str):
    sql = "INSERT INTO news_list (title, link) VALUES (%s, %s)"
    rows = cursor.execute(sql, (title, link))
    return rows
