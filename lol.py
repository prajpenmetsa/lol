def fetch_user():
    query = "select * from user_info;"
    cursor.execute(query)
    results = cursor.fetchall()
    dic = {}
    for i in results:
        dic[i[1]]=i[2]
    return dic

import psycopg2

db = psycopg2.connect("postgresql://lakshmi:-wsuF7g_tKtqKXTFAm4huw@iss-group-3-4110.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")
cursor = db.cursor()

query = '''CREATE TABLE IF NOT EXISTS user_info (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL
);
'''
cursor.execute(query)
db.commit()

query = '''CREATE TABLE IF NOT EXISTS user_images (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    num_images INT NOT NULL,
    image1 BYTEA,
    image1_name VARCHAR(200),
    image2 BYTEA,
    image2_name VARCHAR(200),
    image3 BYTEA,
    image3_name VARCHAR(200),
    image4 BYTEA,
    image4_name VARCHAR(200),
    image5 BYTEA,
    image5_name VARCHAR(200),
    image6 BYTEA,
    image6_name VARCHAR(200),
    image7 BYTEA,
    image7_name VARCHAR(200),
    image8 BYTEA,
    image8_name VARCHAR(200),
    image9 BYTEA,
    image9_name VARCHAR(200),
    image10 BYTEA,
    image10_name VARCHAR(200),
    image11 BYTEA,
    image11_name VARCHAR(200),
    image12 BYTEA,
    image12_name VARCHAR(200)
);
'''
cursor.execute(query)
db.commit()

query = '''CREATE TABLE IF NOT EXISTS audio (
    audio BYTEA
);
'''
cursor.execute(query)
db.commit()