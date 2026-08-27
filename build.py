#!/usr/bin/env python3
"""
Generates every page of nimbo.mahiruslu.com from one template.

The site is committed as plain HTML so Vercel needs no build step; this script
is the authoring tool. Run it after editing CONTENT, then commit the output.

The Turkish and English versions of a legal page must say the same thing, and
keeping them in one file beside each other is what makes that checkable.

    python3 build.py
"""
import os

OWNER = "Mahir Uslu"
EMAIL = "nimbo@mahiruslu.com"
ORIGIN = "https://nimbo.mahiruslu.com"
UPDATED = {"tr": "27 Ağustos 2026", "en": "27 August 2026"}

# path -> its counterpart in the other language
ALT = {
    "/": "/en", "/en": "/",
    "/gizlilik": "/privacy", "/privacy": "/gizlilik",
    "/kullanim-kosullari": "/terms", "/terms": "/kullanim-kosullari",
    "/destek": "/support", "/support": "/destek",
}
FOOTER = {
    "tr": [("/gizlilik", "Gizlilik"), ("/kullanim-kosullari", "Koşullar"), ("/destek", "Destek")],
    "en": [("/privacy", "Privacy"), ("/terms", "Terms"), ("/support", "Support")],
}


def page(path, lang, title, desc, body):
    other = ALT[path]
    tr_href = path if lang == "tr" else other
    en_href = path if lang == "en" else other
    tr_active = ' aria-current="true"' if lang == "tr" else ""
    en_active = ' aria-current="true"' if lang == "en" else ""
    skip = "İçeriğe geç" if lang == "tr" else "Skip to content"
    lang_label = "Dil" if lang == "tr" else "Language"
    home = "/" if lang == "tr" else "/en"
    links = " ".join(f'<a href="{h}">{t}</a>' for h, t in FOOTER[lang])
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{ORIGIN}{path}">
<link rel="alternate" hreflang="tr" href="{ORIGIN}{tr_href}">
<link rel="alternate" hreflang="en" href="{ORIGIN}{en_href}">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{ORIGIN}{path}">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="site"><div class="bar">
  <a class="home" href="{home}"><img src="/assets/mark.svg" alt="" width="30" height="30"><span class="name">Nimbo</span></a>
  <nav class="lang" aria-label="{lang_label}">
    <a href="{tr_href}"{tr_active} lang="tr">Türkçe</a>
    <a href="{en_href}"{en_active} lang="en">English</a>
  </nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="bar"><div>© 2026 {OWNER}</div><div>{links}</div></div></footer>
</body>
</html>
'''


def write(path, html):
    target = "index.html" if path == "/" else path.strip("/") + "/index.html"
    directory = os.path.dirname(target)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(html)
    print("wrote", target)


# ---------------------------------------------------------------------------
# Privacy policy
# ---------------------------------------------------------------------------

PRIVACY_TR = f'''<h1>Gizlilik Politikası</h1>
<p class="lede">Nimbo hiçbir veri toplamaz. Bu sayfa neyin toplanmadığını tek tek sayar.</p>
<p class="updated">Son güncelleme: {UPDATED["tr"]} · Sürüm 1.0</p>

<div class="card">
  <h2>Kısaca</h2>
  <ul>
    <li>Nimbo sizden veya çocuğunuzdan <strong>hiçbir kişisel bilgi istemez</strong>.</li>
    <li>Hesap, oturum açma veya e-posta adresi gerekmez.</li>
    <li>Reklam ağı, analitik aracı ve çökme raporlama servisi <strong>yoktur</strong>.</li>
    <li>Uygulamanın oluşturduğu her şey <strong>yalnızca cihazda</strong> kalır.</li>
    <li>Uygulamayı silmek, ürettiği tüm veriyi siler.</li>
  </ul>
</div>

<h2>1. Toplanan kişisel veriler</h2>
<p><strong>Hiçbiri.</strong> Nimbo aşağıdakilerin hiçbirini istemez, okumaz veya iletmez:</p>
<ul>
  <li>Ad, soyad, kullanıcı adı</li>
  <li>Doğum tarihi (yalnızca “3–4” veya “5–6” şeklinde bir yaş <em>aralığı</em> seçilir; bu bilgi cihazda kalır ve içerik zorluğunu ayarlamak için kullanılır)</li>
  <li>E-posta adresi, telefon numarası, adres</li>
  <li>Fotoğraf, video, ses kaydı</li>
  <li>Konum bilgisi</li>
  <li>Kişi listesi, takvim, sağlık verisi</li>
  <li>Reklam kimliği (IDFA / GAID), çerez veya takip pikseli</li>
</ul>
<p>Uygulamada <strong>hiçbir metin giriş alanı yoktur</strong>. Çocuğun yazabileceği bir yer
olmadığı için, istemeden kişisel bilgi girmesi de mümkün değildir.</p>

<h2>2. Cihazda saklananlar</h2>
<p>Nimbo aşağıdakileri cihazınızın yerel deposunda tutar. Bunlar cihazdan çıkmaz ve
tarafımızca erişilemez:</p>
<div class="scroll"><table>
  <tr><th>Veri</th><th>Amaç</th></tr>
  <tr><td>Tamamlanan etkinlikler, kazanılan çıkartma ve rozetler</td><td>İlerlemeyi göstermek</td></tr>
  <tr><td>Ekran süresi kayıtları ve günlük limit</td><td>Ebeveyn kontrolleri</td></tr>
  <tr><td>Çizimler ve boyama sayfaları</td><td>Sanat galerisi</td></tr>
  <tr><td>Ses, dil, erişilebilirlik ve uyku ayarları</td><td>Tercihleri hatırlamak</td></tr>
  <tr><td>Seçilen yaş aralığı</td><td>İçerik zorluğunu ayarlamak</td></tr>
  <tr><td>Satın alma durumu</td><td>Tam erişimi açık tutmak</td></tr>
</table></div>
<p>Ebeveyn alanında bir PDF raporu oluşturduğunuzda, rapor cihazın önbelleğinde hazırlanır.
Paylaşmayı siz seçmedikçe cihazdan ayrılmaz; Nimbo hiçbir sunucuya yüklemez. Raporda çocuğun
adı yer almaz, çünkü Nimbo çocuğun adını hiç bilmez.</p>

<h2>3. Ağ trafiği</h2>
<p>Nimbo çevrimdışı çalışır. Uygulamanın kendi başlattığı tek ağ isteği şudur:</p>
<ul>
  <li>Her açılışta <code>{ORIGIN}/config/app-config.json</code> adresine <strong>anonim bir GET</strong>
  isteği. Bu istek yalnızca yapılandırma dosyasını indirir; gövde, başlık veya sorgu parametresi ile
  <strong>hiçbir bilgi göndermez</strong>. Cihaz kimliği, kullanıcı kimliği veya kullanım verisi taşımaz.</li>
</ul>
<p>Bu istek bir bakım duyurusunu veya zorunlu güncelleme bilgisini iletmek içindir. İstek
başarısız olursa uygulama önbellekteki veya uygulamayla birlikte gelen yapılandırmayı kullanır ve
normal şekilde çalışmaya devam eder.</p>

<h2>4. Üçüncü taraf hizmetler</h2>
<p>Nimbo'da <strong>tek bir</strong> üçüncü taraf bileşen vardır:</p>
<h3>RevenueCat (satın alma doğrulama)</h3>
<p>Tam erişim satın alındığında veya “Satın Alımları Geri Yükle” kullanıldığında, satın alma
makbuzunun doğrulanması için RevenueCat, Inc. hizmeti kullanılır. Bu kapsamda:</p>
<ul>
  <li>Nimbo RevenueCat'e <strong>kimlik bilgisi vermez</strong>; anonim bir uygulama kullanıcı kimliği kullanılır.</li>
  <li>Reklam kimliği toplama özelliği <strong>kapalıdır</strong> ve hiçbir zaman çağrılmaz.</li>
  <li>RevenueCat, satın alma doğrulaması için mağazadan gelen makbuz bilgisini ve temel cihaz/ülke
  bilgisini işler. Bu veriler reklam veya takip amacıyla kullanılmaz.</li>
  <li>Ayrıntılar: <a href="https://www.revenuecat.com/privacy" rel="noopener">revenuecat.com/privacy</a></li>
</ul>
<p>Satın alma işleminin kendisi Apple App Store veya Google Play tarafından yürütülür. Ödeme
bilgileriniz mağazada kalır; Nimbo kart bilgisi görmez.</p>
<p>Uygulamada reklam ağı, analitik aracı (Google Analytics, Firebase Analytics vb.), çökme
raporlama servisi veya sosyal medya SDK'sı <strong>bulunmaz</strong>.</p>

<h2>5. Çocuk gizliliği</h2>
<p>Nimbo çocuklara yönelik olarak tasarlanmıştır ve çocuklardan kişisel veri toplamaz.</p>
<ul>
  <li><strong>COPPA</strong> (ABD, 16 CFR Part 312): Nimbo 13 yaş altı çocuklardan kişisel bilgi
  toplamadığı için ebeveyn onayı gerektiren bir veri işleme yapmaz.</li>
  <li><strong>GDPR-K</strong> (AB, Madde 8): Çocuğun kişisel verisi işlenmediğinden, yaşa bağlı
  rıza koşulu doğmaz.</li>
  <li><strong>KVKK</strong> (Türkiye, 6698 sayılı Kanun): Kanun anlamında kişisel veri
  <em>işlenmemektedir</em>; cihazda tutulan ilerleme kayıtları veri sorumlusuna aktarılmaz ve
  tarafımızca erişilebilir değildir.</li>
</ul>
<p>Uygulamada çocuğun başkalarıyla iletişim kurabileceği hiçbir özellik yoktur: sohbet, yorum,
kullanıcı içeriği paylaşımı, sosyal ağ bağlantısı veya harici bağlantı gezintisi bulunmaz.
Uygulamadan dışarı açılan her bağlantı bir yetişkin doğrulamasının arkasındadır.</p>

<h2>6. İzinler</h2>
<div class="scroll"><table>
  <tr><th>İzin</th><th>Neden</th></tr>
  <tr><td>Face ID / Touch ID / parmak izi</td><td>Ebeveyn alanını ve satın alma seçeneklerini korumak. Doğrulamayı işletim sistemi yapar; Nimbo biyometrik veriyi görmez.</td></tr>
  <tr><td>Ses ayarlarını değiştirme (Android)</td><td>Oyun sesleri ve uyku sesleri için ses yönlendirmesi.</td></tr>
</table></div>
<p>Kamera, mikrofon, konum, kişiler, fotoğraflar ve bildirim izinleri <strong>istenmez</strong>.</p>

<h2>7. Verilerin silinmesi</h2>
<p>Sunucularımızda size ait hiçbir veri bulunmadığı için silinmesi gereken bir kayıt yoktur.
Cihazdaki verileri silmek için uygulamayı kaldırmanız yeterlidir; ilerleme, çizimler, ayarlar ve
raporlar cihazla birlikte gider.</p>
<p>Satın alma kaydı mağaza hesabınıza bağlıdır. Uygulamayı silip yeniden kurduğunuzda Ebeveyn
Alanı → Satın Alımlar bölümünden <strong>Satın Alımları Geri Yükle</strong> ile tam erişimi geri
kazanabilirsiniz.</p>

<h2>8. Bu politikadaki değişiklikler</h2>
<p>Politika değişirse bu sayfadaki tarih ve sürüm numarası güncellenir. Uygulamanın veri
davranışını değiştiren bir güncelleme yapılırsa, değişiklik uygulama sürüm notlarında da belirtilir.</p>

<h2>9. İletişim</h2>
<p>Veri sorumlusu: <strong>{OWNER}</strong> (Türkiye)</p>
<p class="contact"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Gizlilikle ilgili sorularınıza en geç 30 gün içinde yanıt verilir.</p>'''

PRIVACY_EN = f'''<h1>Privacy Policy</h1>
<p class="lede">Nimbo collects no data. This page lists, item by item, what is not collected.</p>
<p class="updated">Last updated: {UPDATED["en"]} · Version 1.0</p>

<div class="card">
  <h2>In short</h2>
  <ul>
    <li>Nimbo asks for <strong>no personal information</strong> from you or your child.</li>
    <li>No account, no sign-in, no email address.</li>
    <li>There is <strong>no</strong> ad network, analytics tool, or crash-reporting service.</li>
    <li>Everything the app creates stays <strong>on the device only</strong>.</li>
    <li>Deleting the app deletes all of the data it produced.</li>
  </ul>
</div>

<h2>1. Personal data collected</h2>
<p><strong>None.</strong> Nimbo does not request, read or transmit any of the following:</p>
<ul>
  <li>Name, surname, username</li>
  <li>Date of birth (only an age <em>band</em> — “3–4” or “5–6” — is selected; it stays on the device and is used to set content difficulty)</li>
  <li>Email address, phone number, postal address</li>
  <li>Photos, video, audio recordings</li>
  <li>Location</li>
  <li>Contacts, calendar, health data</li>
  <li>Advertising identifiers (IDFA / GAID), cookies or tracking pixels</li>
</ul>
<p>The app contains <strong>no text input field of any kind</strong>. Because there is nowhere for a
child to type, it is not possible for them to enter personal information by accident.</p>

<h2>2. What is stored on the device</h2>
<p>Nimbo keeps the following in your device's local storage. It never leaves the device and we
cannot access it:</p>
<div class="scroll"><table>
  <tr><th>Data</th><th>Purpose</th></tr>
  <tr><td>Completed activities, earned stickers and badges</td><td>Showing progress</td></tr>
  <tr><td>Screen-time records and the daily limit</td><td>Parental controls</td></tr>
  <tr><td>Drawings and coloring pages</td><td>The art gallery</td></tr>
  <tr><td>Audio, language, accessibility and sleep settings</td><td>Remembering preferences</td></tr>
  <tr><td>Selected age band</td><td>Setting content difficulty</td></tr>
  <tr><td>Purchase state</td><td>Keeping full access unlocked</td></tr>
</table></div>
<p>When you generate a PDF report in the parent area, it is produced in the device's cache. It does
not leave the device unless you choose to share it, and Nimbo never uploads it anywhere. The report
contains no child's name, because Nimbo never knows it.</p>

<h2>3. Network traffic</h2>
<p>Nimbo works offline. The only network request the app makes on its own is:</p>
<ul>
  <li>An <strong>anonymous GET</strong> to <code>{ORIGIN}/config/app-config.json</code> at each
  launch. The request only downloads the configuration file; it <strong>sends no information</strong>
  in a body, header or query parameter. It carries no device identifier, user identifier or usage data.</li>
</ul>
<p>The purpose is to deliver a maintenance notice or a required-update notice. If the request fails,
the app uses its cached or bundled configuration and continues to work normally.</p>

<h2>4. Third-party services</h2>
<p>Nimbo contains exactly <strong>one</strong> third-party component:</p>
<h3>RevenueCat (purchase validation)</h3>
<p>When full access is purchased, or “Restore Purchases” is used, RevenueCat, Inc. validates the
purchase receipt. In that process:</p>
<ul>
  <li>Nimbo provides <strong>no identity information</strong> to RevenueCat; an anonymous app user ID is used.</li>
  <li>Advertising-identifier collection is <strong>disabled</strong> and is never called.</li>
  <li>RevenueCat processes the store receipt and basic device/country information in order to validate
  the purchase. This data is not used for advertising or tracking.</li>
  <li>Details: <a href="https://www.revenuecat.com/privacy" rel="noopener">revenuecat.com/privacy</a></li>
</ul>
<p>The purchase itself is carried out by the Apple App Store or Google Play. Your payment details stay
with the store; Nimbo never sees card information.</p>
<p>The app contains <strong>no</strong> ad network, analytics tool (Google Analytics, Firebase
Analytics and similar), crash-reporting service or social media SDK.</p>

<h2>5. Children's privacy</h2>
<p>Nimbo is designed for children and collects no personal data from them.</p>
<ul>
  <li><strong>COPPA</strong> (US, 16 CFR Part 312): because Nimbo collects no personal information
  from children under 13, it performs no processing that would require verifiable parental consent.</li>
  <li><strong>GDPR-K</strong> (EU, Article 8): as no personal data of a child is processed, the
  age-related consent condition does not arise.</li>
  <li><strong>KVKK</strong> (Türkiye, Law No. 6698): no personal data is <em>processed</em> within the
  meaning of the law; progress records held on the device are not transferred to the data controller
  and are not accessible to us.</li>
</ul>
<p>The app has no feature that lets a child communicate with anyone: no chat, comments, user-content
sharing, social network connection or web browsing. Every link that leaves the app sits behind an
adult verification step.</p>

<h2>6. Permissions</h2>
<div class="scroll"><table>
  <tr><th>Permission</th><th>Why</th></tr>
  <tr><td>Face ID / Touch ID / fingerprint</td><td>To protect the parent area and purchase options. Verification is handled by the operating system; Nimbo never sees biometric data.</td></tr>
  <tr><td>Modify audio settings (Android)</td><td>Audio routing for game sounds and sleep sounds.</td></tr>
</table></div>
<p>Camera, microphone, location, contacts, photos and notification permissions are
<strong>never requested</strong>.</p>

<h2>7. Deleting data</h2>
<p>Because we hold no data about you on any server, there is no record to delete. To remove the data
on the device, simply uninstall the app; progress, drawings, settings and reports go with it.</p>
<p>Your purchase is tied to your store account. If you delete and reinstall the app, you can recover
full access from Parent Area → Purchases with <strong>Restore Purchases</strong>.</p>

<h2>8. Changes to this policy</h2>
<p>If this policy changes, the date and version number on this page are updated. If an update changes
the app's data behaviour, the change is also noted in the app's release notes.</p>

<h2>9. Contact</h2>
<p>Data controller: <strong>{OWNER}</strong> (Türkiye)</p>
<p class="contact"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Privacy questions are answered within 30 days at the latest.</p>'''


# ---------------------------------------------------------------------------
# Terms of use
# ---------------------------------------------------------------------------

TERMS_TR = f'''<h1>Kullanım Koşulları</h1>
<p class="lede">Nimbo'yu indirerek veya kullanarak bu koşulları kabul etmiş olursunuz.</p>
<p class="updated">Son güncelleme: {UPDATED["tr"]} · Sürüm 1.0</p>

<h2>1. Lisans</h2>
<p>Nimbo, {OWNER} tarafından geliştirilen bir mobil uygulamadır. Uygulamayı kişisel ve ticari
olmayan amaçlarla, sahibi olduğunuz cihazlarda kullanmanız için size devredilemez ve münhasır
olmayan bir lisans verilir.</p>
<p>Uygulamayı kopyalayamaz, kaynak koduna dönüştüremez, değiştiremez, kiralayamaz, satamaz veya
içeriğini ayrı bir ürün olarak dağıtamazsınız. Uygulamadaki tüm metin, görsel, ses ve yazılım
üzerindeki haklar saklıdır.</p>
<p>iOS'ta uygulama ayrıca Apple'ın Lisanslı Uygulama Son Kullanıcı Lisans Sözleşmesi'ne
(Standard EULA) tabidir.</p>

<h2>2. Satın alma ve iade</h2>
<ul>
  <li>Nimbo'nun bir bölümü ücretsizdir. <strong>Tam erişim</strong> tek seferlik bir satın almadır;
  abonelik değildir ve yenilenmez.</li>
  <li>Satın alma işlemi Apple App Store veya Google Play üzerinden yürütülür. Ödeme, faturalandırma
  ve iade işlemleri ilgili mağazanın kurallarına tabidir.</li>
  <li>İade talepleri doğrudan mağazaya iletilir: iOS için
  <a href="https://reportaproblem.apple.com" rel="noopener">reportaproblem.apple.com</a>,
  Android için Google Play sipariş geçmişi.</li>
  <li>Satın alma, mağaza hesabınıza bağlıdır. Aynı hesapla giriş yaptığınız cihazlarda
  <strong>Satın Alımları Geri Yükle</strong> ile açabilirsiniz.</li>
</ul>

<h2>3. Uygun kullanım</h2>
<p>Uygulamayı yasalara aykırı bir amaçla veya uygulamanın çalışmasını engelleyecek şekilde
kullanamazsınız. Satın alma korumalarını veya ebeveyn doğrulamasını atlatmaya yönelik girişimler
lisansın sona ermesine yol açar.</p>

<h2>4. Çocukların kullanımı</h2>
<p>Nimbo çocuklar için tasarlanmıştır ancak sözleşme ehliyeti olan bir yetişkinin sorumluluğu
altında kullanılmalıdır. Ebeveyn alanına ve satın alma seçeneklerine erişim cihazın kendi kilidiyle
korunur; cihazın kilidini paylaştığınız kişiler bu alanlara erişebilir.</p>

<h2>5. Garanti reddi</h2>
<p>Uygulama “olduğu gibi” sunulur. Kesintisiz veya hatasız çalışacağı garanti edilmez. Nimbo bir
eğitim aracıdır; pedagojik, tıbbi veya gelişimsel bir teşhis veya tavsiye niteliği taşımaz.</p>

<h2>6. Sorumluluk sınırı</h2>
<p>Yürürlükteki hukukun izin verdiği azami ölçüde, uygulamanın kullanımından doğan dolaylı,
arızi veya sonuç niteliğindeki zararlardan sorumluluk kabul edilmez. Her hâlükârda toplam
sorumluluk, uygulama için ödediğiniz tutarla sınırlıdır.</p>

<h2>7. Değişiklikler</h2>
<p>Bu koşullar güncellenebilir. Değişiklikler bu sayfada yayımlandığı tarihte yürürlüğe girer;
sayfanın üstündeki tarih ve sürüm numarası güncellenir.</p>

<h2>8. Geçerli hukuk</h2>
<p>Bu koşullar Türkiye Cumhuriyeti hukukuna tabidir. Uyuşmazlıklarda İstanbul mahkemeleri ve icra
daireleri yetkilidir. Bulunduğunuz ülkedeki tüketici mevzuatının size tanıdığı zorunlu haklar
saklıdır.</p>

<h2>9. İletişim</h2>
<p class="contact"><a href="mailto:{EMAIL}">{EMAIL}</a></p>'''

TERMS_EN = f'''<h1>Terms of Use</h1>
<p class="lede">By downloading or using Nimbo you accept these terms.</p>
<p class="updated">Last updated: {UPDATED["en"]} · Version 1.0</p>

<h2>1. Licence</h2>
<p>Nimbo is a mobile application developed by {OWNER}. You are granted a non-transferable,
non-exclusive licence to use the app for personal, non-commercial purposes on devices you own.</p>
<p>You may not copy, reverse-engineer, modify, rent, sell or redistribute the app or its content as a
separate product. All rights in the text, artwork, audio and software of the app are reserved.</p>
<p>On iOS the app is additionally subject to Apple's Licensed Application End User Licence Agreement
(the Standard EULA).</p>

<h2>2. Purchases and refunds</h2>
<ul>
  <li>Part of Nimbo is free. <strong>Full access</strong> is a one-time purchase; it is not a
  subscription and does not renew.</li>
  <li>Purchases are processed by the Apple App Store or Google Play. Payment, billing and refunds are
  governed by that store's rules.</li>
  <li>Refund requests go directly to the store: for iOS,
  <a href="https://reportaproblem.apple.com" rel="noopener">reportaproblem.apple.com</a>;
  for Android, your Google Play order history.</li>
  <li>A purchase is tied to your store account. On any device signed in with that account you can
  unlock it with <strong>Restore Purchases</strong>.</li>
</ul>

<h2>3. Acceptable use</h2>
<p>You may not use the app for any unlawful purpose or in a way that interferes with its operation.
Attempts to bypass purchase protection or parental verification terminate the licence.</p>

<h2>4. Use by children</h2>
<p>Nimbo is designed for children but must be used under the responsibility of an adult with legal
capacity to contract. Access to the parent area and purchase options is protected by the device's own
lock; anyone you share that lock with can reach those areas.</p>

<h2>5. Disclaimer of warranties</h2>
<p>The app is provided “as is”. It is not warranted to operate uninterrupted or error-free. Nimbo is
an educational tool; it is not a pedagogical, medical or developmental diagnosis or advice.</p>

<h2>6. Limitation of liability</h2>
<p>To the maximum extent permitted by applicable law, no liability is accepted for indirect,
incidental or consequential damages arising from use of the app. In any event total liability is
limited to the amount you paid for the app.</p>

<h2>7. Changes</h2>
<p>These terms may be updated. Changes take effect on the date they are published on this page, and
the date and version number at the top are updated.</p>

<h2>8. Governing law</h2>
<p>These terms are governed by the laws of the Republic of Türkiye. The courts and enforcement
offices of Istanbul have jurisdiction. Mandatory consumer rights available to you in your country of
residence are unaffected.</p>

<h2>9. Contact</h2>
<p class="contact"><a href="mailto:{EMAIL}">{EMAIL}</a></p>'''


# ---------------------------------------------------------------------------
# Support
# ---------------------------------------------------------------------------

SUPPORT_TR = f'''<h1>Destek</h1>
<p class="lede">Sorunuz mu var? Yazın — en geç iki iş günü içinde yanıt veriyoruz.</p>
<p class="contact"><a href="mailto:{EMAIL}">{EMAIL}</a></p>

<h2>Sık sorulanlar</h2>

<h3>Ebeveyn alanına nasıl girerim?</h3>
<p>Çocuk ana ekranındaki ayarlar düğmesine dokunun. Cihazınızın Face ID, Touch ID, parmak izi veya
ekran kilidi parolasıyla doğrulama istenir. Cihazınızda ekran kilidi tanımlı değilse yerine bir
yetişkin sorusu (çarpma işlemi) sorulur.</p>

<h3>Hangi bölümler ücretsiz?</h3>
<p>203 etkinliğin 97'si ücretsizdir. Sanat Atölyesi'nin tamamı (52 etkinlik) ücretsizdir; Matematik,
Türkçe, Dikkat, Uyku ve Robot bölümlerinin bir kısmı ücretsiz, kalanı tam erişimle açılır.</p>

<h3>Tam erişim nedir?</h3>
<p>Tek seferlik bir satın almadır — abonelik değildir, yenilenmez. Tüm bölümlerdeki 203 etkinliğin
tamamını açar. Satın alma, ebeveyn doğrulamasının arkasındadır ve satın alma anında ikinci kez
doğrulama istenir.</p>

<h3>Satın alımımı nasıl geri yüklerim?</h3>
<p>Ebeveyn Alanı → Ayarlar → Satın Alımlar → <strong>Satın Alımları Geri Yükle</strong>. Mağaza
hesabınızla giriş yapmış olmanız yeterlidir; yeniden ödeme alınmaz.</p>

<h3>Yeni bir cihaza geçtim, ilerlemem gitti.</h3>
<p>İlerleme, çizimler ve ayarlar yalnızca cihazda tutulur ve cihazlar arasında senkronize edilmez —
bu, hiçbir veri toplamamanın doğal sonucudur. Satın alma kaydınız mağaza hesabınıza bağlı olduğu için
<strong>Satın Alımları Geri Yükle</strong> ile geri gelir.</p>

<h3>Ekran süresi limitini nasıl ayarlarım?</h3>
<p>Ebeveyn Alanı → Ayarlar → Genel bölümünden günlük limiti belirleyebilirsiniz. Limit dolduğunda
çocuk bir bekleme ekranı görür; bir yetişkin düğmeyi 3 saniye basılı tutarak 15 dakika ekleyebilir.</p>

<h3>Dili nasıl değiştiririm?</h3>
<p>Ebeveyn Alanı → Ayarlar → Genel → Dil. Türkçe ve İngilizce desteklenir; seslendirmeler de seçilen
dile göre değişir.</p>

<h3>Verilerimi nasıl silerim?</h3>
<p>Uygulamayı kaldırmanız yeterlidir. Sunucularımızda size ait hiçbir veri bulunmadığı için silinmesi
gereken başka bir kayıt yoktur. Ayrıntı için <a href="/gizlilik">Gizlilik Politikası</a>.</p>

<h3>İnternet olmadan çalışır mı?</h3>
<p>Evet. Tüm etkinlikler, sesler ve oyunlar çevrimdışı çalışır.</p>

<h3>Reklam var mı?</h3>
<p>Hayır. Reklam ağı, sponsorlu içerik veya çocuğu satın almaya yönelten reklam alanı bulunmaz.</p>

<hr>
<p>Yanıt bulamadığınız bir soru için: <a href="mailto:{EMAIL}">{EMAIL}</a>. Yazarken cihaz modelinizi
ve işletim sistemi sürümünüzü eklerseniz daha hızlı yardımcı olabiliriz.</p>'''

SUPPORT_EN = f'''<h1>Support</h1>
<p class="lede">Have a question? Write to us — we reply within two working days.</p>
<p class="contact"><a href="mailto:{EMAIL}">{EMAIL}</a></p>

<h2>Frequently asked</h2>

<h3>How do I open the parent area?</h3>
<p>Tap the settings button on the child home screen. You will be asked to verify with your device's
Face ID, Touch ID, fingerprint or screen-lock passcode. If your device has no screen lock, an adult
question (a multiplication) is asked instead.</p>

<h3>Which parts are free?</h3>
<p>97 of the 203 activities are free. The whole Art Studio (52 activities) is free; the numeracy,
language, attention, sleep and robot sections have some free activities, with the rest unlocked by
full access.</p>

<h3>What is full access?</h3>
<p>A one-time purchase — not a subscription, and it does not renew. It unlocks all 203 activities
across every section. The purchase sits behind parental verification, and a second verification is
requested at the moment of purchase.</p>

<h3>How do I restore my purchase?</h3>
<p>Parent Area → Settings → Purchases → <strong>Restore Purchases</strong>. You only need to be signed
in with your store account; you are not charged again.</p>

<h3>I moved to a new device and my progress is gone.</h3>
<p>Progress, drawings and settings are kept only on the device and are not synchronised between
devices — that is the natural consequence of collecting no data. Your purchase is tied to your store
account, so <strong>Restore Purchases</strong> brings it back.</p>

<h3>How do I set the screen-time limit?</h3>
<p>Parent Area → Settings → General lets you set a daily limit. When it is reached the child sees a
resting screen; an adult can add 15 minutes by holding a button for 3 seconds.</p>

<h3>How do I change the language?</h3>
<p>Parent Area → Settings → General → Language. Turkish and English are supported, and the spoken
audio follows the selected language.</p>

<h3>How do I delete my data?</h3>
<p>Simply uninstall the app. Because we hold no data about you on any server, there is no other record
to delete. See the <a href="/privacy">Privacy Policy</a> for details.</p>

<h3>Does it work without internet?</h3>
<p>Yes. Every activity, sound and game works offline.</p>

<h3>Are there ads?</h3>
<p>No. There are no ad networks, sponsored content or ad placements pushing a child toward a purchase.</p>

<hr>
<p>For anything not answered here: <a href="mailto:{EMAIL}">{EMAIL}</a>. Including your device model
and operating system version helps us help you faster.</p>'''


# ---------------------------------------------------------------------------
# Landing
# ---------------------------------------------------------------------------

LANDING_TR = f'''<div class="hero">
  <img src="/assets/icon.svg" alt="Nimbo uygulama simgesi" width="88" height="88">
  <div><h1>Nimbo</h1><p class="lede">3–6 yaş için reklamsız, takipsiz bir öğrenme dünyası.</p></div>
</div>

<p>Nimbo; matematik, Türkçe, dikkat, sanat, robotik ve uyku rutini olmak üzere altı bölümde
<strong>203 etkinlik</strong> sunar. Tamamı Türkçe ve İngilizce seslendirilmiştir ve internet
bağlantısı olmadan çalışır.</p>

<div class="card">
  <h2>Nimbo'nun sözü</h2>
  <ul class="promise">
    <li><span class="tick">✓</span><div><strong>Reklam yok</strong><span class="sub">Reklam ağı, sponsorlu içerik veya çocuğu satın almaya yönelten reklam alanı bulunmaz.</span></div></li>
    <li><span class="tick">✓</span><div><strong>Takip yok</strong><span class="sub">Analitik profili, davranışsal izleme, üçüncü taraf takip pikseli veya reklam kimliği kullanılmaz.</span></div></li>
    <li><span class="tick">✓</span><div><strong>Veriler cihazda</strong><span class="sub">İlerleme, ekran süresi, çizimler, ayarlar ve ebeveyn raporları yalnızca cihazda tutulur.</span></div></li>
    <li><span class="tick">✓</span><div><strong>Çocuk hesabı yok</strong><span class="sub">Oturum açma, profil oluşturma veya e-posta verme gerekmez.</span></div></li>
    <li><span class="tick">✓</span><div><strong>İnternet gerekmez</strong><span class="sub">Etkinliklerin tamamı çevrimdışı çalışır.</span></div></li>
    <li><span class="tick">✓</span><div><strong>Abonelik yok</strong><span class="sub">Tam erişim tek seferlik bir satın almadır.</span></div></li>
  </ul>
</div>

<h2>Ebeveyn alanı</h2>
<p>Ebeveyn alanı, satın alma seçenekleri ve gizlilik ekranı cihazın kendi kilidiyle (Face ID,
Touch ID, parmak izi veya ekran kilidi parolası) korunur. Doğrulamayı işletim sistemi yapar; Nimbo
biyometrik verinizi veya cihaz parolanızı görmez ve saklamaz. Cihazda ekran kilidi tanımlı değilse
yerine bir yetişkin sorusu sorulur.</p>
<p>Ebeveyn alanında ekran süresi limiti, bölüm bazlı içerik kontrolü, ilerleme istatistikleri ve
cihazda oluşturulan PDF raporları bulunur.</p>

<h2>Belgeler</h2>
<div class="scroll"><table>
  <tr><th>Belge</th><th>Bağlantı</th></tr>
  <tr><td>Gizlilik Politikası</td><td><a href="/gizlilik">nimbo.mahiruslu.com/gizlilik</a></td></tr>
  <tr><td>Kullanım Koşulları</td><td><a href="/kullanim-kosullari">nimbo.mahiruslu.com/kullanim-kosullari</a></td></tr>
  <tr><td>Destek</td><td><a href="/destek">nimbo.mahiruslu.com/destek</a></td></tr>
</table></div>

<p class="contact">İletişim: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''

LANDING_EN = f'''<div class="hero">
  <img src="/assets/icon.svg" alt="Nimbo app icon" width="88" height="88">
  <div><h1>Nimbo</h1><p class="lede">An ad-free, tracking-free learning world for ages 3–6.</p></div>
</div>

<p>Nimbo offers <strong>203 activities</strong> across six areas: numeracy, language, attention, art,
robotics and a bedtime routine. Every activity is voiced in both Turkish and English, and the whole
app works without an internet connection.</p>

<div class="card">
  <h2>The Nimbo promise</h2>
  <ul class="promise">
    <li><span class="tick">✓</span><div><strong>No ads</strong><span class="sub">No ad networks, sponsored content, or ad placements that push a child toward a purchase.</span></div></li>
    <li><span class="tick">✓</span><div><strong>No tracking</strong><span class="sub">No analytics profiles, behavioural tracking, third-party pixels, or advertising identifiers.</span></div></li>
    <li><span class="tick">✓</span><div><strong>Data stays on the device</strong><span class="sub">Progress, screen time, drawings, settings and parent reports are kept only on this device.</span></div></li>
    <li><span class="tick">✓</span><div><strong>No child account</strong><span class="sub">No sign-in, no profile, no email address.</span></div></li>
    <li><span class="tick">✓</span><div><strong>No internet needed</strong><span class="sub">Every activity works offline.</span></div></li>
    <li><span class="tick">✓</span><div><strong>No subscription</strong><span class="sub">Full access is a single one-time purchase.</span></div></li>
  </ul>
</div>

<h2>Parent area</h2>
<p>The parent area, purchase options and privacy screen are protected by the device's own lock
(Face ID, Touch ID, fingerprint or screen-lock passcode). Verification is handled by the operating
system; Nimbo never sees or stores your biometric data or device passcode. If the device has no
screen lock, an adult question is asked instead.</p>
<p>The parent area holds a screen-time limit, per-module content controls, progress statistics and
PDF reports generated on the device.</p>

<h2>Documents</h2>
<div class="scroll"><table>
  <tr><th>Document</th><th>Link</th></tr>
  <tr><td>Privacy Policy</td><td><a href="/privacy">nimbo.mahiruslu.com/privacy</a></td></tr>
  <tr><td>Terms of Use</td><td><a href="/terms">nimbo.mahiruslu.com/terms</a></td></tr>
  <tr><td>Support</td><td><a href="/support">nimbo.mahiruslu.com/support</a></td></tr>
</table></div>

<p class="contact">Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'''


PAGES = [
    ("/", "tr", "Nimbo — Çocuklar için reklamsız öğrenme uygulaması",
     "Nimbo, 3–6 yaş için 203 etkinlik içeren, reklamsız ve takipsiz bir öğrenme uygulaması. Tüm veriler cihazda kalır.", LANDING_TR),
    ("/en", "en", "Nimbo — An ad-free learning app for children",
     "Nimbo is an ad-free, tracking-free learning app for ages 3–6 with 203 activities. All data stays on the device.", LANDING_EN),
    ("/gizlilik", "tr", "Gizlilik Politikası — Nimbo",
     "Nimbo hiçbir kişisel veri toplamaz. Reklam, analitik ve takip yoktur; tüm veriler cihazda kalır.", PRIVACY_TR),
    ("/privacy", "en", "Privacy Policy — Nimbo",
     "Nimbo collects no personal data. No ads, no analytics, no tracking; everything stays on the device.", PRIVACY_EN),
    ("/kullanim-kosullari", "tr", "Kullanım Koşulları — Nimbo",
     "Nimbo kullanım koşulları: lisans, tek seferlik satın alma, iade, sorumluluk ve geçerli hukuk.", TERMS_TR),
    ("/terms", "en", "Terms of Use — Nimbo",
     "Nimbo terms of use: licence, one-time purchase, refunds, liability and governing law.", TERMS_EN),
    ("/destek", "tr", "Destek — Nimbo",
     "Nimbo destek ve sık sorulan sorular: ebeveyn alanı, satın alma geri yükleme, ekran süresi, dil.", SUPPORT_TR),
    ("/support", "en", "Support — Nimbo",
     "Nimbo support and FAQ: parent area, restoring purchases, screen time, language.", SUPPORT_EN),
]


def main():
    for path, lang, title, desc, body in PAGES:
        write(path, page(path, lang, title, desc, body))
    # No trailing slash: vercel.json sets trailingSlash false, and these must
    # match the <link rel="canonical"> on each page.
    urls = "".join(f"  <url><loc>{ORIGIN}{p}</loc></url>\n" for p, *_ in PAGES)
    with open("sitemap.xml", "w", encoding="utf-8") as handle:
        handle.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    print("wrote sitemap.xml")
    with open("robots.txt", "w", encoding="utf-8") as handle:
        handle.write(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    print("wrote robots.txt")


if __name__ == "__main__":
    main()
