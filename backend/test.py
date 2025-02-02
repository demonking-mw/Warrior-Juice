import psycopg

conn = psycopg.connect(
    "postgresql://wjdb_owner:U31LBQlcgPYf@ep-patient-darkness-a1123ymq-pooler.ap-southeast-1.aws.neon.tech/wjdb?sslmode=require",
    sslmode="require",
)
cur = conn.cursor()
cur.execute("SELECT 1")
print(cur.fetchone())
cur.close()
conn.close()
