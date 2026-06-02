import base64
import json
import logging
import httpx
from fastapi import APIRouter, HTTPException, File, UploadFile

from ..core.config import settings
from ..schemas.measure import FootMeasurementRequest, FootMeasurementResponse

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

async def analyze_image_with_gemini(image_base64: str, mime_type: str) -> dict:
    """
    Llama a la API REST de Google Gemini (1.5 Flash) para analizar la imagen del pie
    y estimar la talla de calzado.
    """
    if not settings.gemini_api_key or settings.gemini_api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY no configurado en el archivo .env")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.gemini_api_key}"
    
    prompt = (
        "Analiza esta imagen de un pie y estima la talla de calzado estándar (EU/EUR) más probable. "
        "Devuelve únicamente un objeto JSON con los siguientes campos:\n"
        "- 'shoe_size': la talla estimada en formato string (ej: '42')\n"
        "- 'confidence': un float entre 0.0 y 1.0 que indique tu seguridad en la estimación (debe ser menor si el pie no se ve claro)\n"
        "- 'brand_advice': una recomendación en español para comprar tallas según marcas populares (Nike, Adidas, Converse).\n"
        "Asegúrate de que la respuesta sea estrictamente un JSON válido, sin bloques de código ```json ni texto adicional."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": image_base64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        
        # Extraer el texto de la respuesta
        text_response = data["candidates"][0]["content"]["parts"][0]["text"]
        result = json.loads(text_response.strip())
        return result


def get_mock_prediction(seed_string: str, is_demo_notice: bool = False) -> FootMeasurementResponse:
    """Genera una predicción simulada consistente basada en un string semilla."""
    sizes = ["38", "39", "40", "41", "42", "43", "44"]
    shoe_size = sizes[len(seed_string) % len(sizes)]
    
    advices = {
        "38": "Talla 38 estimada. Horma estándar. En Nike sugerimos tu talla usual; en Converse, media talla menos.",
        "39": "Talla 39 estimada. Horma estándar. En Adidas te recomendamos media talla más de lo habitual.",
        "40": "Talla 40 estimada. Horma ligeramente ancha. Se recomienda comprar tu talla exacta en marcas europeas.",
        "41": "Talla 41 estimada. Horma estándar. Nike y Puma se ajustan perfectamente a tu medida habitual.",
        "42": "Talla 42 estimada. Horma estándar. Recomendamos Adidas Ultraboost en tu talla normal o media talla más.",
        "43": "Talla 43 estimada. Horma ligeramente estrecha. En calzado deportivo, prefiere una talla extra para mayor comodidad.",
        "44": "Talla 44 estimada. Horma ancha. Excelente soporte. Nike Air Force 1 se ajustará idealmente en tu talla usual."
    }
    
    brand_advice = advices.get(shoe_size, "Horma estándar. Se recomienda comprar tu talla de calzado habitual.")
    if is_demo_notice:
        brand_advice = f"⚠️ [Modo Demo] GEMINI_API_KEY no configurado en backend/.env. Por favor, añada su clave de Google Gemini para usar la predicción real por visión de IA. {brand_advice}"
        
    confidence = 0.85 + (len(seed_string) % 11) / 100.0
    return FootMeasurementResponse(
        shoe_size=shoe_size,
        brand_advice=brand_advice,
        confidence=round(confidence, 2),
    )


@router.post("/predict", response_model=FootMeasurementResponse)
async def predict_size(request: FootMeasurementRequest):
    # Intentar análisis real con Gemini si la API key está configurada
    if settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here":
        try:
            # Descargar la imagen
            async with httpx.AsyncClient() as client:
                img_response = await client.get(str(request.image_url), timeout=15.0)
                img_response.raise_for_status()
                img_bytes = img_response.content
                mime_type = img_response.headers.get("content-type", "image/jpeg")
            
            image_base64 = base64.b64encode(img_bytes).decode("utf-8")
            result = await analyze_image_with_gemini(image_base64, mime_type)
            
            return FootMeasurementResponse(
                shoe_size=str(result.get("shoe_size", "N/A")),
                brand_advice=str(result.get("brand_advice", "")),
                confidence=float(result.get("confidence", 0.85)),
            )
        except Exception as exc:
            logger.error(f"Error analizando imagen por URL con Gemini: {exc}")
            # Si falla, hacer fallback a la simulación pero reportando el log
            return get_mock_prediction(str(request.image_url), is_demo_notice=True)
    else:
        # Fallback a simulación directa en modo demo
        return get_mock_prediction(str(request.image_url), is_demo_notice=True)


@router.post("/upload", response_model=FootMeasurementResponse)
async def upload_image(file: UploadFile = File(...)):
    file_content = await file.read()
    
    # Intentar análisis real con Gemini si la API key está configurada
    if settings.gemini_api_key and settings.gemini_api_key != "your_gemini_api_key_here":
        try:
            image_base64 = base64.b64encode(file_content).decode("utf-8")
            mime_type = file.content_type or "image/jpeg"
            result = await analyze_image_with_gemini(image_base64, mime_type)
            
            return FootMeasurementResponse(
                shoe_size=str(result.get("shoe_size", "N/A")),
                brand_advice=str(result.get("brand_advice", "")),
                confidence=float(result.get("confidence", 0.85)),
            )
        except Exception as exc:
            logger.error(f"Error analizando archivo subido con Gemini: {exc}")
            return get_mock_prediction(file.filename, is_demo_notice=True)
    else:
        # Fallback a simulación directa en modo demo
        return get_mock_prediction(file.filename, is_demo_notice=True)
