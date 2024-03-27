import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])

with conn.cursor() as cur:
    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)

# export DATABASE_URL="postgresql://lakshmi:-wsuF7g_tKtqKXTFAm4huw@iss-group-3-4110.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"
# have to run everytime you open a new terminal