python -m venv venv         # crear entorno virtual
<br>
.\venv\Scripts\activate     # activar entorno virtual en Windows
<br>
<br>
activar api
<br>
uvicorn main:app --host 0.0.0.0 --port 8000 
<br>
uvicorn main:app --reload
<br>


Instalar dependencias 
<br>
pip install fastapi uvicorn pydantic cx_Oracle python-dotenv 
<br>
pip freeze > requirements.txt   # guarda las dependencias en requirements.txt


<br>
<br>
ERROR DE LIBRERÍAS DE ORACLE SOLUCIÓN:
<br>
export LD_LIBRARY_PATH=/home/mario/oracle/instantclient



<br>
borar todas las tablas
<br>
BEGIN
    FOR t IN (SELECT table_name FROM user_tables) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;

<br>
borrar una sola:
<br>
DROP TABLE clientes CASCADE CONSTRAINTS;
