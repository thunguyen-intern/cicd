from bs4 import BeautifulSoup
import re
import psycopg2
import env_db_vars


db_host = env_db_vars.DB_HOST
db_name = env_db_vars.DB_NAME
db_user = env_db_vars.DB_USER
db_password = env_db_vars.DB_PASSWORD
db_table = env_db_vars.DB_TABLE

try:
    connection = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    cursor = connection.cursor()
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

pattern = re.compile(r"user/human/*")
with open('index.html', 'r') as file:
    html_content = file.read()
count = 0
soup = BeautifulSoup(html_content, 'html.parser')
span_user = soup.find_all('span', attrs={'role': 'presentation', 'data-member-id': pattern})
if span_user:
    insert_query = f"INSERT INTO {db_table} (email, uid) VALUES (%s, %s)"
    for span_element in span_user:
        hovercard_id = span_element.get('data-hovercard-id')
        member_id = span_element.get('data-member-id')
        # cursor.execute(insert_query, (hovercard_id, member_id[11:]))
        # connection.commit()
        count += 1
else:
    print("No divs with span='presentation' found.")
    
print(count)