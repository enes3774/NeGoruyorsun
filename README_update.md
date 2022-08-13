# Ne Görüyorsun?
Ne Görüyorsun, çeşitli resimleri metinsel olarak tasvir eden GPT2 ve CLIP modellerini kullanan Türkçe Doğal Dil İşleme projesi.

...

# Projenin Detayları
Proje iki kısımdan oluşuyor, image encoder ve text decoder. İmage encoder, verilen resmi 512 uzunluğunda bir vektöre dönüştürür. 
Bu vektör içinde resimdeki önemli detayları(eşyalar,onların renkleri vs.) barındırır. Oluşturulan bu vektör başka küçük bir model sayesinde text_decoder'a verilmek için boyutu arttırılır.
Arttırılan bu vektör text decoder modeline verilir. Bu model ise adlığı vektöre göre bir metin oluşturur. Oluşturulan bu metin, modelin resimde gördükleri olur.

Projeyi yaparken daha önceden Türkçe verilerle eğitiliş  gt2 modeli kullanıldı. Bunun nedeni modelin daha hızlı Türkçe metinlere uyum sağlaması. İmage encoder olarak da OpenAI'ın yayınlamış olduğu CLIP image encoder modeli kullanıldı.
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
