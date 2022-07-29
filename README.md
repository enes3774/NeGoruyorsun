# Metni Resme Çevirme

## Ben Kimim?
Merhaba ben Enes Mahmut Kulak. Bartın Fen Lisesi 10. sınıf öğrencisiyim. Daha öncesinde yapay zeka ile alakalı kongrelerde sunum yapmıştım. Yapay zeka ile 9. Sınıfta tanıştım ve sonrasında kendimi bu alanda geliştirmeye başladım. Bu yazı da Teknofest 2022 Doğal Dil İşleme Yarışmasına katılarak geçirmek istedim.
## Projenin Motivasyonu
Daha önceden metin alıp resim üreten(image generation) veya resim alıp metin üreten(image captioning) yapay zeka modelleri görmüşsünüzdür. Ama bu modeller genelde İngilizce oluyor ve çeviri kullanınca istediğiniz sonucu alamayabiliyorsunuz.
İşte bu projenin amacı Türkçe bir veriseti kullanarak bu tip bir model üretmek.
## Proje Hakkında
Bu proje 3 farklı model barındırıyor.
- Türkçe verilerle eğitilmiş CLIP modeli
- Verilen resmi Türkçe tasvir eden model
- Verilen Türkçe metne göre resim oluşturan model
Her bir model elde ettiğim tamamen Türkçe metin-resim çiftleri ile eğitildi.

## Türkçe Veriseti
Bu projeyi yapmak için resim ve o resmi tasvir eden Türkçe metin barındıran bir verisetine ihtiyacım vardı. Bu veriseti, Wikipedia'daki resimler ve o resimlerin altında yazan tanımlarıyla oluşturuldu. Veriseti, toplam 260.000 resim ve ona karşılık gelen metin çiftlerini barındırıyor.
Verisetini dataset klasörü içinde bulabilirsiniz.

## Türkçe Verilerle Eğitilmiş CLIP Modeli
OpenAI'ın yayınlamış olduğu CLIP modeli, bir resim ile bir metnin ne kadar benzer olduğunu bize verebiliyor. Bunu yaparkenki kullandığı yöntem ise metinleri ve resimleri aynı boyuta getirmek. Model içinde text encoder ve image encoder olmak üzere 2 farklı model barındırıyor. 
| ![CLIP](https://raw.githubusercontent.com/mlfoundations/open_clip/main/docs/CLIP.png) |
|:--:|
| Resim: https://github.com/openai/CLIP |

Bu modeller sayesinde resim ve metinler 512 uzunluğunda bir vektöre dönüşüyor. Eğer resim ve metin benziyorsa vektörleri de benziyor. Yani "bu bir köpek" metninin vektörü ile köpek fotoğrafının vektörü benzer olacaktır.

Aslında model, resimlerle metinler arasındaki bağlantıyı öğreniyor.

Ben de elde ettiğim wikipedia dataseti ile ilk CLIP modeli gibi çalışan bir model oluşturdum. 

Modelin Türkçe metinleri anlaması için CLIP modelinin text encoder kısmını kendi oluşturduğum model ile değiştirdim. Sıfırdan model oluşturmak yerine Türkçe verilerle eğitilmiş bir bert modelini kullandım. Bert modeli output olarak 768 uzunluğunda bir vektör veriyordu. Modelin sonuna 512 uzunluğunda bir vektör vermesi için başka bir model daha ekledim. Böylelikle boyutlar konusundaki problemi çözmüş oldum.
