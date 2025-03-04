import cx_Oracle

# conexión a la base de datos
def get_db_connection():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name="FREEPDB1")  
    conn = cx_Oracle.connect(user="oracle_db", password="admin_202110509", dsn=dsn)
    #print("Conexión exitosa")
    return conn

