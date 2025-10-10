import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from scripts.db import MongoDB

app = Flask(__name__)

@app.route('/api/tasa', methods=['GET'])
def obtener_tasa():
    try:
        db = MongoDB()
        tasa = db.obtener_tasa()
        db.close()
        
        if tasa:
            response = {
                'exito': True,
                'datos': {
                    'valor': tasa['valor'],
                    'fecha': tasa['fecha'],
                    'ultima_actualizacion': tasa['ultima_actualizacion'],
                    'fuente': 'Banco Central de Venezuela'
                }
            }
            return jsonify(response), 200
        else:
            return jsonify({
                'exito': False,
                'error': 'No hay datos disponibles'
            }), 404
    
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': f'Error del servidor: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'servicio': 'API Tasa BCV'
    }), 200

# Para desarrollo local
if __name__ == '__main__':
    app.run(debug=True)