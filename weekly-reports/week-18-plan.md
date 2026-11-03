# Week 18 plan — Compose ve izole veritabanı CI

10–16 Kasım 2026. Planlama durumu: uygulanmadı. [Ay 5 sözleşmesi](../monthly-plans/month-05.md) kapsam ve güvenlik sınırlarında esas kaynaktır.

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
