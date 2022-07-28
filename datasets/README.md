Veriseti yaklaşık 260.000 tane fotoğrafın url'i ve o resme karşılık gelen metni barındırıyor.

Veriseti, https://arxiv.org/abs/2103.01913 makalesindeki toplanan veriler işlenerek oluşturulmuştur.

## Veriyi Temizleme
- Sadece Türkçe veriler alındı.
- Alınan verilerde GIF,SVG gibi modeli eğitirken kullanmadığım fotoğraf türleri atıldı.(yaklaşık 5 bin fotoğraf)
- Bazı wikipedia sayfalarında fotoğrafların tanımları olmayabiliyor.(%50'sinde yok)
 <table>
  <tr>
    <td><img src="../images/image_with_alttext.png" width="300"></td>
    <td><img src="../images/image_without_alttext.png" width="300"></td>
  </tr>
  <tr>
    <td>Altında tanımı olan Wikipedia resmi </td>
     <td>Altında tanımı olmayan Wikipedia resmi</td>
  </tr>
 </table>
 
- Eğer tanımı yoksa o fotoğrafa karşılık gelen metni o sayfanın başlığından aldım.
- Bazı url'lerdeki fotoğraflar silinmişti. Silinen fotoğraflar tespit edilip çıkartıldı.

Şuanki verisetinde "url" ve "captions" olmak üzere iki sütun bulunuyor.

