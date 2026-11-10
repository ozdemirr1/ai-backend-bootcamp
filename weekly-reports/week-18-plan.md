# Week 18 plan — Compose ve izole veritabanı CI

10–16 Kasım 2026. Planlama durumu: uygulanmadı. [Ay 5 sözleşmesi](../monthly-plans/month-05.md) kapsam ve güvenlik sınırlarında esas kaynaktır.

## 10 Kasım hazırlık kararı — henüz uygulama değil

Week 17 kapanış doğrulaması 10 Kasım'a taşındı. Bugün mevcut guard/config/migration
kodları incelendi; servis, volume, veritabanı veya Compose dosyası oluşturulmadı.
İlk uygulama oturumu önce küçük Compose DNS örneği, ardından sınırlı ürün iskeleti
olacak. Takvim sıkışırsa kabul testleri düşürülmeyecek.

| Bileşen | Hazırlanan sınır |
| --- | --- |
| API | Mevcut non-root image; yalnızca host loopback üzerinde yayınlanan port; aynı origin React/API |
| PostgreSQL | Ayrı Compose projesi ve yeni named volume; mevcut host veya visaassist volume'ları kullanılmaz; varsayılan host port yayını yok |
| Redis | Dahili ağda servis; host portu yok; Week 18'de bağlantı/servis temeli, ürün cache/limiter Week 19 |
| Migration | Tek seferlik servis; DB healthy sonrasında başlar; API için başarılı tamamlanma koşulu gerekir |
| Config | Takip edilen .env.example yalnızca boş/örnek alanlar; yerel .env ignored; gerekli secret eksikse erken hata |
| Yetkiler | Bootstrap yönetimi, migration ve runtime rolleri ayrılır; API'ye migration/admin parolası aktarılmaz |
| CI test DB | Runner'dan 127.0.0.1:5432 / opsdesk_product_test; mevcut test runner rolü ve guard korunur |

Önerilen Compose gelişim DB adı `opsdesk_compose_dev`; roller
`opsdesk_compose_migrator` ve `opsdesk_compose_app`. Bunlar henüz oluşturulmadı.
Bu DB üzerinde destructive test yapılmayacak. Testler yalnızca guarded
`opsdesk_product_test` hedefine gider.

Mevcut development migration kodu host/port/DB/rol olarak yalnızca
127.0.0.1:5432 / opsdesk_product_dev / opsdesk_product_app kabul ediyor; test guard
da servis adı kabul etmiyor. Bu nedenle mevcut target'ları değiştirmek yerine
ayrı `compose` migration target'ı tasarlanıp hedef/rol/bağlantı doğrulaması ve ret
testleriyle incelenecek. CI için mevcut test target'ı aynen kalacak.

CI hazırlığı: schema ve data job'ları `needs` ile sıralanacak. Job'lar veritabanını
paylaşmaz; her biri kendi disposable PostgreSQL servisini bootstrap/migrate eder.
Testler runner üzerinde çalışır; container içi localhost ile karıştırılmaz.
Schema/data aynı DB üzerinde paralel çalıştırılmaz. Production secret kullanılmaz;
güvenilmeyen PR koduna ayrıcalıklı token/secrets verilmez. Q03 #25 yalnızca kabul
kanıtından sonra kapatılır. PostgreSQL 18 uyumluluğu mevcut test belgeleriyle
hizalanacak; image patch/digest seçimi uygulama sırasında doğrulanacak.

Silme kuralı: normal oturum durdurması için `docker compose stop` tercih edilir.
`down` container/network kaldırır, `down -v` ayrıca volume verisini siler; kullanıcı
izni olmadan hiçbiri temizlik amacıyla çalıştırılmaz. Mevcut kaynaklar korunur.
Rendered `docker compose config` çıktısı secret içerebilir; paylaşılmaz/loglanmaz.

Başlangıç sırası: küçük DNS örneği → ürün servis/config iskeleti → ayrı migration
target ve rol/bootstrap → readiness/cold start → guarded DB CI → restart/restore
kanıtı. Mevcut backend/frontend/Docker CI korunur. Bugünkü hazırlık bu çıktıları
tamamlanmış saymaz.

Kaynaklar: [Compose başlangıç koşulları](https://docs.docker.com/compose/how-tos/startup-order/),
[runner üzerinde PostgreSQL service](https://docs.github.com/en/actions/tutorials/use-containerized-services/create-postgresql-service-containers).

## Öğrenme ve uygulama yöntemi

Kavram → küçük örnek → OpsDesk uygulaması → kontrollü hata → test → öğrenenin
anlatımı sırası izlenir. GitHub Actions temelleri mevcut CI var diye atlanmaz.
Günlük tablo başlangıç sırasıdır; öğrenme kontrolü geçilmeden bağımlı işe geçilmez.

## Günlük çalışma

| Gün | Çalışma | Beklenen kanıt |
| --- | --- | --- |
| 10 Kasım | API/PostgreSQL/Redis servisleri, internal DNS/port/volume tasarımı. | docker-compose.yml iskeleti ve .env.example. |
| 11 Kasım | DB bootstrap rol ayrımı ve tek seferlik Alembic migration servisi. | Boş volume üzerinden kurulum; migration başarısızsa API başlamaz. |
| 12 Kasım | Healthcheck/readiness ve uygulama bağlantı retry sınırları. | Cold start, gecikmiş DB, eksik config deneyleri. |
| 13 Kasım | Actions needs/service container/env/secrets/minimum permissions öğren; Q03 guarded PostgreSQL schema/data CI kur. | Sıralı migration/data job; test hedefi reddetme kontrolü. |
| 14 Kasım | Volume restart kalıcılığı ve izole yedekten dönüş; Linux log okuma. | Veri korunur; normal down volume silmez. |
| 15 Kasım | Tek komut acceptance; başarısız CI DB bağlantısını teşhis et; reverse proxy ve HTTP/TLS kavramını incele. | Port, servis DNS ve HTTP/TLS sınırı notu; yeni canlı proxy yok. |
| 16 Kasım | README ve haftalık rapor; CI/review; Q03 kabulünü kontrol et. | Kanıt yeterliyse #25 kapatılır; otomatik kapanış yok. |

## Test ve kabul

- [ ] fresh volume startup; restart persistence; migration failure; missing env; bounded connection failure; schema then data tests
- [ ] İlgili regression, Ruff ve mevcut frontend CI korunur.
- [ ] Yerel/dev/hosted veriye destructive test yapılmaz.
- [ ] Öğrenen kodun hata ve veri sınırını açıklayabilir.

## Öğrenme kanıtı

- [ ] Bir küçük uygulama adımını öğrenen yeniden yapar ve gerekçesini açıklar.
- [ ] Kontrollü uygulama/CI hatası logdan teşhis edilip düzeltilir.
- [ ] Notta tahmin, gözlenen sonuç ve çıkarılan ders ayrılır.
- [ ] Runner localhost ile servis içindeki localhost neden farklıdır? CI secret ile yerel env nasıl ayrılır?

Yazılması planlanan konu notları: notes/docker/compose-networking.md; notes/ci/postgresql-service-tests.md. Bu plan notların tamamlandığını iddia etmez.

## Notlar ve kapanış

Haftalık kavram notlarını `notes/` altında konu bazlı tut; Week 18 raporunu gerçek çalışma başladığında oluştur. Günlük ayrı rapor açma. `feature/week-18-compose-postgres-ci` önerilen feature branch adıdır; bu plan branch oluşturmaz. Küçük anlamlı commit, review ve normal PR merge kullan. Test sayısı/süre/yayın sonucu yalnızca çalıştırıldıktan sonra kaydedilir.

## Öğrenme soruları

- Container running neden DB ready değildir?
- Volume ve image farkı nedir?
- Migration yetkisi neden runtime yetkisinden ayrılır?

Hafta ortasında kalan işleri ve kapasiteyi yeniden değerlendir. Sonraki haftanın başlangıç koşulu, bu haftanın bağımlılıklarının doğrulanmasıdır; takvim güvenli testlerin önüne geçmez.
