import psycopg

conn = psycopg.connect(
    "postgresql://wjdb_owner:U31LBQlcgPYf@ep-patient-darkness-a1123ymq-pooler.ap-southeast-1.aws.neon.tech/wjdb?sslmode=require",
    sslmode="require",
)
try:
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("complete")
except Exception as e:
    print("error")
    print(str(e))
cur.close()
conn.close()
