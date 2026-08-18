from fastapi import HTTPException, status
from groq import Groq, GroqError

from app.config import settings

_client = Groq(api_key=settings.groq_api_key)

_LANGUAGE_LABEL = {
    "tr": "Türkçe",
    "en": "English",
}


def summarize_text(text: str, language: str = "tr") -> str:
    label = _LANGUAGE_LABEL.get(language, "Türkçe")
    prompt = (
        f"Aşağıdaki metni kısa ve anlaşılır bir özet olarak {label} dilinde döndür. "
        f"Sadece özeti yaz, başka açıklama ekleme:\n\n{text}"
    )

    try:
        completion = _client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=512,
        )
    except GroqError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI servisine ulaşılamadı, lütfen daha sonra tekrar deneyin.",
        )

    summary = completion.choices[0].message.content
    if not summary or not summary.strip():
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI servisinden geçerli bir yanıt alınamadı.",
        )

    return summary.strip()
