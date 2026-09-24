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

venv\Scripts\activate = venve aktif
Çünkü idx aslında numpy.int64 tipinde olabilir. JSON'a göndermeden önce normal Python int'ine çeviriyoruz.

Bir endpoint, API'nin kapısıdır.

Mesela evini düşün.

Evinin:

🚪 Ana kapısı
🚪 Balkon kapısı
🚪 Garaj kapısı

var.

Hepsi aynı eve ait ama farklı işler yapıyor.

API'de de aynı mantık var.

Bizim API'mizde şu an:

GET /

➡️ Ana sayfa

GET /search

➡️ Film ara

GET /movie/{id}

➡️ Tek filmin detayını getir

İşte bunların her biri bir endpoint'tir.

HTTPException demek:

"FastAPI, kullanıcıya düzgün bir hata mesajı gönder."

input validation (girdi doğrulama)

# Sprint 8

## Completed

- Improved REST API
- Added Movie Detail endpoint
- Added Movie List endpoint
- Added Pagination
- Added Sorting
- Added Input Validation
- Improved Search API
- Tested all endpoints using Swagger UI

## Status

Sprint 8 Completed Successfully

REST API, istemci (client) ile sunucu (server) arasında HTTP istekleri kullanarak veri alışverişi yapan bir yazılım arayüzüdür.
Endpoint, API içerisindeki belirli bir URL'dir ve belirli bir görevi yerine getirir.
Path Parameter = URL'nin bir parçası olarak gönderilen değişkendir.

Marketten diyorsun ki

Bana kola getir.

Kasiyer soruyor.

Büyük mü küçük mü?

İşte sonradan verilen bilgiler Query Parameter.


input validation = Kullanıcıdan gelen verinin kurallara uygun olup olmadığını kontrol etmektir.

Telefon alıyorsun.

Kullanım kılavuzu var.

Swagger da API'nin kullanım kılavuzu.

React, kullanıcı arayüzü (User Interface - UI) oluşturmak için kullanılan açık kaynaklı bir JavaScript kütüphanesidir (library). Facebook (Meta) tarafından geliştirilmiştir.
anım

Component, React uygulamasının yeniden kullanılabilen küçük bir parçasıdır.

Her component tek bir görevi yerine getirir.

JSX (JavaScript XML), JavaScript içerisinde HTML benzeri kod yazmamızı sağlayan özel bir sözdizimidir.

React aslında JSX'i JavaScript'e dönüştürerek çalıştırır.

Library (Kütüphane): Sadece ihtiyacın olan araçları kullanırsın. React buna örnektir.
Framework: Uygulamanın genel yapısını da belirler. Örneğin Angular veya Django.

| Dosya/Klasör      | Görevi                                                       |
| ----------------- | ------------------------------------------------------------ |
| **src/**          | Uygulamanın tüm React kodları burada olacak.                 |
| **App.jsx**       | Ana React component'i. İlk değiştireceğimiz dosya.           |
| **main.jsx**      | React uygulamasını başlatır. Genellikle çok az değiştirilir. |
| **App.css**       | App component'inin stilleri.                                 |
| **index.css**     | Genel CSS dosyası.                                           |
| **public/**       | Logo, resim gibi herkese açık dosyalar.                      |
| **package.json**  | Projenin kullandığı paketleri ve komutları tutar.            |
| **node_modules/** | `npm install` ile indirilen kütüphaneler. Elle düzenlenmez.  |


export default SearchBar;

şunu söyler:

"Bu component'i başka dosyalar da kullanabilir."

Şu an SearchBar.jsx dosyasını oluşturduk.
Ama React henüz onun varlığını bilmiyor.
Çünkü sadece dosyayı oluşturmak yetmez.
Onu kullanacağımız dosyaya import etmemiz 
gerekir.

component kullanma adımları= 1.component oluştur
2.export et
3.başka dosyada import et
4.jsx içinde kullan

State, bir React component'inin zamanla değişebilen verileridir.

State değiştiğinde React ilgili component'i yeniden render (yeniden çizim) eder.

useState, React'in state oluşturmak için kullandığı Hook'tur.(kanca)

event function = Yani butona basılınca çalışacak fonksiyon.

handleSearch()= butona basınca çalışıyor

Fetch API, JavaScript'in başka bir sunucudan veri almak veya veri göndermek için kullandığı yerleşik (built-in) fonksiyondur.

response.json() -JSON verisini JavaScript nesnesine çeviriyor.

CORS (Cross-Origin Resource Sharing), tarayıcının güvenlik mekanizmasıdır.

Tarayıcı, farklı adreslerde çalışan uygulamaların birbiriyle konuşmasını varsayılan olarak engeller.

function MovieCard({ movie })

Bu Props denilen kavramdır.

Props = Bir component'e dışarıdan veri göndermek.

map() nedir?

map(), dizinin (Array) her elemanı için işlem yapar.

SearchBar → Veriyi alır.
App → Veriyi saklar ve yönetir.
MovieList → Listeyi oluşturur.
MovieCard → Tek bir filmi gösterir.

useEffect'in görevi

Sayfa açıldığında otomatik bir işlem yapmak.

# Sprint 8 — React Frontend

## Goals
- Build the React frontend.
- Connect React with the FastAPI backend.
- Display AI-powered movie recommendations.
- Improve user experience.

## Completed Tasks

✔ Created React project with Vite.

✔ Learned JSX and Components.

✔ Built reusable React components.

- SearchBar
- MovieCard
- MovieList

✔ Learned Props.

✔ Learned useState.

✔ Learned useEffect.

✔ Connected React to FastAPI.

✔ Used Fetch API.

✔ Switched from Fetch API to Axios.

✔ Implemented movie search.

✔ Displayed movie recommendations.

✔ Added Loading State.

✔ Added Error Handling.

✔ Tested React ↔ FastAPI communication.

## Technologies

- React
- Vite
- Axios
- FastAPI
- REST API
- Semantic Search

## Result

Sprint 8 completed successfully.

The CineMind AI frontend can now communicate with the backend and display AI-generated movie recommendations in real time.

useParams
Nedir?

URL'deki değişkeni okumamızı sağlar.

BrowserRouter

Bütün uygulamada yönlendirmeyi aktif eder.

Routes

Tüm sayfaları içinde tutar.

Route

Belirli URL'yi belirli sayfaya bağlar.

useParams()

React Router'ın Hook'udur.

URL'den değişken okumaya yarar.

useEffect= sayfa açıldığında çalışır
Axios GET= Backende istek gönderir
response.data= backendin döndürdüğü jsonu alır
state güncelleme = veriyi react stateine kaydeder

# Daily Log – Sprint 9

## Date
06.08.2026

## Tasks Completed

- Added React Router
- Created Home page
- Created Movie Detail page
- Added dynamic routing
- Connected React to FastAPI using Axios
- Implemented Movie Detail API endpoint
- Displayed movie title
- Displayed overview
- Displayed genres
- Displayed rating
- Displayed release date
- Fixed CORS issues
- Tested complete navigation flow

## Result

Sprint 9 completed successfully.
The application now supports navigation between movie search results and detailed movie pages.


## Daily Log – Authentication, Favorites & Rating System

### Completed

- Implemented user registration
- Implemented user login
- Added password hashing with bcrypt
- Added JWT authentication
- Added protected FastAPI endpoints
- Created User and Favorite database models
- Implemented add/remove favorites
- Connected favorites to authenticated users
- Added Favorites page in React
- Added movie rating system
- Added 1–5 star rating UI
- Connected movie ratings to the backend
- Tested registration, login, favorites and rating functionality

### Current Project Status

The core user system is now functional. Users can register, log in, receive a JWT token, add/remove favorite movies and rate movies.

### Next Step

Implement personalized movie recommendations based on user ratings.

clean_text() fonksiyonun:text = text.lower ile metni küçültüyor.

pip install nltk= NLTK = Natural Language Toolkit.
Yani Python'da insan dilindeki metinleri işlememize yardımcı olan bir kütüphane.
Biz CineMind'da kullanıcının yazdığı:
I want a movie about space and loneliness
gibi metinleri daha düzgün işleyebilmek için kullanacağız.

NLTK → metni hazırlar 🧹
TF-IDF → metni sayısal vektöre dönüştürür 🔢
Cosine Similarity → iki metnin ne kadar benzer olduğunu ölçer 📐
CineMind → buna göre film önerir 🎬

lemmatization = Buradaki amaç, kelimelerin farklı biçimlerinin sistemi gereksiz yere yanıltmasını azaltmak.

NLP = Natural Language Processing = Doğal dil işleme = bilgisayarların insan dilini/metinlerini analiz etmesini ve işlemesini sağlayan yapay zekâ alanıdır.

Stopwords, metinde sık kullanılan ve recommendation açısından genellikle düşük bilgi taşıyan kelimelerdir.

Stemming

Kelimeyi basitçe köküne benzetmeye çalışır.

Lemmatization

Kelimenin dilbilgisel/anlamsal temel biçimini bulmaya çalışır.

Örneğin bazı durumlarda stemming anlamsız bir kelime üretebilir.

Bu yüzden NLP projelerinde lemmatization daha anlamlı sonuçlar verebilir.
IDF

Inverse Document Frequency

Kelimenin bütün dokümanlarda ne kadar yaygın olduğuna bakar.

                    CineMind AI
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
     MovieLens       Content-Based    Semantic
    Recommendation   Recommendation   Recommendation
          │              │              │
          ↓              ↓              ↓
     Rating verisi     TF-IDF        Embedding
                                      ↓
                                Sentence Transformer


 data_loader.py, CineMind AI'daki film, rating, TMDB, credits, keywords ve link verilerini yükleyen veri erişim katmanıdır.

AI dosyaları veriye doğrudan dosyadan değil, çoğunlukla data_loader.py üzerinden ulaşır.

Day 1 23 eylül  — AI & Backend Audit

CineMind AI'ın mevcut backend sistemi incelendi.

Mevcut sistemde Content-Based Recommendation, TF-IDF, NLP preprocessing, lemmatization, cosine similarity, Sentence Transformer, semantic search, JWT authentication, favorites, ratings ve personalized recommendation zaten bulunmaktadır.

Eksik/iyileştirilecek bölümler:

Keyword Recommendation API endpoint
Duplicate recommendation filtering
Recommendation score sorting
Movie ID consistency
Popular movies endpoint improvement
Semantic Search code cleanup

Mevcut çalışan özellikler tekrar geliştirilmeyecek; eksik özellikler tamamlanacaktır.

çalıştırma backend
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\Users\Yeşim\OneDrive\Masaüstü\CineMind-AI\venv\Scripts\Activate.ps1)

sonra bu uvicorn backend.app.api:app --reload
Personalized Recommendation Improvement

Existing personalized recommendation endpoint was improved.

User ratings of 4 or 5 stars are used as liked movies.

Content-Based Recommendation generates similar movies using TF-IDF and cosine similarity.

Duplicate recommendations are removed.

Movies already rated by the user are excluded.

If the same movie is generated from multiple liked movies, the highest similarity score is preserved.

Final recommendations are sorted by similarity and the top 10 results are returned.

Day 1 – Step 3: Movie ID Consistency

/movies endpointinde title sorting yapıldığında sıralanmış listedeki pozisyon yanlışlıkla movie ID olarak kullanılıyordu.

Pandas DataFrame'in original index değeri korunarak movie ID olarak kullanılmaya başlandı.

/movies ve /movie/{movie_id} endpointleri arasında ID tutarlılığı sağlandı.

Movie list response'una poster_path ve rating alanları da eklendi.

Keyword Search — kelimelere bakıyor
Semantic Search — anlamı anlamaya çalışıyor

CineMind AI implements two text-based recommendation approaches. The keyword-based system uses NLP preprocessing, TF-IDF vectorization and cosine similarity. The semantic search system uses a Sentence Transformer to convert movie descriptions and user queries into dense embeddings, then retrieves movies using cosine similarity. Therefore, the semantic system can capture contextual similarity beyond exact keyword overlap

CineMind AI, iki metin tabanlı öneri yaklaşımı uygulamaktadır. Anahtar kelime tabanlı sistem, NLP ön işleme, TF-IDF vektörleştirme ve kosinüs benzerliği kullanır. Semantik arama sistemi ise film açıklamalarını ve kullanıcı sorgularını yoğun gömülü vektörlere dönüştürmek için bir Cümle Dönüştürücü (Sentence Transformer) kullanır ve ardından kosinüs benzerliği kullanarak filmleri bulur. Bu nedenle, semantik sistem, tam anahtar kelime örtüşmesinin ötesinde bağlamsal benzerliği yakalayabilir.

                    HYBRID AI

Content Similarity       TMDB Rating       Popularity
       │                      │                 │
      %60                    %25               %15
       │                      │                 │
       └──────────────┬───────┴─────────────────┘
                      ↓
                 Hybrid Score
                      ↓
                  Ranking


Sprint 10 – Hybrid Recommendation v1 ✅
The personalized recommendation system was upgraded from similarity-only ranking to hybrid ranking. The system combines content similarity (60%), TMDB vote average (25%), and popularity (15%). The signals are normalized and combined into a final hybrid_score. Recommendations are now ranked according to the hybrid score instead of content similarity alone.


Sprint 10 – Semantic Hybrid Recommendation v2 ✅
Sentence Transformer embeddings were integrated into the personalized recommendation pipeline. Existing cached movie embeddings are reused instead of recalculating embeddings. Candidate movies are generated using TF-IDF content-based recommendation and re-ranked using semantic similarity, TMDB rating, and popularity. The final hybrid score combines 40% content similarity, 30% semantic similarity, 20% TMDB rating, and 10% popularity.

Sentence Transformer:

“Bu metnin anlamını sayılara dönüştür.”

FAISS:

“Bu sayılara en yakın olan diğer sayıları çok hızlı bul.”

Hybrid Recommendation:

“Bulduğumuz adaylardan hangisini kullanıcıya daha üst sırada göstermeliyim?”

Sprint 10 – FAISS Semantic Search ✅
FAISS was integrated into the semantic movie search system. Existing Sentence Transformer movie embeddings are normalized and stored in a FAISS IndexFlatIP vector index. User queries are converted into embeddings, normalized, and searched against 44,512 movie vectors using nearest-neighbor search. FAISS now provides the semantic search results returned by the FastAPI /search endpoint.


Sprint 10 – FAISS Hybrid Recommendation ✅
FAISS vector search was integrated into the personalized recommendation engine. For every movie liked by the user, the system now generates candidates from both TF-IDF content-based retrieval and FAISS semantic vector retrieval. Duplicate candidates are merged and ranked using a hybrid score combining content similarity (40%), semantic similarity (30%), TMDB rating (20%), and popularity (10%). Sentence Transformer embeddings are reused from cache, avoiding repeated movie embedding generation.

                 CİNEMIND AI

Kullanıcı
   │
   ├── Kayıt / Login
   ├── Film arama
   ├── Favori ❤️
   └── Rating ⭐
          │
          ▼
     FastAPI Backend
          │
    ┌─────┴──────────────┐
    │                    │
 TF-IDF            Sentence Transformer
    │                    │
kelime benzerliği    anlam benzerliği
    │                    │
    │                  FAISS
    │                    │
    └─────────┬──────────┘
              ▼
        Hybrid Score
              │
              ▼
      Personalized Movies
              │
              ▼
         React Frontend

AI Recommendation → kullanıcının o anda yazdığı doğal dil isteğini anlıyor.

Hybrid recommendation, kullanıcının geçmiş rating davranışlarını kullanarak kişiselleştirilmiş öneriler üretir. Natural-language AI recommendation ise kullanıcının o anda yazdığı isteği yorumlayarak semantic retrieval gerçekleştirir.

ome.jsx
→ AI Movie Assistant + ana sayfa yapısı

App.css
→ ana tasarım, renkler, kartlar, butonlar

index.css
→ genel body/background/yazı ayarları

MovieCard.jsx
→ film kartlarının görünümü

Navbar.jsx
→ üst menü


Sprint 10 – AI Movie Assistant Frontend ✅
The React Home page was integrated with the /ai-recommend endpoint. Users can now describe a desired movie in natural language, including Turkish requests. CineMind sends the request to the local Llama model, performs semantic retrieval with Sentence Transformers and FAISS, and displays the resulting movies in the frontend.