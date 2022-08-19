# Ne Görüyorsun?
Ne Görüyorsun, çeşitli resimleri metinsel olarak tasvir eden GPT2 ve CLIP modellerini kullanan Türkçe Doğal Dil İşleme projesi.

Proje Takım Adı: TEXT-GEN

![image](https://user-images.githubusercontent.com/77508537/184640351-05e43f6d-ea4b-459b-a4be-be21da65e717.png)

[![Kaggle](http://img.shields.io/static/v1?logo=kaggle&style=plastic&color=blue&label=kaggle&labelColor=grey&message=notebooks)](https://www.kaggle.com/code/eneskulak/ne-goruyorsun)
# Projenin Motivasyonu
Görme engellilerin en büyük problemi dış çevreyi tanımlamaktır. Bu sorunu çözebilmek için onlara dış çevreyi tasvir eden bir yapay zeka projesi geliştirdim.

Bu proje bir resim alır ve bu resmi analiz edip size yazıyla tasvir eder. Model eğitilirken kendi oluşturduğum wikipedia resim-metin veriseti, Turkish MSCOCO ve Tasvir Et verisetleri kullanılmıştır. Datasets kısmından daha fazla ayrıntıya bakabilirsiniz.

Model Kaggle ortamında yaklaşık 10 saat eğitildi. Her bir epoch 3 saat sürdü yani yaklaşık 3 epoch eğitilidi.

Teknofest Sunum Linki:https://docs.google.com/presentation/d/1U-gMP8bJkzaW_pu14nTu5CHa3S7SChhUdHkBMDg0tWQ
# Örnek
https://user-images.githubusercontent.com/77508537/185377116-aaa2690e-6353-4684-9a59-dfea08501a05.mp4



# Modelin Detayları
Proje iki kısımdan oluşuyor, image encoder ve text decoder. İmage encoder, verilen resmi 512 uzunluğunda bir vektöre dönüştürür. 
Bu vektör içinde resimdeki önemli detayları(eşyalar,onların renkleri vs.) barındırır. Oluşturulan bu vektör başka küçük bir model sayesinde text decoder'a verilmek için boyutu arttırılır.
Arttırılan bu vektör text decoder modeline verilir. Bu model ise aldığı vektöre bakarak yeni bir metin oluşturur. Oluşturulan bu metin, modelin resimde gördükleri olur.

| ![CLIP](../main/images/model_sema.jpg) |
|:--:|
| İmage Captioning Modeli |

Projeyi yaparken daha önceden Türkçe verilerle eğitilmiş  GPT-2 modeli kullanıldı. Bunun nedeni modelin daha hızlı Türkçe metinlere uyum sağlamasıydı. İmage encoder olarak da OpenAI'ın yayınlamış olduğu CLIP Image Encoder modeli kullanıldı.
Bu modeli kullanmış olmamın nedeni, modelin daha önceden 400 milyon fotoğraf üzerinde eğitilmesi. Bu sayede model daha hızlı optimize edilebildi.

# Model Sonuçları
 <table>
  <tr>
    <td><img src="../main/images/test1.jpg" width="300"></td>
    <td><img src="../main/images/test3.jpg" width="300"></td>
    <td><img src="../main/images/test5.png" width="300"></td>
  </tr>
  <tr>
    <td>Bir kız doğum günü pastasında mumları üfler.</td>
     <td> Sörf yapan bir adam.</td>
    <td>Bir grup otobüs, bir otoparkta park edildi.</td>
  </tr>
 </table>
 <table>
  <tr>
    <td><img src="../main/images/test2.png" width="300"></td>
    <td><img src="../main/images/test4.jpg" width="300"></td>
    <td><img src="../main/images/test6.jpg" width="300"></td>
  </tr>
  <tr>
    <td>Bir köpek bir yöne bakıyor.</td>
     <td> Elmanın yakın plan görüntüsü.</td>
    <td>Çimlerin altında duran bir yavru kedi.</td>
  </tr>
 </table>
 
 # Modeli Eğitmek 
 ### 1. Projeyi Kendi Bilgisayarınıza Yükleyin
  ```
  git clone enes3774/NeGoruyorsun 
  ```
 
 ### 2. Bağımlılıkları İndir
 Modeli eğitmek için öncelikle requirements.txt dosyasındaki kütüphanelerin kurulmuş olması gerekir.
  ```
  pip install -r requirements.txt
  ```
  
  Bir de CLIP kütüphanesini github sayfasından yüklemeniz gerekiyor.
  ```
  pip install git+https://github.com/openai/CLIP.git
  ```
 
 ### 3. Örnek Dataseti veya Kendi Datasetinizi İndirin
Modeli eğitmek için resimlere ve resimlerin Türkçe metinleri olan bir json dosyasına ihtiyacınız var. 
- Örnek olarak MSCOCO resimlerini [buradan](https://www.kaggle.com/datasets/aftaab/mscoco) indirin ve proje dosyasında "images_data/" klasorü oluşturup içine atın. 
- Bu resimlerin Türkçe metinlerini barındıran json dosyasını da [buradan](https://github.com/giddyyupp/turkish-image-captioning/blob/master/MSCOCO/train/coco_train_captions_tr.json) indirip "dataset.json" olarak proje dosyasına koyun. Faklı verisetleri hakkında daha fazla bilgiyi datasets klasorunde bulabilirsiniz.

Dataseti hazırladıktan dosya klasoru bu şekilde olmalı: 

    .
    ├── images                  # Github için kullanılan resimler burada 
    ├── datasets                # verisetleri ve kullanımı hakkında 
    ├── İmageCaptioning         # Projenin modeli bu dosyada bulunuyor
    ├── images_data                  #içerisinde kullandığın verisetinin fotoğrafları olmalı
    ├── .gitignore            
    ├── dataset.json             #images içindeki resimlerin dosya adları ve o resme karşılık gelen metinleri barındırıyor 
    ├── LICENSE
    ├── requirements.txt
    └── README.md
 Kullandığınız dataset flickr ise train.py kodunda 4. satırı okuyun. 
 
  ### 4. Modeli Eğitmek
 
 Modeli eğitmek için  aşağıdaki kodu yazın.
 ```
  python İmageCaptioning/train.py
 ```
 Train dosyasındaki hiperparametreleri(epoch sayısı, batch_size, learning rate vb.) düzenleyip modeldeki sonuçları gözlemleyebilirsiniz(şuanki hiperparametrelerde model doğru sonuç verecektir.). Modeli bu veriyle 1 epoch eğitmeniz bile yeterli olacaktır.
 
 # Test Aşaması
 ### 1. Eğitilen Modeli Kaydetmek
 Eğittiğiniz modeli ImageCaptioning dosyası içinde "checkpoints/" klasorune "model_latest.pth" şeklinde koymanız gerekiyor(Modeli eğitirken her 6000 adımda bir ve epoch sonunda kaydediliyor. Train ederken model doğru yere kaydedilecektir.). Hazır bir model checkpoint paylaşmayacağım çünkü model çok hızlı bir şekilde(yaklaşık 1-2 saate çalışan bir model elde edebilirsiniz.) eğitebiliyor olmanız.
 ### 2. Modeli Test Etmek
 Modeli belirtlien dosyaya koyduktan sonra test kodunu çalıştırın. 
  ```
  python İmageCaptioning/test.py
 ```
Test kodundaki resmi değiştirip farklı resimler için modeli test edebilirisiniz.
## 📓 Kaggle

* Modeli [Kaggle](https://www.kaggle.com/code/eneskulak/ne-goruyorsun) ortamında yaklaşık 2 saatte eğitebilirsiniz. İçerisinde eğittiğiniz modeli kullanmak için beam_search ve greedy olmak üzere 2 algoritma bulunuyor.

## Videoları Tasvir Etmek

Bu model ile videoları tasvir etmek de mümkün. Bununla alakalı   ```PredictVideoCaption.py``` kodunu paylaştım. Bunu yaparken verdiğiniz videodan 5 saniyede bir resim alınıp modelden geçiriliyor. Elde ettiğiniz metinler toplanıyor ve bu sizin videoda ne yaptığınızın özeti oluyor. Burada cümleler birbirine benzeyebilir. Bunu önlemek için birbirine çok benzeyen cümleleri atabilirsiniz.

Bunu kullanarak tam zamanlı görüntü tasviri yapabilirsiniz.
### Örnek
!!!LÜTFEN SESİ AÇIN






https://user-images.githubusercontent.com/77508537/185651778-a2a6df5e-5e48-403b-9446-7c94b232a52d.mp4






NOT: Oluşturulan cümleler tamamen eğittiğim yapay zeka tarafından elde edildi. Projenin işlevselliğini ortaya çıkarmak için bir video düzenleyicisinden seslendirme ve altyazı eklenmiştir. Bunu Google Text to Speech gibi bir API kullanarak otomatik şekilde yapmak mümkün.

## Risk Puanı Hesaplanması
Elde edilen cümleler üzerinde kullanıcıyı tehdit eden durumlar tespit edilmesi ve kullanıcıyı uyarmak için risk puanı hesaplanmıştır. Bununla alakalı ```CalculateTestScore.ipynb``` kodu hazırlandı. Yaptığı şey, verdiğiniz metni almak ve bu cümlenin bir görme engelli için ne kadar tehlikeli olduğunu döndürmek.
Bunu yaparkenki aşamaları:
1. Cümleler kelimelere ayrıldı ve her bir kelimenin kökü alındı
2. Alınan kelime köklerinin, daha önceden verilen tehlikeli kelimelerle olan benzerliği hesaplandı. Bu sayede o kelimenin ne kadar tehlikeli olduğu öğrenildi.
3. Elde edilen kelimelerin tehlike puanları toplanıp o cümlenin tehlike skoru hesaplandı.

## Gelecek Hedefler
1. Veriyi Genişletmek
Modele günlük hayatta olmayan veriler(animasyonlar, hayali figürler, sanatlar) vererek modelin her konuda fikir sahibi olmasını sağlamak.

2. Modelin videoları daha iyi anlaması için frame değil birden çok frame’i aynı anda alıp değerlendiren bir video encoder model kullanılması.

3. Projenin mobil app halinde kullanılabilir olması.

4. Giyilebilir bir teknoloji ile görme engelliler için projeyi hayata geçirmek. Eğer model sonuçları arttırıl
