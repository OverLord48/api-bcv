# API Tasa BCV

API REST para consultar la tasa de cambio del Banco Central de Venezuela (BCV).

## 🚀 Características

- 📊 Obtiene la tasa oficial del BCV
- 🔄 Actualización automática diaria vía GitHub Actions
- ⚡ API rápida alojada en Vercel
- 💾 Datos almacenados en MongoDB Atlas
- 🆓 100% gratis

## 📡 Endpoints

### GET `/api/tasa`
Obtiene la tasa actual del dólar

**Respuesta exitosa (200):**
```json
{
  "exito": true,
  "datos": {
    "valor": 36.50,
    "fecha": "2025-10-09",
    "ultima_actualizacion": "2025-10-09T12:00:00Z",
    "fuente": "Banco Central de Venezuela"
  }
}
```

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

### 4. Configurar MongoDB Atlas
1. Crea una cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crea un cluster gratuito
3. Obtén tu connection string
4. Agrega tu IP a la whitelist

### 5. Desplegar en Vercel
1. Importa el repositorio en [Vercel](https://vercel.com)
2. Agrega las variables de entorno en la configuración
3. Despliega

### 6. Configurar GitHub Actions
1. Ve a Settings > Secrets and variables > Actions
2. Agrega el secret: `MONGODB_URI`

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