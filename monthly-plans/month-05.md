# Ay 5 — Backend sistem temelleri ve güvenilir iş yürütme

3 Kasım 2026 tarihinde kullanıcı tarafından onaylanan kapsam. Bu bir uygulama
planıdır; aşağıdaki çıktılar henüz üretilmiş veya doğrulanmış değildir.

## Amaç ve sınırlar

Docker + Compose + Redis cache/rate limiting + Celery + GitHub Actions CI +
retry/idempotency + temel Linux/networking/logging. Python/FastAPI bilgisini
çalıştırılabilir, gözlemlenebilir ve hata davranışı anlaşılmış bir sisteme taşımak.

Yeni React özellikleri, frontend yeniden tasarımı, RAG, MCP, agents, Kubernetes,
AI görevleri, async SQLAlchemy ve sağlayıcı taşıması kapsam dışıdır. Mevcut React
build'i korunur; mevcut frontend CI kaldırılmaz. RQ yerine Celery seçilmiştir.

Eklenen piyasa metni karar bağlamıdır; içindeki istatistik ve ilan iddiaları bu
çalışmada bağımsız doğrulanmadı, doğrulanmış araştırma olarak aktarılmadı.

## Takvim ve kapasite varsayımı

Kullanıcının belirlediği başlangıç **4 Kasım 2026**. Öğrenme günlerini sıkıştırmamak
için tüm günlük takvim bir gün kaydırıldı; hedef kapanış 30 Kasım. Haftalar bu
ay için çalışma bloklarıdır, Pazartesi–Pazar takvim haftası olmak zorunda değildir.

| Hafta | Önerilen tarihler | Odak | Tahmini aktif süre |
| --- | --- | --- | --- |
| [17](../weekly-reports/week-17-plan.md) | 4–9 Kasım | Dockerfile, Linux ve Docker build CI | 20–24 saat |
| [18](../weekly-reports/week-18-plan.md) | 10–16 Kasım | Compose, config, migration, PostgreSQL CI | 20–26 saat |
| [19](../weekly-reports/week-19-plan.md) | 17–23 Kasım | Scoped stats, cache ve rate limiting | 20–26 saat |
| [20](../weekly-reports/week-20-plan.md) | 24–30 Kasım | Celery, retry, idempotency ve sistem kabulü | 24–32 saat |

Toplam 84–108 saat bir tahmindir, çalışılmış süre değildir. Week 17 kısa bir ilk
haftadır. Her hafta ortasında kapasite kontrolü yapılır; yetmezse tarih güncellenir,
testler düşürülmez veya işler tamamlanmış gösterilmez. Önceki yoğun Week 16 temposu
bu aya otomatik taşınmaz. Günlük sıralama hafta planlarında öneridir.

## Öğrenme sözleşmesi

Kullanıcının son onayı: öğrenme bölümleri, GitHub Actions dahil, mevcut kod veya
test sayısı gerekçesiyle kısaltılmaz. Çalışan proje, bağımsız yetkinlik kanıtı değildir.
Her konu şu sırayla işlenir:

1. Kavram ve neden ihtiyaç duyulduğu; küçük benzer örnek.
2. Öğrenenin sonucu tahmin etmesi ve örneği çalıştırması.
3. OpsDesk üzerinde sınırlı değişiklik.
4. Kontrollü hata üretme, log okuma ve hatayı düzeltme.
5. İlgili test, kısa konu notu ve tasarım kararını kendi sözleriyle açıklama.

Küçük deneyler yeni bir yan projeye dönüşmez. Mentor mimariyi açıklar ve review
yapar; öğrenen temel adımları tekrar kurar. Hazır kod verilmesi öğrenme kontrolünün
yerine geçmez. Günlük oturum için yaklaşık dağılım: %25 kavram/örnek, %45 uygulama,
%20 test/hata teşhisi, %10 not ve anlatım; gerçek ihtiyaca göre değişebilir.

## GitHub Actions öğrenme hattı

- **Week 17:** CI ile CD farkı; YAML, workflow, event, runner, job, step,
  `uses`/`run`, çalışma dizini, exit code, PR/push tetikleyicileri. Mevcut workflow'u
  satır satır açıkla; küçük bir kontrolü yaz, bilerek boz ve logdan düzelt.
  Checkout, Python/Node kurulumu ve kilitli bağımlılıklardan sonra Ruff/pytest/
  frontend/Docker build adımlarının neden bu sırada olduğunu öğren.
- **Week 18:** `needs`, job izolasyonu, service container, healthcheck, env/secrets,
  minimum token izinleri ve güvenilmeyen PR kodu. Production secret kullanılmadan
  PostgreSQL hazırlığı, guarded schema/data testleri, migration kontrolü ve başarısız
  job logları. Runner üzerinde çalışan test ile container içindeki localhost farkı.
- **Week 19:** Dependency cache ile ürün Redis cache farkı; cache key ve lockfile,
  artifact/log ile cache farkı, Redis service entegrasyonu, timeout ve deterministik
  test. Bozuk bir Redis bağlantısını CI logundan teşhis et; flaky testi retry ile gizleme.
- **Week 20:** Gerçek worker/broker testi, servis loglarının hata halinde toplanması,
  cleanup, job timeout ve check sonuçları. PR checks ile merge kuralları arasındaki
  farkı öğren; ücretli veya repo ayarı değişikliği varsayma. Docker build başarısı
  ile çalışan sistem smoke testini ayır. Otomatik production deploy bu ay zorunlu değil.

CI öğrenme kabulü: öğrenen mevcut workflow'u açıklayabilir, küçük bir job'ı örnekten
uyarlayabilir ve başarısız bir çalışmayı logdan düzeltebilir. Yeşil işaret veya test
sayısı tek başına bu kabulü karşılamaz.

## Hedef mimari

Mevcut monorepo korunur: `src/opsdesk`, `migrations`, `tests`, `frontend`.
Kullanıcının backend/ ağacı mantıksal bileşen ayrımıdır; klasör taşıma şartı değildir.

- Kök `Dockerfile`: kilitli Python bağımlılıkları; API ve worker aynı uygulama
  image'ından farklı komutlarla başlar. Mevcut React çıktısı gerektiğinde build
  aşamasında üretilip FastAPI tarafından sunulur; yeni frontend servisi zorunlu değil.
- `docker-compose.yml`: API, PostgreSQL, Redis ve Week 20'de Celery worker.
  Migration tek seferlik servis, güvenilir gönderim için küçük outbox dispatcher
  ayrı process/servis olabilir. Genel amaçlı event platformu yapılmaz.
- Redis: disposable cache/rate-limit ve broker sorumluluklarının eviction/persistence
  ihtiyaçları ayrılır. Broker için ayrı Redis instance'ı tercih edilir; sadece DB
  numarasını ayırmak bellek politikalarını birbirinden bağımsız yapmaz.
- `.dockerignore`, secrets içermeyen `.env.example`, README başlangıç/test/kurtarma
  komutları. Secrets image layer, build arg, Git veya log içine girmez.
- Mevcut `.github/workflows/ci.yml` genişletilir; yeni paralel CI kopyası oluşturulmaz.

Temiz checkout'ta Docker/Compose kurulu ve belgelenmiş yerel secret/config hazırlığı
bir kez yapıldıktan sonra `docker compose up --build` tüm gerekli servisleri başlatır.
Bu, ilk config hazırlığını gizleyen veya hardcoded secret kullanan bir vaat değildir.

## Teknik sözleşmeler

### Docker/Compose ve veri

Image/container/venv farkı, PID 1/sinyaller, non-root runtime, port binding, DNS,
servis adları, volume ve loglar uygulama üzerinde öğrenilir. Production-oriented
image, production-ready sistem sertifikası değildir. Readiness ile process'in
başlaması ayrı tutulur; migration başarısızsa API/worker başlamaz. Migration rolü
worker/runtime ortamına gereksiz yere aktarılmaz. Volume silmek normal kapatma değildir.

Destructive test hedefi yalnızca `opsdesk_product_test` kalır. CI testleri runner'da
çalışıp disposable PostgreSQL'e 127.0.0.1 üzerinden bağlanır; mevcut guard'a uyar.
Container içi servis adı için guard gevşetilmez. Gerekirse yeni allowlist ayrı
karar/test incelemesi ister. Dev, test ve hosted veri/credential'ları ayrıdır.

### Redis/cache/rate limit

Önce cache'siz `GET /organizations/{organization_id}/ticket-stats` sözleşmesi:
mevcut durum başına Ticket sayısı, customer için yalnızca kendi kayıtları, staff
için aynı organizasyon. Yeni grafik veya React paneli zorunlu değildir.

Her istekte güncel yetki kontrolü cache'den önce yapılır. Key; organizasyon,
görünürlük/kullanıcı kapsamı, sorgu ve şema sürümünü içerir. TTL ve invalidation
ölçülür. Ticket create commit'inden sonra ilgili stats geçersizleştirilir; rollback
etmez. Eşzamanlı eski sorgunun cache'i yeniden doldurma yarışı test edilir.
Yalnızca durum sayıları için öncelik değişimi gereksiz invalidation istemez.
Redis cache kesintisinde kontrollü DB fallback ve timeout; yetki fallback'i yoktur.

Kayıt/login için sınırlı rate-limit politikası: atomik sayaç+expiry, 429 ve
Retry-After, güvenilir proxy/IP sınırı, ham parola/token loglamama. İstemcinin
X-Forwarded-For değerine kör güvenilmez. Limiter store kesintisi için açık politika
önerisi güvenli 503; cache fallback'inden ayrıdır. Eşikler uygulanmadan önce seçilir.
Session/cache farkı öğrenilir; JWT/session/refresh-token mimarisi değiştirilmez.

### Celery ve idempotency

Öğretim sırası zorunludur: önce basit task → broker → worker ve yalnızca simülasyon
logu; sonra kontrollü hata/retry/timeout; ardından kalıcı sonuç ve duplicate testi;
en son commit/publish boşluğu deneyi ve küçük outbox/dispatcher. İlk örneğe bütün
altyapı yüklenmez. Aşağıdaki sözleşme ay sonu hedefidir, ilk günün işi değildir.


İlk iş gerçek e-posta veya AI değildir: Ticket bildirimi simülasyonu.
Ticket ve notification event aynı PostgreSQL transaction'ında kaydedilir.
Küçük outbox dispatcher commit edilmiş event'i broker'a yollar; publish öncesi/
sonrası çökme tekrar teslim doğurabilir. Worker yalnızca ID taşır, gerekli kaydı
DB'den okur. Retry yalnızca geçici hatalarda, sınırlı sayıda backoff/jitter ve timeout
ile yapılır; kalıcı hata görünür failed durumuna gider. Sonsuz retry yoktur.

Bir event ID için tek kalıcı simulated-notification kaydı, unique constraint ve
transaction ile sağlanır. Duplicate/concurrent delivery yeni mantıksal sonuç
oluşturmaz. Log satırının tam bir kez yazılması veya gerçek dış servis için exactly-once
iddiası yapılmaz. Log açıkça `notification_simulated` der.

Task idempotency, HTTP POST idempotency değildir. Aynı HTTP isteğinin iki Ticket
oluşturmasını önleyen Idempotency-Key sözleşmesi küçük öğrenme notu olarak incelenir;
ürüne genel middleware zorunlu değildir. Bu ayın zorunlu idempotency çıktısı worker
ve kalıcı simülasyon sonucudur. HTTP idempotency yapılmadan POST tekrarına güvence verilmez.

## CI ve kabul koşulları

PR'da mevcut Ruff check/format ve non-integration pytest devam eder. Week 17'de
Docker build eklenir; Week 18'de Q03 için izole schema ardından data testi job'u,
Week 19–20'de Redis/worker entegrasyon kontrolleri eklenir. Frontend CI korunur.
DB suite'leri aynı hedef üzerinde paralel çalıştırılmaz. Test-secret'ları production
credential'ları değildir. Docker build testi tek başına startup kanıtı değildir.

- [ ] Belgelenmiş hazırlık sonrası tek Compose komutu; cold start ve restart geçer.
- [ ] Health/readiness, başarısız migration, port/DNS/config hataları anlaşılır.
- [ ] Veri restart sonrası korunur; test/dev/hosted hedefleri karışmaz.
- [ ] Cache hit/miss/TTL/invalidation, customer/staff/tenant sınırları testlidir.
- [ ] Rate limit eşzamanlılık, expiry, 429 ve Redis kesintisi testlidir.
- [ ] Commit edilmiş Ticket event'i worker'a ulaşır; rollback'te iş oluşmaz.
- [ ] Broker kesintisi sonrası event geri kazanılır; duplicate iş tek DB sonucu verir.
- [ ] Retry tükenmesi/worker restart sonuçları ve güvenli loglar doğrulanır.
- [ ] PR'da Ruff, pytest, Docker build ve gerekli entegrasyon job'ları yeşildir.
- [ ] README, haftalık raporlar ve öğrenenin mimari açıklaması kanıtla tamamlanır.

## Ay sonu bağımsız uygulama kontrolü

- [ ] README ile ortamı yeniden kur; image, container, network ve volume ilişkisini anlat.
- [ ] Bir port/config/servis bağlantı hatasını loglarla bulup düzelt.
- [ ] Bir CI job'ını açıkla ve kontrollü başarısızlığı gider.
- [ ] Aynı stats isteğinde cache hit/miss ve erişim kapsamını göster.
- [ ] Bir işi iki kez gönder; kalıcı sonucun neden tek olduğunu açıkla.
- [ ] Broker kapalıyken oluşan işi, broker açılınca geri kazan; sınırları anlat.

Week 20 en yoğun haftadır. 27 Kasım'da retry/idempotency kontrolü, 29 Kasım'da
outbox ve entegrasyon kontrolü yapılır. Öğrenme veya test eksikse 30 Kasım kapanışı
ertelenir; Ay 6 görevleriyle üst üste bindirilmez. İlk hafta da altı günlük bir
aralıkta yaklaşık 20–24 saat gerektirir. Saatler kapasite varsayımıdır, taahhüt değil.

## Devreden işler ve issue sınırları

#19/#24 3 Kasım'da tamamlandı olarak kapatıldı. #25 PostgreSQL CI bu ay Week 18'e
hedeflenir. #26 kapsamlı backend yayını, bağımlılıkları bitmeden kapatılmaz.
#16/#17/#20'nin atama kısmı/#21/#22/#23 mevcut backlog'dur; bunların tamamını bu aya
sıkıştırma veya ay sonunda bitmiş gösterme. Tarihleri hâlâ ayrıca kararlaştırılmalı.

Ay 4'ten gelen dependency bulguları, provider audit, hosting kullanım kontrolü ve
hosted backup/export/restore eksikleri Week 17 başında gözden geçirilir. Yerel
Compose kanıtı hosted backup kanıtı sayılmaz. Rate-limit uygulaması Week 19'da
ilerler; canlıya alınması ayrı rollout kontrolüdür. Geniş demo daveti, yeni ücretli
hizmet veya Railway'den geçiş bu planla onaylanmış değildir.

## Çalışma yöntemi ve kaynaklar

Önce gerekçe ve küçük benzer örnek, ardından sınırlı uygulama, öğrenen code review,
pytest/entegrasyon/manual doğrulama, sonra commit. Yeni işte hata/yetki/veri sınırını
öğrenen açıklayabilmeli. Kodun kaynağını öne çıkaran ürün etiketleri eklenmez;
bağımsız öğrenme ve test sonucu uydurulmaz. Haftalık normal merge geçmişi korunur.

Resmi referanslar (3 Kasım plan incelemesi):
- [Docker Compose startup/readiness](https://docs.docker.com/compose/how-tos/startup-order/)
- [Celery tasks, retry ve idempotency](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [Redis INCR ve rate limiter örnekleri](https://redis.io/docs/latest/commands/incr/)

Ay sonu CV cümlesi yalnızca kabul testlerinden sonra kullanılacak taslaktır:
“FastAPI, PostgreSQL, Redis ve Celery için Docker Compose geliştirme ortamı kurdum;
yetki kapsamına uygun cache, rate limiting ve retry/idempotency kontrollü bildirim
simülasyonu ekledim; Ruff, pytest ve Docker build kontrollerini PR akışına bağladım.”
