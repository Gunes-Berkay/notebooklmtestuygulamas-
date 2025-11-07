# 🧠 PyQt6 Quiz Uygulaması

Bu proje, **çoktan seçmeli test sorularını** `.txt` dosyalarından okuyarak **SQLite veritabanına aktaran** ve ardından **PyQt6 arayüzüyle quiz oynatabilen** bir masaüstü uygulamasıdır.

"pip install -r requirements.txt" ile kütüphaneleri kurmanız gerekmektedir.

Soruları hazırlamak için notebooklm kullanıldı, prompt şu şekilde :
 "Her bir pdf'i incele ve her bir pdf için 25 tane çoktan seçmeli soru hazırla. bu soruların bazıları kısa formatlı olsun ve sadece tanım sorsun bazıları da biraz daha konu ile ilgili mantıksal çıkarımlar yapılması gereken ve uzun cevaplı sorular olsun. soruları ingilizce hazırla. her bir soru arasına 20 tane '-' işareti koy ki benim için görülmesi basit olsun. her bir soru metninden önce parantez içerisinde hangi pdf'den aldığını belirt. şıklar bittikten sonra doğru şıkkı parantez içerisinde belirt.  soru metnini ve her bir şık metnini ayrı ayrı '()' içine yani parantez içine al. soruları gönder."

 notebooklm çıktıyı hazırladıktan sonra kopyalayın ardından tests klasörü içerinde bir txt dosyası oluşturun ve o dosyanın içerisine kopyalanan içeriği atın. uygulamayı açtığınız zaman ilgili txt'yi sağ üstten seçtikten sonra "soruları getir" butonuna tıklayın ve ardından test başlıcaktır.

quiz.py ile çalıştırın.



---

## 🚀 Özellikler

✅ `tests/` klasöründeki tüm `.txt` dosyaları otomatik algılanır.  
✅ Kullanıcı, **sağ üstteki seçim kutusundan** çözmek istediği kaynağı seçebilir.  
✅ Kaynak seçildiğinde, sistem ilgili tabloyu oluşturur ve verileri veritabanına kaydeder.  
✅ Sorular ve şıklar rastgele sırayla gösterilir.  
✅ Doğru cevap **yeşil**, yanlış cevap **kırmızı** renkle vurgulanır.  
✅ Üstte skor tablosu bulunur.  
✅ Modern karanlık tema kullanılır.  
✅ Uygulama sabit boyut: `900x500`

---

## 🧩 Klasör Yapısı

