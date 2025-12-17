from pymongo import MongoClient

#constructor vacío porque nuestra BBDD es local, si no lo fuera se tendría
#que indicar su url de conexión
db_client = MongoClient("mongodb+srv://anamontero_db_user:7FLGLGcdsKQf4Swk@proyecto1.oqnimro.mongodb.net/?appName=Proyecto1")