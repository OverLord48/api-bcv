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
    
    def actualizar_tasas(self, monedas, fecha=None):
        if fecha is None:
            fecha = datetime.now().strftime('%Y-%m-%d')
        
        documento = {
            '_id': fecha,  # Se usa la fecha como ID único
            'fecha': fecha,
            'ultima_actualizacion': datetime.now().isoformat(),
            'monedas': monedas
        }
        
        # Reemplazar si existe, insertar si no
        self.collection.replace_one(
            {'_id': fecha},
            documento,
            upsert=True
        )
        return documento
    
    def obtener_tasas(self, fecha=None):
        if fecha:
            tasas = self.collection.find_one({'_id': fecha})
        else:
            tasas = self.collection.find_one(sort=[('fecha', -1)])
        
        if tasas:
            tasas.pop('_id', None)
        return tasas
    
    def obtener_tasa_moneda(self, codigo_moneda, fecha=None):
        tasas = self.obtener_tasas(fecha)
        if tasas and 'monedas' in tasas:
            moneda = tasas['monedas'].get(codigo_moneda.upper())
            if moneda:
                return {
                    'fecha': tasas['fecha'],
                    'ultima_actualizacion': tasas['ultima_actualizacion'],
                    'moneda': {
                        'codigo': codigo_moneda.upper(),
                        **moneda
                    }
                }
        return None
    
    def obtener_historico(self, limite=30):
        cursor = self.collection.find().sort('fecha', -1).limit(limite)
        historico = []
        for doc in cursor:
            doc.pop('_id', None)
            historico.append(doc)
        return historico
    
    def close(self):
        self.client.close()