import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client[os.getenv('DATABASE_NAME', 'bcv_api')]
        self.collection = self.db[os.getenv('COLLECTION_NAME', 'tasas')]
    
    def actualizar_tasa(self, valor, fecha=None):
        if fecha is None:
            fecha = datetime.now().strftime('%Y-%m-%d')
        
        documento = {
            '_id': 'tasa_actual',
            'valor': valor,
            'fecha': fecha,
            'ultima_actualizacion': datetime.now().isoformat()
        }
        
        self.collection.replace_one(
            {'_id': 'tasa_actual'},
            documento,
            upsert=True
        )
        return documento
    
    def obtener_tasa(self):
        tasa = self.collection.find_one({'_id': 'tasa_actual'})
        if tasa:
            tasa.pop('_id', None)
        return tasa
    
    def close(self):
        self.client.close()