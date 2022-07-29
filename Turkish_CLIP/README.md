## Türkçe Verilerle Eğitilen CLIP Modeli
| ![CLIP](https://raw.githubusercontent.com/mlfoundations/open_clip/main/docs/CLIP.png) |
|:--:|
| Image Credit: https://github.com/openai/CLIP |

CLIP modelinin kullandığı text encoder modeli İngilizce metin alıp embedding yapıyor.
Bu projenin amacı gerçek CLIP modelindeki text encoder kısmını Türkçe verilerle eğiteceğim bir text encoder ile değiştirmek. Bu sayede model Türkçe verileri anlayabilir hale gelecek.

Bu projede text encoder olarak daha önceden Türkçe verilerle eğitilmiş Turkish bert modeli kullanıldı. Bert modeli aldığı bir metni 768 boyutunda bir vektöre dönüştürebiliyor.
Boyutların uyuşması için bert modeline bir model daha eklendi(projection head). Bu modelin yaptığı iş ise aldığı 768 boyutundaki vektörü 512 boyutuna getirmek.


## Eğitim Aşamaları
Eğitim aşamasında sadece text encoder(bert+projection head) modeli eğitildi. 
Aslında amacım, text encoder modelinin sonuçlarının image encoder modelinin sonuçları ile eşleşmasini sağlamaktı. Yani model eğitilirken label olarak image embeddingleri kullanıldı.
Eğitim aşamaları:
- İmage ve metin verileri alınıyor.
- Alınan metin verileri bert tokenizer ile token haline getirilip bu tokenler bert modeline veriliyor.
- Bert modeli 768 uzunluğunda(boyutunda) bir vektör oluşturuyor.
- Oluşturulan vektör, projection head modeline verilip 512 boyutunda text embedding vektörü elde edilmiş oluyor.
- Aynı şekilde image verileri image encoder modeline verilip 512 boyutunda bir image embedding vektörüne dönüştürülüyor.
- Hata için text embedding vektörünün image embedding vektöründen ne kadar farklı olduğu hesaplanıyor. Burada amacım, text embedding vektörü ile image embedding vektörünün tıpatıp benzemesini sağlamak.
- Hataya göre model optimize ediliyor.

## Test Aşaması
Test aşamasında image encoder modeline resimler ve eğittiğim text encoder modeline metinler veriyorsunuz.

Model ise size verdiğiniz metinlerin resimlerle ne kadar eşleştiğini veriyor. Metinle en çok eşleşen fotoğraf sizin istediğiniz sonuç oluyor.
