import sqlite3
con=sqlite3.connect('ruyalar.db')
cursor=con.cursor()

def tabloolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS ruyalar (kullaniciadi TEXT, tarih TEXT, metin TEXT)")
    con.commit()
tabloolustur()

def tabirlistolustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS tabirler (kelime TEXT PRIMARY KEY, anlam TEXT NOT NULL)")
    con.commit()


def ruyaekle(kullaniciadi):
    tarih=input("tarih (gg.aa.yy): ")
    metin=input("rüya : ")
    cursor.execute("INSERT INTO ruyalar (kullaniciadi,tarih, metin) VALUES (?,?,?)", (kullaniciadi, tarih, metin))
    con.commit()
    print("rüyanız kaydedildi.")

    with open(f"{kullaniciadi}_ruyalar.txt", "a", encoding="utf-8") as dosya:
        dosya.write(f"Tarih: {tarih} | Rüya: {metin}\n")


def ruyagoster(kullaniciadi):
    cursor.execute("SELECT tarih, metin FROM ruyalar WHERE kullaniciadi=?", (kullaniciadi,))
    ruyalar=cursor.fetchall()
    if not ruyalar:
        print("kaydedilmiş rüyanız bulunmamaktadır.")
    else:
        print(f"{kullaniciadi} adlı kullanıcının rüyaları:")
        with open(f"{kullaniciadi}_ruyalar.txt", "w", encoding="utf-8") as dosya:
            for tarih, metin in ruyalar:
                satir = f"Tarih: {tarih} ---> Rüya: {metin}"
                print(satir)
                dosya.write(satir + "\n")
        print(f"Tüm rüyalar '{kullaniciadi}_ruyalar.txt' dosyasına kaydedildi.")


def tabiranaliz(metin):
    kelimeler= metin.lower().split()
    bulunantabirler=[]

    for kelime in kelimeler:
        cursor.execute("SELECT anlam FROM tabirler WHERE kelime=?", (kelime,))
        sonuc = cursor.fetchone()
        if sonuc:
            bulunantabirler.append((kelime, sonuc[0]))
    return(bulunantabirler)


def tabiranaliz_ve_yaz(metinler, kullaniciadi):
    yorumlar = []
    with open(f"{kullaniciadi}_tabirler.txt", "w", encoding="utf-8") as dosya:
        for metin in metinler:
            analiz = tabiranaliz(metin)
            if analiz:
                for kelime, anlam in analiz:
                    satir = f"{kelime}: {anlam}"
                    print(satir)
                    dosya.write(satir + "\n")
                    yorumlar.append(satir)
            else:
                uyarı = "eşleşen anlam yok. lütfen rüyanızı yazarken anahtar kelimeleri kullanmakta özen gösteriniz."
                print(uyarı)
                dosya.write(uyarı + "\n")
    print(f"Tabir analizleri '{kullaniciadi}_tabirler.txt' dosyasına kaydedildi.")


def tabiryukle():
    tabirlist={
        "su": "Temizlik, arınma ve huzur anlamına gelir.",
        "ateş": "Tutku, öfke veya tehlike işaretidir.",
        "yılan": "Gizli düşman, korku ya da ihanet anlamına gelir.",
        "uçmak": "Özgürlük, yükselme veya manevi rahatlık.",
        "karanlık": "Belirsizlik, korku ya da içe kapanıklık.",
        "ışık": "Aydınlanma, umut ve çözüm bulma.",
        "ölüm": "Yenilenme, bir dönemin bitişi.",
        "bebek": "Yeni başlangıç, masumiyet veya sorumluluk.",
        "kan": "Hayat gücü, öfke veya kayıp.",
        "diş": "Korku, yaşlılık veya kontrol kaybı.",
        "düşmek": "Başarısızlık korkusu veya yetersizlik.",
        "yüzmek": "Duygularla başa çıkma, akışta kalma.",
        "deniz": "Duyguların derinliği, bilinçaltı.",
        "rüzgar": "Değişim, yönsüzlük veya haber.",
        "ağaç": "Büyüme, köklenme veya aile bağları.",
        "kapı": "Yeni fırsatlar veya geçiş dönemleri.",
        "ayna": "Kendini tanıma, iç hesaplaşma.",
        "ev": "Benlik, iç dünya veya güvenlik.",
        "yol": "Hayat yolu, kararlar ve yön değişimi.",
        "uçurum": "Tehlike, belirsizlik veya risk.",
        "koşmak": "Kaçış, hedefe ulaşma arzusu.",
        "yağmur": "Arınma, bereket veya duygusal boşalma.",
        "kar": "Soğukluk, duygusal mesafe veya arınma.",
        "gölge": "Bilinçaltı korkular, bastırılmış yönler.",
        "zincir": "Bağlılık, engel veya sorumluluk.",
        "ceviz": "Zeka, sabır ve içsel bilgi.",
        "yorgan": "Korunma, mahremiyet veya tembellik.",
        "aslan": "Güç, cesaret veya liderlik.",
        "kedi": "Bağımsızlık, kadınsılık veya şüphe.",
        "köpek": "Sadakat, dostluk veya koruma.",
        "çocuk": "Masumiyet, yeni başlangıçlar.",
        "uçak": "Hedeflere ulaşma arzusu, yüksek beklentiler.",
        "merdiven": "Yükselme veya düşme korkusu.",
        "araba": "Kontrol, yön belirleme veya özgürlük.",
        "okul": "Öğrenme, gelişim veya sınanma.",
        "cam": "Kırılganlık, saydamlık veya savunmasızlık.",
        "ayna": "Kendini tanıma veya iç hesaplaşma.",
        "para": "Değer, kaygı veya fırsat.",
        "elma": "Arzu, sağlık veya günah.",
        "ekmek": "Geçim, bereket ve temel ihtiyaçlar.",
        "çiçek": "Güzellik, aşk veya geçicilik.",
        "kırmızı": "Tutku, tehlike veya enerji.",
        "beyaz": "Temizlik, saflık veya teslimiyet.",
        "siyah": "Gizem, korku veya bilinçaltı.",
        "ölü": "Geçmişle yüzleşme, kapanış.",
        "polis": "Kural, otorite veya baskı.",
        "sınav": "Kaygı, değerlendirme veya hazırlık.",
        "tren": "Yolculuk, fırsat veya kaçırılmış şans.",
        "orman": "Kayıp, keşif veya gizem.",
        "kuş": "Özgürlük, haber veya ruhsal yön.",
        "balık": "Bolluk, bilinçaltı veya spiritüel mesaj.",
        "dağ": "Zorluk, hedef veya dayanıklılık.",
        "telefon": "İletişim, özlem veya haberleşme.",
        "kitap": "Bilgi, sırlar veya öğrenme arzusu.",
        "çorap": "Gizlilik, temizlik veya önemsiz detaylar.",
        "göz": "Algı, dikkat veya ruhsal bakış.",
        "eller": "Eylem, yardım veya ilişki.",
        "ay": "Duygular, kadınsı enerji veya döngüler.",
        "güneş": "Hayat enerjisi, netlik veya umut.",
        "kale": "Güvenlik, savunma veya yalnızlık.",
        "kurbağa": "Dönüşüm, sürpriz veya şaşkınlık.",
        "uçurtma": "Hayal, özgürlük veya denetim kaybı.",
        "bıçak": "Tehlike, karar veya zarar.",
        "çanta": "Yük, sorumluluk veya sır.",
        "anahtar": "Çözüm, giriş veya kontrol.",
        "sandalye": "Durum, konum veya rahatlama.",
        "halı": "Gizleme, lüks veya rahatlık.",
        "kuşak": "Bağ, gelenek veya koruma.",
        "karınca": "Çalışkanlık, sabır veya küçük sorunlar.",
        "örümcek": "Yaratıcılık, tuzak veya korku.",
        "ayna": "Kendine bakış, içsel yüzleşme.",
        "kedi": "Bağımsızlık veya gizemli durum.",
        "yağ": "Kayganlık, bolluk veya kaygı.",
        "gemi": "Yolculuk, uzaklaşma veya değişim.",
        "fırtına": "Çatışma, stres veya ani değişim.",
        "yorgan": "Örtme, koruma veya içe çekilme.",
        "bahçe": "Huzur, gelişim veya gizli duygular.",
        "çizme": "Hazırlık, koruma veya uzun yolculuk.",
        "düğün": "Birleşme, değişim veya kutlama.",
        "cenaze": "Veda, kabullenme veya değişim.",
        "hırsız": "Kayıp, korku veya tehdit.",
        "kaplumbağa": "Yavaşlık, sabır veya korunma.",
        "boşluk": "Eksiklik, arayış veya yalnızlık.",
        "ayna": "Kendini değerlendirme ve yüzleşme.",
        "otobüs": "Toplu yolculuk, hayat rotası.",
        "bavul": "Taşınma, geçmişle bağ veya hazırlık.",
        "kule": "Yalnızlık, güç veya düşüş riski.",
        "gözlük": "Gerçeği görme, netlik arayışı.",
        "battaniye": "Rahatlık, sıcaklık ve korunma.",
        "lavabo": "Arınma, temizlik veya yük boşaltma.",
        "ayakkabı": "Yolculuk, statü veya ilerleme.",
        "çöp": "İstenmeyen duygular veya geçmiş.",
        "yorgan": "İçe kapanma, korunma arzusu.",
        "kayık": "Duygusal geçiş veya yalnızlık.",
        "tren": "Fırsat, planlı ilerleyiş veya karar.",
        "mezar": "Geçmişi gömme, bitiş veya korku.",
        "kalem": "İfade, iletişim veya düşünce.",
        "kitap": "Bilgi, sırlar veya rehberlik.",
        "lamba": "Fikir, aydınlanma veya uyarı.",
        "yatak": "Rahatlama, mahremiyet veya dinlenme.",
        "çay": "Sohbet, huzur veya alışkanlık.",
        "bal": "Tatlılık, bolluk veya çekicilik."
    }
    for kelime,anlam in tabirlist.items():
        cursor.execute("INSERT OR IGNORE INTO tabirler (kelime, anlam) VALUES(?,?)", (kelime, anlam))
    con.commit()


tabirlistolustur()
tabiryukle()

giris=int(input("yönetici girisi icin 1,kullanici girisi icin 2 ye basınız."))

if giris==1:
    print("yönetici girisini sectiniz.kullanici adi kismina 'yönetici' yazınız.")
else:
    print("kullanici girisi sectiniz.")

kullaniciadi=input("kullanıcı adı:")
sifre=int(input("sifre giriniz. (sadece sayı!!):"))

if kullaniciadi=="yönetici" and sifre==123456:
    print("yönetici girisi yaptiniz. kullanicilari yonetme ve rüya tabirlerini düzenleme yetkisine sahipsiniz.")
elif kullaniciadi=="yönetici" and sifre!=123456:
    while(True):
        print("Tekrar deneyiniz.")
        sifre=int(input("sifre giriniz(sadece sayı!!):"))
        if sifre ==123456:
            print("yönetici girisi yaptiniz. kullanicilari yonetme ve rüya tabirlerini düzenleme yetkisine sahipsiniz.")
            break
else:
    print("kullanici girisi yaptiniz, sisteme yonlendiriliyorsunuz.")
while True:
    menu=int(input("istediğiniz uygulamayı seçiniz.\n 1.yeni rüya girişi \n 2.rüyalarımı görüntüle \n 3.rüya tabirlerini görüntüle \n 4.çıkış\n"))
    if menu==1:
        ruyaekle(kullaniciadi)
    elif menu==2:
        ruyagoster(kullaniciadi)
    elif menu == 3:
        cursor.execute("SELECT metin FROM ruyalar WHERE kullaniciadi=?", (kullaniciadi,))
        ruyalar = cursor.fetchall()

        if not ruyalar:
            print("Kaydedilmiş rüyanız bulunmamaktadır.")
        else:
            print("Rüyanızda bulunan kelimelerin anlamları:")
            tabiranaliz_ve_yaz([r[0] for r in ruyalar], kullaniciadi)

    elif menu==4:
        print("programdan cıkılıyor..")
        break
    else:
        print("gecersiz secim!!!")
