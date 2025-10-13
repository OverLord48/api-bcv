import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import logging
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BCVScraper:
    def __init__(self):
        self.url = 'https://www.bcv.org.ve/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.tz = pytz.timezone("America/Caracas")
        
        # Mapeo de los acronimos de monedas disponibles y sus símbolos
        self.simbolos = {
            'USD': '$', 'EUR': '€', 'CNY': '¥',
            'TRY': '₺', 'RUB': '₽', 'GBP': '£', 'JPY': '¥'
        }
    
    def obtener_tasas(self):
        try:
            today_vzla = datetime.now(self.tz).strftime('%Y-%m-%d')
            logger.info(f"Consultando tasas del BCV para: {today_vzla}")
            
            response = requests.get(self.url, headers=self.headers, verify=False, timeout=10)
            
            if response.status_code != 200:
                return {'exito': False, 'error': f'Error HTTP: {response.status_code}'}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Validar fecha
            date_html = soup.find('span', {'class': 'date-display-single'})
            if not date_html:
                return {'exito': False, 'error': 'No se encontró la fecha'}
            
            date_str = date_html.get('content', '')[:10]
            
            if date_str != today_vzla:
                logger.warning(f"Tasa desactualizada. BCV: {date_str}, Hoy: {today_vzla}")
                return {'exito': False, 'error': f'Tasa desactualizada: {date_str}'}
            
            monedas = {}
            
            # Buscar divs con IDs comunes de monedas
            divs_monedas = soup.find_all('div', id=re.compile(r'^(dolar|euro|yuan|lira|rublo)', re.IGNORECASE))
            
            for div in divs_monedas:
                div_id = div.get('id', '')
                
                # Extraer valor
                valor_tag = div.find('strong')
                if not valor_tag:
                    continue
                
                try:
                    valor_str = valor_tag.text.strip().replace('.', '').replace(',', '.')
                    valor = float(valor_str)
                except ValueError:
                    logger.warning(f"No se pudo convertir valor en {div_id}")
                    continue
                
                # Determinar código de moneda basado en el ID
                codigo = self._obtener_codigo_desde_id(div_id)
                simbolo = self.simbolos.get(codigo, '')
                nombre = self._obtener_nombre_desde_id(div_id)
                
                monedas[codigo] = {
                    'nombre': nombre,
                    'simbolo': simbolo,
                    'valor': valor
                }
                logger.info(f"✓ {nombre} ({codigo}): {valor}")
            
            if len(monedas) == 0:
                return {'exito': False, 'error': 'No se encontraron tasas'}
            
            logger.info(f"Total de monedas: {len(monedas)}")
            
            return {
                'fecha': date_str,
                'monedas': monedas,
                'exito': True
            }
        
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {'exito': False, 'error': str(e)}
    
    def _obtener_codigo_desde_id(self, div_id):
        """Convierte el ID del div al código ISO de la moneda"""
        mapeo = {
            'dolar': 'USD',
            'euro': 'EUR',
            'yuan': 'CNY',
            'lira': 'TRY',
            'rublo': 'RUB'
        }
        div_id_lower = div_id.lower()
        return mapeo.get(div_id_lower, div_id.upper()[:3])
    
    def _obtener_nombre_desde_id(self, div_id):
        """Convierte el ID del div a un nombre legible"""
        mapeo = {
            'dolar': 'Dólar estadounidense',
            'euro': 'Euro',
            'yuan': 'Yuan chino',
            'lira': 'Lira turca',
            'rublo': 'Rublo ruso'
        }
        div_id_lower = div_id.lower()
        return mapeo.get(div_id_lower, div_id.capitalize())