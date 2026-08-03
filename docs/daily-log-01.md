docs/daily-log-01.md dosyana şu soruların cevabını yaz:

Virtual Environment neden kullanılır? = venv yani iki tane proje varsa ikisi de çakışmasın diye her iki projenin kendi python dünyası vardır buna denir
pip install ne işe yarar? = pandas, numpy, scikit learn yok bilgisayarda bunu internetten indirme yapan programa denir

requirements.txt neden vardır? = githuba yüklerken başkası indirirse o indiren benim hangi kütüphaneleri kullandığımı bilsin diye buraya kaydediyor

CSV = comma seperated values 

1.hatam = FileNotFoundError:
No such file or directory:
'../../dataset/movies.csv'
nedeni code runner ile çalıştırdım yani yol yanlış oldu düşündü ki sadece sayfayı çalıştıracağım ben komple projeyi çalıştırdım

.gitignore sayfası sadece gerekli şeyleri pushlayacak githuba

Neden movieId üzerinden merge yaptın?

Cevabın şu olabilir:

"ratings.csv kullanıcıların puanlarını içeriyor, movies.csv ise film bilgilerini içeriyor. Ortak alan movieId olduğu için iki tabloyu bu sütun üzerinden birleştirdim. Böylece her puan kaydına filmin adı ve türü de eklendi."

# iki tablo alınıyor merged datada saklanıyorlar pd.merge birleştirme fonksiyonu
#  onmovieıd de iki tabloda da ortak olan movieId sütununu kullanarak eşleştir. diyor
# how="inner" = İki tabloda da bulunan kayıtları getir.
# return de birleşen tabloyu döndürüyor.

neden groupby("title") kullandım = aynı filme ait tüm kullanıcı puanlarını bir araya getirip  tek bir ortalama puan hesaplamak için kullandım

agg()
Bu fonksiyonun adı:
Aggregate
Yani aynı anda birden fazla hesaplama yapabilir. = ortalama, oy sayısı

genre= kullanıcının yazdığı tür
 case=False yazı doğru ama harflerin büyük küçük olmasını sorun etmez kabul eder.

 na=False eğer bir satır boşsa hata verme

 ## Error 3

### Error
TypeError: unhashable type: 'list'

### Cause
I accidentally replaced the original "genres" column with a list using:

movies["genres"] = movies["genres"].str.split("|")

Later, functions such as unique() and str.contains() expected string values, not lists.

### Solution
Do not modify the original DataFrame.

Instead, create a new variable:

genres = extract_genres(movies)

iterrows()

Bu yeni bir Pandas fonksiyonu.

DataFrame'in satırlarını tek tek dolaşır.

sorted()= a-z sıralar
input()= kullanıcıdan veri alırız

Sprint 3 Özeti (Türkçe)
Sprint 3 – Film Öneri Motoru

Bu sprintte projenin ilk çalışan öneri sistemi geliştirildi. MovieLens veri seti kullanılarak filmler puanlarına ve oy sayılarına göre analiz edildi. Kullanıcı seçtiği film türüne göre en yüksek puanlı filmleri görebilecek hale getirildi.

Yapılanlar
Film öneri algoritması geliştirildi.
Ortalama puan ve oy sayısı hesaplandı.
Türe göre filtreleme sistemi oluşturuldu.
Kullanıcıdan konsol üzerinden film türü alınmaya başlandı.
Sonuçlar daha okunabilir bir formatta gösterildi.
Kod yapısı modüler hale getirildi (recommender.py, main.py).
Çeşitli hatalar (dosya yolu, import, Unicode vb.) giderildi.
Öğrenilen Konular
Pandas (groupby, merge, sort_values)
Fonksiyon tasarımı
Modüler Python yapısı
Kullanıcıdan veri alma (input)
Konsol arayüzü oluşturma
Hata ayıklama (Debugging)


Sprint 3 Summary (English)
Sprint 3 – Movie Recommendation Engine

In this sprint, the first working recommendation engine of the project was implemented. Using the MovieLens dataset, movies were analyzed based on their average ratings and rating counts. Users can now select a movie genre and receive the highest-rated movies in that category.

Completed Tasks 28/07/2026
Developed the movie recommendation algorithm.
Calculated average ratings and rating counts.
Implemented genre-based filtering.
Added user input through the console.
Improved the output formatting for better readability.
Organized the project into a modular structure (recommender.py, main.py).
Fixed common issues such as file path, import, and Unicode errors.
Topics Learned
Pandas (groupby, merge, sort_values)
Function design
Modular Python architecture
User input handling (input)
Console application development
Debugging techniques

29/07/26
-DataFrame = Satır ve sütunlardan oluşan bir tablo.
-çalıştırma = python backend/app/main.py
- 24 sütun var = title overview budget runtime ... artıyor
- dropna()  Diyor ki "Boş olan satırları sil."
- subset=["overview"] -> overview boş ise demek 
-
links.csv, MovieLens ile TMDB arasında köprü görevi görüyor.
Aynı filmi iki farklı veri tabanında eşleştirebilmemizi sağlıyor.

sprint5- content-based recommendation
vectorization = yazıyı sayıya dönüştürmek love=3 mesela
tf-ıdf -> term frequency - ınverse document frequency
tf= kelime kaç defa geçmiş 
ıdf= ayırt edicileri seçiyor the a falan almıyor.
tf-ıdf = ikisini de birleştiriyor

scikit-learn=sklearn=içinde  TF-IDF Cosine Similarity  KNN Decision Tree  Random Forest  Logistic Regression K-Means PCA Naive Bayes
Yani machine learning araç kutusu
cosine similarity= filmleri karşılaştırır=İki vektör arasındaki benzerliği hesaplıyor.
| Dosya          | Görevi               |
| -------------- | -------------------- |
| data_loader.py | Veriyi yüklemek      |
| recommender.py | Tür bazlı öneriler   |
| main.py        | Programı çalıştırmak |
fit_transform

İkisini tek seferde yapıyor.

Veriyi öğren.
Sayıya dönüştür.
matrix= sayı ve sütunlardan oluşan sayı tablosu 
✅ enumerate() → Her elemana sıra numarası ekler.

✅ lambda → Kısa, tek satırlık fonksiyon yazma yöntemi.

✅ sorted() → Listeyi sıralar.

✅ reverse=True → Büyükten küçüğe sıralar.
loc Etikete göre seçer.
iloc Satır numarasına göre seçer.

Kullanıcı
↓
Toy Story
↓
Toy Story'nin indexini bul
↓
Similarity Matrix'in Toy Story satırını al
↓
En yüksek puanları sırala
↓
Toy Story'yi çıkar
↓
İlk 5 filmi al
↓
İndeksleri film isimlerine çevir
↓
Kullanıcıya listeyi döndür

✅ iloc → Satır numarasına göre veri seçme
✅ append() → Listeye yeni eleman ekleme
✅ Dictionary ({}) → Yapısal veri tutma
✅ for index, score in ... → Tuple açma (unpacking)
✅ f"{...:.2f}" → Ondalık sayıyı 2 basamak gösterme

re = Regular Expressions (Regex)

Yani metin temizlemek için kullanılan Python kütüphanesi.

CLI (Command Line Interface) oluşturuyoruz.

Yani program artık kullanıcıyla konuşuyor.

itertuples()

Bir DataFrame'in satırlarını tek tek dolaşmamızı sağlar.


| Kavram                | Ne işe yarıyor?                                     |
| --------------------- | --------------------------------------------------- |
| **Text Cleaning**     | Metni temizler.                                     |
| **Stopwords**         | Gereksiz kelimeleri siler.                          |
| **TF-IDF**            | Metni sayılara dönüştürür.                          |
| **Vectorization**     | Her filmi bir sayı listesi (vektör) haline getirir. |
| **Scikit-learn**      | Bu işlemleri yapan makine öğrenmesi kütüphanesi.    |
| **Cosine Similarity** | İki metnin ne kadar benzediğini hesaplar.           |
| **argsort()**         | En yüksek benzerlik puanlarını sıralar.             |
| **iloc()**            | Bu puanlara karşılık gelen filmleri getirir.        |
6.sprint
Embedding, bir kelimeyi veya cümleyi ANLAMINI temsil eden sayılara çevirir.
Sentence Transformer bu milyonlarca cümleyle eğitilmiş bir hazır AI modeli
-AI Modeli oluşturuyor
Transformer

Google'ın geliştirdiği

çok güçlü bir yapay zekâ mimarisi.

Pooling ise diyor ki Bunların hepsini tek bir vektöre dönüştür.

Normalize demek vektörü standart hale getirmek.

model.encode() metodu (özellikle Sentence-Transformers veya Hugging Face kütüphanelerinde), verilen bir metni veya metin listesini sayısal vektörlere (embeddings) dönüştürür.

Kısacası: Metnin anlamsal içeriğini bilgisayarların anlayabileceği ve matematiksel olarak kıyaslayabileceği bir "anlam vektörüne" çevirir.
.tolist()=Listeye çevirmek için
.Çünkü AI modeli (SentenceTransformer) Python listesini daha 
rahat işler.
# Sprint 6 Progress

Today I implemented an AI-powered semantic movie recommendation system.

Completed tasks:

- Learned how embeddings work.
- Integrated Sentence Transformers.
- Generated embeddings for over 44,000 movies.
- Saved embeddings with pickle to avoid recalculation.
- Implemented semantic search using cosine similarity.
- Added user input for dynamic movie recommendations.
- Refactored the code using the main() function.

Outcome:

The recommendation system can now understand the meaning of user queries instead of relying only on keyword matching.

Yani Swagger aslında API test ekranı.
sentence-transformers = cümleleri anlayan ve onları sayısal vektöre dönüştüren AI modeli
# Convert movie descriptions and user queries into numerical vectors
# so we can compare their semantic similarity.


# Sprint 7

## Date
03.08.2026

## Tasks Completed

- Installed FastAPI
- Installed Uvicorn
- Created api.py
- Created GET endpoints
- Learned Swagger documentation
- Connected Semantic Search with FastAPI
- Fixed import issues
- Returned JSON responses
- Successfully tested the API

## Result

The CineMind backend can now provide AI-powered movie recommendations through a REST API.