import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from scripts.db import MongoDB

app = Flask(__name__)

@app.route('/api/tasas', methods=['GET'])
def obtener_todas_tasas():
    try:
        db = MongoDB()
        tasas = db.obtener_tasas()
        db.close()
        
        if tasas:
            response = {
                'exito': True,
                'datos': {
                    'fecha': tasas['fecha'],
                    'ultima_actualizacion': tasas['ultima_actualizacion'],
                    'monedas': tasas['monedas'],
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

@app.route('/api/tasa/<codigo_moneda>', methods=['GET'])
def obtener_tasa_especifica(codigo_moneda):
    try:
        db = MongoDB()
        tasa = db.obtener_tasa_moneda(codigo_moneda)
        db.close()
        
        if tasa:
            response = {
                'exito': True,
                'datos': {
                    **tasa,
                    'fuente': 'Banco Central de Venezuela'
                }
            }
            return jsonify(response), 200
        else:
            return jsonify({
                'exito': False,
                'error': f'No se encontró la moneda {codigo_moneda.upper()}'
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

if __name__ == '__main__':
    app.run(debug=True)