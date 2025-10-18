# 📱 Basit Mobil QR Handler - Web Landing Page

## 🎯 Nasıl Çalışır?

QR kod direkt web URL'i içeriyor:
```
http://192.168.1.103:8000/receipt/new?amount=25&store=Granny%27s+Waffle&items=[...]
```

**Kullanıcı QR'ı tarattığında:**
- ✅ **Uygulama varsa** → WebView'da aç veya in-app browser'da göster
- ✅ **Uygulama yoksa** → Normal kamera uygulaması URL'i tarayıcıda açar

---

## 📱 React Native / Expo Kodu

### Basit Versiyon (Linking ile)

```javascript
import { Linking } from 'react-native';

const handleBarCodeScanned = async ({ type, data }) => {
  try {
    // QR'dan gelen: http://192.168.1.103:8000/receipt/new?amount=...
    
    if (data.startsWith('http://') || data.startsWith('https://')) {
      console.log('📱 Landing page açılıyor:', data);
      
      // Direkt browser'da aç
      await Linking.openURL(data);
      
      // Landing page fiş bilgilerini gösterecek ve backend'e kaydedecek
    }
    
  } catch (error) {
    console.error('URL açılamadı:', error);
    Alert.alert('Hata', 'Fiş sayfası açılamadı');
  }
};
```

---

## 🌐 WebView ile In-App Açma

Eğer kullanıcıyı uygulamadan çıkarmak istemezseniz:

```javascript
import { WebView } from 'react-native-webview';

const handleBarCodeScanned = async ({ type, data }) => {
  if (data.startsWith('http://') || data.startsWith('https://')) {
    // WebView sayfasına yönlendir
    navigation.navigate('ReceiptWebView', { url: data });
  }
};

// ReceiptWebView Screen
function ReceiptWebViewScreen({ route }) {
  const { url } = route.params;
  
  return (
    <WebView
      source={{ uri: url }}
      onMessage={(event) => {
        // Landing page'den mesaj gelirse (fiş kaydedildi, vs.)
        const message = JSON.parse(event.nativeEvent.data);
        if (message.type === 'receipt_saved') {
          // Fiş kaydedildi, geri dön
          navigation.goBack();
        }
      }}
    />
  );
}
```

---

## 🎨 Komple Örnek - QR Scanner

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Alert, Linking } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';

export default function QRScanner() {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const handleBarCodeScanned = async ({ type, data }) => {
    setScanned(true);
    
    try {
      console.log('📱 QR Okundu:', data);
      
      // WillPay landing page URL'i mi kontrol et
      if (data.includes('receipt/new')) {
        // Landing page'i aç
        await Linking.openURL(data);
        
        Alert.alert(
          'Fiş Sayfası Açıldı',
          'Tarayıcıda fiş detaylarını görebilirsiniz.',
          [
            {
              text: 'Tamam',
              onPress: () => setTimeout(() => setScanned(false), 2000)
            }
          ]
        );
      } else {
        Alert.alert('Hata', 'Geçersiz QR kod');
        setScanned(false);
      }
      
    } catch (error) {
      console.error('QR işleme hatası:', error);
      Alert.alert('Hata', 'URL açılamadı');
      setScanned(false);
    }
  };

  if (hasPermission === null) {
    return <Text>Kamera izni isteniyor...</Text>;
  }
  
  if (hasPermission === false) {
    return <Text>Kamera erişimi yok</Text>;
  }

  return (
    <View style={styles.container}>
      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={StyleSheet.absoluteFillObject}
      />
      
      {scanned && (
        <View style={styles.overlay}>
          <Text style={styles.text}>✅ QR Kod Okundu!</Text>
          <Text style={styles.subtext}>Fiş sayfası açılıyor...</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1
  },
  overlay: {
    position: 'absolute',
    bottom: 100,
    left: 0,
    right: 0,
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 20
  },
  text: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold'
  },
  subtext: {
    color: 'white',
    fontSize: 14,
    marginTop: 5
  }
});
```

---

## 🌍 Landing Page'den Geri Dönüş (Opsiyonel)

Landing page'de fiş kaydedildikten sonra app'e geri dönmek için:

### Landing Page (HTML/JavaScript):
```javascript
// Backend'de /receipt/new sayfasında
<script>
  // Fiş kaydedildikten sonra
  function onReceiptSaved(receiptId) {
    // Deep link ile app'e dön (eğer yüklüyse)
    const appDeepLink = `willpay://receipt/${receiptId}`;
    
    // Önce app'i aç
    window.location.href = appDeepLink;
    
    // Eğer app yoksa (setTimeout'tan sonra hala sayfadaysa)
    setTimeout(() => {
      alert('Fiş başarıyla kaydedildi!');
    }, 500);
  }
</script>
```

### Mobil App Deep Link Handler:
```javascript
import { useEffect } from 'react';
import * as Linking from 'expo-linking';

function App() {
  useEffect(() => {
    // Deep link dinle
    const subscription = Linking.addEventListener('url', ({ url }) => {
      // willpay://receipt/123
      if (url.includes('receipt/')) {
        const receiptId = url.split('/').pop();
        navigation.navigate('ReceiptDetail', { receiptId });
      }
    });
    
    return () => subscription.remove();
  }, []);
  
  // ...
}
```

---

## 📋 Özet

### POS Tarafı ✅
QR içeriği:
```
http://192.168.1.103:8000/receipt/new?amount=90&store=Granny%27s%20Waffle&items=[...]
```

### Mobil Tarafı
**3 Seçenek:**

1. **Basit (Önerilen):** `Linking.openURL(data)` → Browser'da açar
2. **In-App:** WebView ile app içinde göster
3. **Hybrid:** Önce WebView, sonra deep link ile geri dön

**En basit çözüm:**
```javascript
await Linking.openURL(data);
```

Bu kadar! Landing page'iniz zaten her şeyi hallediyor. 🎉

---

## 🎯 Avantajlar

- ✅ Uygulama olmasına gerek yok
- ✅ Normal QR okuyucu yeterli
- ✅ Web'de tüm detaylar görünür
- ✅ Backend otomatik kaydediyor
- ✅ Basit ve hızlı

---

**Mobil uygulamanızda sadece `Linking.openURL(data)` kullanın, backend'inizdeki landing page gerisini halleder!** 🚀

