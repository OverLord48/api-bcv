# API Tasa BCV

API REST para consultar las tasas de cambio del Banco Central de Venezuela (BCV).

## 🚀 Características

- 📊 Obtiene todas las tasas oficiales del BCV (USD, EUR, CNY, TRY, RUB)
- 🔄 Actualización automática diaria vía GitHub Actions
- ⚡ API rápida alojada en Vercel
- 💾 Datos almacenados en MongoDB Atlas
- 🆓 100% gratis

## 📡 Endpoints

### GET `/api/tasas`
Obtiene todas las tasas de cambio

**Respuesta exitosa (200):**
```json
{
  "exito": true,
  "datos": {
    "fecha": "2025-10-13",
    "ultima_actualizacion": "2025-10-13T08:00:00Z",
    "monedas": {
      "USD": {
        "nombre": "Dólar estadounidense",
        "simbolo": "$",
        "valor": 36.50
      },
      "EUR": {
        "nombre": "Euro",
        "simbolo": "€",
        "valor": 39.87
      },
      "CNY": {
        "nombre": "Yuan chino",
        "simbolo": "¥",
        "valor": 5.12
      }
    },
    "fuente": "Banco Central de Venezuela"
  }
}
```

### GET `/api/tasa/<codigo_moneda>`
Obtiene la tasa de una moneda específica

**Ejemplos:**
- `/api/tasa/USD` - Dólar estadounidense
- `/api/tasa/EUR` - Euro
- `/api/tasa/CNY` - Yuan chino

**Respuesta exitosa (200):**
```json
{
  "exito": true,
  "datos": {
    "fecha": "2025-10-13",
    "ultima_actualizacion": "2025-10-13T08:00:00Z",
    "moneda": {
      "codigo": "USD",
      "nombre": "Dólar estadounidense",
      "simbolo": "$",
      "valor": 36.50
    },
    "fuente": "Banco Central de Venezuela"
  }
}
```

### GET `/api/health`
Verifica el estado de la API

## 💱 Monedas Disponibles

| Código | Moneda | Símbolo |
|--------|--------|---------|
| USD | Dólar estadounidense | $ |
| EUR | Euro | € |
| CNY | Yuan chino | ¥ |
| TRY | Lira turca | ₺ |
| RUB | Rublo ruso | ₽ |

### GET `/api/health`
Verifica el estado de la API

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/OverLord48/api-bcv.git
cd bcv-api
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crea un archivo `.env`:
```
MONGODB_URI=tu_connection_string_de_mongodb
DATABASE_NAME=bcv_api
COLLECTION_NAME=tasas
```
### 4. Direccion web de consulta

```bash
https://api-bcv-sigma.vercel.app/
```

## 🧪 Desarrollo Local

```bash
python api/tasa.py
```

La API estará disponible en `http://localhost:5000`

## ⚠️ Importante

- Ajusta los selectores CSS en `scripts/scraper.py` según la estructura actual del sitio del BCV
- Respeta los términos de uso del sitio del BCV
- El scraping se hace una vez al día para no sobrecargar el servidor

## 📝 Licencia

MIT

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor abre un issue primero para discutir los cambios.