python -m venv venv         # crear entorno virtual
<br>
.\venv\Scripts\activate     # activar entorno virtual en Windows
<br>
<br>
activar api
<br>
uvicorn main:app --host 0.0.0.0 --port 8000 
<br>


Instalar dependencias <br>
pip install fastapi uvicorn pydantic cx_Oracle python-dotenv <br>
pip freeze > requirements.txt   # guarda las dependencias en requirements.txt
