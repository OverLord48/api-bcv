import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BCVScraper:
    def __init__(self):
        self.url = 'https://www.bcv.org.ve/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.tz = pytz.timezone("America/Caracas")
    
    def obtener_tasa(self):
        """
        Hace scraping del sitio del BCV para obtener la tasa del dólar.
        Verifica que la fecha sea la actual antes de retornar el valor.
        """
        try:
            # Fecha actual en Venezuela
            today_vzla = datetime.now(self.tz).strftime('%Y-%m-%d')
            
            logger.info(f"Consultando tasa del BCV para hoy: {today_vzla}")
            
            # Hacer request al BCV (sin verificar SSL como en el código original)
            response = requests.get(
                self.url, 
                headers=self.headers, 
                verify=False,  # El BCV a veces tiene problemas con SSL
                timeout=10
            )
            
            if response.status_code != 200:
                return {
                    'exito': False,
                    'error': f'Error HTTP: {response.status_code}'
                }
            
            # Parsear HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Obtener la fecha de la tasa publicada
            date_html = soup.find('span', {'class': 'date-display-single'})
            if not date_html:
                return {
                    'exito': False,
                    'error': 'No se encontró la fecha en el sitio del BCV'
                }
            
            # Extraer fecha (formato: YYYY-MM-DD en el atributo content)
            date_str = date_html.get('content', '')[:10]
            
            # Verificar que la tasa sea del día actual
            if date_str != today_vzla:
                logger.warning(f"La tasa no está actualizada. Fecha BCV: {date_str}, Hoy: {today_vzla}")
                return {
                    'exito': False,
                    'error': f'La tasa no está actualizada. Última actualización: {date_str}'
                }
            
            # Obtener el valor del dólar
            dolar_div = soup.find('div', {'id': 'dolar'})
            if not dolar_div:
                return {
                    'exito': False,
                    'error': 'No se encontró el div con id "dolar"'
                }
            
            valor_tag = dolar_div.find('strong')
            if not valor_tag:
                return {
                    'exito': False,
                    'error': 'No se encontró el valor de la tasa'
                }
            
            # Limpiar y convertir el valor
            # Formato BCV: "36.234,56" -> convertir a float
            valor_str = valor_tag.text.strip().replace('.', '').replace(',', '.')
            
            try:
                dolar_float = float(valor_str)
            except ValueError:
                return {
                    'exito': False,
                    'error': f'No se pudo convertir el valor: {valor_str}'
                }
            
            logger.info(f"✓ Tasa del BCV obtenida: {dolar_float} para fecha {date_str}")
            
            return {
                'valor': dolar_float,
                'fecha': date_str,
                'exito': True
            }
        
        except requests.RequestException as e:
            logger.error(f"Error en la petición: {str(e)}")
            return {
                'exito': False,
                'error': f'Error en la petición: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return {
                'exito': False,
                'error': f'Error inesperado: {str(e)}'
            }