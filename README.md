# Summarize-AI

Kullanıcıların yazdığı metni Groq LLM ile özetleyen web uygulaması. Admin onayı gerektiren kayıt akışı, JWT tabanlı kimlik doğrulama ve admin panelinde log/kullanıcı yönetimi içerir.

## Mimari

- **Backend:** Python + FastAPI (REST API)
- **Frontend:** Vue 3 + Vite + Tailwind CSS
- **Veritabanı:** PostgreSQL (SQLAlchemy ORM)
- **AI Sağlayıcı:** Groq API
- **Auth:** JWT (Bearer token)

## Kurulum

### Ön koşullar

- Python 3.11+
- Node.js 18+
- Çalışan bir PostgreSQL sunucusu
- Groq API anahtarı ([console.groq.com](https://console.groq.com))

### 1) Veritabanı

PostgreSQL üzerinde boş bir veritabanı oluşturun:

```sql
CREATE DATABASE summarize_ai;
```

### 2) Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

copy .env.example .env      # Windows (cp .env.example .env  # macOS/Linux)
```

`.env` dosyasını kendi bilgilerinle doldur:

```
DATABASE_URL=postgresql+psycopg2://<user>:<pass>@localhost:5432/summarize_ai
GROQ_API_KEY=...
JWT_SECRET=...
ADMIN_USERNAME_OR_EMAIL=admin@summarize-ai.com
ADMIN_PASSWORD=...
```

Uygulamayı çalıştır:

```bash
uvicorn app.main:app --reload --port 8000
```

İlk çalıştırmada tablolar otomatik oluşturulur ve `.env`'deki bilgilerle bir **admin hesabı** otomatik oluşturulur (`role=admin`, `status=active`).

API dokümantasyonu: http://localhost:8000/docs

### 3) Frontend

```bash
cd frontend
npm install
copy .env.example .env      # Windows (cp .env.example .env  # macOS/Linux)
npm run dev
```

Uygulama: http://localhost:5173

## Kullanıcı Akışı

1. **Kayıt Ol** sayfasından yeni bir kullanıcı oluşturulur → `status = pending`.
2. `pending` durumundaki kullanıcı giriş yapamaz, "onay bekliyor" mesajı görür.
3. Admin, `.env`'de tanımlı hesapla giriş yapar → **Kullanıcı Yönetimi** sayfasında bekleyen kaydı **Onayla**.
4. Onaylanan kullanıcı giriş yapıp **Ana Sayfa**'dan metin özetleyebilir.
5. Her özetleme isteği `ai_logs` tablosuna kaydedilir, admin **Loglar** sayfasından görebilir.

## Roller

- **user:** yalnızca Ana Sayfa'ya erişir (metin gir → özetle).
- **admin:** Log Görüntüleme + Kullanıcı Yönetimi (onaylama, aktif/pasif etme, şifre sıfırlama, yeni kullanıcı oluşturma).

## Güvenlik

- Şifreler bcrypt (salt+hash) ile saklanır.
- Admin uç noktaları backend'de rol kontrolü (JWT payload) ile korunur; frontend router guard'ı da admin olmayanları yönlendirir.
- API anahtarları ve secret'lar `.env` dosyalarında tutulur, repoya dahil edilmez (`.gitignore`).

## Sınırlılıklar

- Rate limiting, girdi maskeleme, istatistik grafiği ve dil dışı bonus özellikler bu sürümde yok.
- E-posta doğrulama/bildirim mekanizması yok; onay tamamen admin panelinden manuel yapılır.
