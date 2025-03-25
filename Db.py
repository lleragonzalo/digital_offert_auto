import psycopg2

def obtener_resultados():
    conn = psycopg2.connect(
        dbname="evaluacion_ofertas",
        user="postgres",
        password="Leon40304030",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM evaluaciones;")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

obtener_resultados()
