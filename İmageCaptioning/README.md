# İmage Captioning Modeli
Bu model input olarak resim alan ve output olarak resim verir.
Modeli oluştururken pretrained image encoder ve daha önceden [Türkçe verilerle eğitilmiş bir GPT-2 modeli](https://huggingface.co/redrussianarmy/gpt2-turkish-cased) kullandım.

![image](https://user-images.githubusercontent.com/77508537/184653010-23384f2f-e8aa-4afc-a6c2-90103a8ba3d8.png)
Modeli 3 parçaya ayırabiliriz:
- İmage Encoder
- Projection Head
- GPT-2

## İmage Encoder
<img src="../../main/images/clip_image_encoder.jpg">
İmage  Encoder modelleri, verdiğiniz bir resmi N uzunluğunda bir vektöre(image embeddings) dönüştüren modellerdir. Bu elde ettiğiniz vektör, resim hakkında önemli bilgileri(cisimler, renkleri, sayıları vs.) tutar.

Bu proje için kullandığım İmage Encoder modeli, OpenAI'ın yayınlamış olduğu CLIP İmage Encoder modeli. Bu model yaklaşık 400 milyon fotoğraf ile eğitildi. Yani bir resim için neyin önemli olduğunu neyin önemsiz olduğunu çok iyi bilen bir model. Model bu kadar fazla veri ile eğitildiği için bu modeli eğitmedim. Yani proje boyunca bu model hep dondurulmuştu. Bu da diğer projenin parçalarının(Projection Head ve GPT-2) daha hızlı ve doğru eğitilmesini sağladı.

## Projection Head
Bu model, İmage Encoder ile GPT-2 arasında köprü görevi görüyor. İmage Encoder 512 uzunluğunda bir vektör çıkarıyor, GPT-2 ise 7680(10x768) boyutunda bir vektör alıyor. Bu yüzden iki modeli birbirine bağlayacak başka bir model kullandım. Bu model 2 tane dense layer'ından oluşuyor (512 -> 3840 -> 7680). 

## GPT-2 
<img src="../../main/images/GPT-2.gif">
GPT-2, OpenAI tarafından oluşturulmuş metin tabanlı bir transformer modeldir. Model input olarak bir metin alıp output olarak bir metin üretir. Bu projeyi kullanırken modelin Türkçe metin yapısına daha hızlı adapte olabilmesi için daha önceden
Oscar Turkish Corpora ile eğitilmiş bir GPT-2 modeli kullanıldı.

### Referans
Model mimarisi hakkında fikierler https://arxiv.org/abs/2111.09734 makalesi referans alınarak oluşturuldu.
