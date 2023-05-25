# Problem
Saya pengen lihat diantara satu indonesia ini, website mana sih yang paling bagus untuk tingkat kabupaten dan kota. 

untuk menguji itu semua tentu saya harus cari dulu alamat website seluruh kabupaten di indonesia.

selanjutnya ingin itu semua diambil screenshotnya. lalu saya akan biarkan kalian yang menilainya.

# Roadmap Solution

beberapa hal yang ada dipikiran :

- [🗸] Pengen buat gimana cara otomatis ambil screen shot semua website 
- [🗸] Bagaimana cara implementasinya, jika itu memungkinkan menggunakan python+chromewebdriver
- [🗸] chromewebdriver sepertinya lambat, apakah ada alternatif lain yang lebih cepat?
- [🗸] bagaimana screenshot yang diambil itu fullpage
- [🗸] bagaimana jika setiap kali mengambil screenshot ada loading
- [🗸] bagaimana jika ada banyak screen size untuk mengetes responsive
- [🗸] bagaimana jika setiap pengambilan screenshot penamaan berdasarkan waktu pengambilan
- [🗸] bagaimana jika url itu dimasukin ke dalam folder dan diklasifikasi berdasarkan waktu
- [🗸] bagaimana jika sebelum mengakses ke website harus dicek dulu apakah website itu aktif atau tidak dan disimpan lognya kedalam satu file
- [🗸] bagaimana jika kita ingin mengetahui berapa lama waktu yang dibutuhkan untuk mengakses dan mengambil screenshot
- [🗸] bagaimana jika ada satu fungsi untuk membersihkan log dan folder
- [🗸] bagaimana jika daftar web itu diimport lewat file json terpisah
- [🗸] bagaimana jika banyaknya screen size itu mengambil screenshot sampai habis fullpage
- [🗸] bagaimana jika semua screenshot di masukan ke dalam satu file pdf atau html untuk laporan

## TO-DO :

- [ ] bagaimana jika halamannya ada loginnya? 
- [ ] bagaimana jika hasil tangkapan otomatis mengirimkan ke instagram atau sosial media lainnya
- [ ] bagaimana jika otomatis berjalan mengecek setiap kali ada perubahan tampilan di website
- [ ] bagaimana jika screenshot otomatis menjadi mockup sesuai dengan device
- [ ] bagaimana jika cli itu ada di extention chrome dengan migrasi ke js
- [ ] bagaimana jika laporannya bisa di custom
- [ ] bagaimana jika screenshotnya otomatis upload ke cloud
- [ ] bagaimana jika semua file yang sudah didapatkan di tampilkan didalam web yang lebih mudah untuk dimanajemen
- [ ] bagaimana jika ukuran tetap asli bawaan perangkat namun dilihat lebih kecil (https://en.wikipedia.org/wiki/Pixel_density)

.....


dari itu semua akhirnya aku dapatkan satu racikan kode.
   
---
   
   
## Apa gunanya?
1. Laporan
2. Mantau
3. Testing

## Instalasi

```
$ pip install --editable .
$ ssind
```

## Inspirasi : 

- [webmobilefirst]
    - Kekurangan 
        - Manual satu persatu
        - Perangkat terbatas dengan fitur berbayar
        - Harus dengan extention chrome
        - Ada iklan
        - Terbatas hanya satu 
    - Kelebihan 
        - Baik untuk simulator
        - Memiliki screencasts (minus .gif)
        - tangkapan screenshot dengan mockup seperti asli


