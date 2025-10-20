# Backend Erişim Notları

## 🔧 Backend'i Dışarıdan Erişilebilir Yapma

### Problem
- QR kod `localhost:8000` kullanıyor
- `localhost` sadece aynı bilgisayarda çalışır
- Telefon/tablet'ten erişilemez

### Çözüm 1: Backend'i 0.0.0.0'da Çalıştır

Backend'inizi şu şekilde başlatın:

```bash
# Docker ile
docker run -p 0.0.0.0:8000:8000 your-backend-image

# Veya Python ile
python app.py --host=0.0.0.0 --port=8000

# Veya Flask ile
flask run --host=0.0.0.0 --port=8000
```

### Çözüm 2: QR URL'ini Düzelt

QR URL'i şu anda:
```
http://172.20.10.4:8000/receipt/new?amount=50&store=Granny%27s%20Waffle&items=...
```

### Test Et

1. **Backend'i 0.0.0.0:8000'de başlat**
2. **Telefon/tablet'ten test et:**
   ```
   http://172.20.10.4:8000/health
   ```
3. **QR'ı oku** - artık çalışacak

### Güvenlik Notu

- `0.0.0.0` tüm arayüzlerden erişim sağlar
- Sadece güvenli ağda kullanın
- Production'da firewall kullanın

## 🎯 Mevcut Durum

- ✅ Backend çalışıyor: `172.20.10.4:8000`
- ✅ QR URL düzeltildi
- ⚠️ Backend'i `0.0.0.0:8000`'de başlatmanız gerekiyor
