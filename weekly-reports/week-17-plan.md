# Week 17 plan — Docker ve sistem temelleri

4–9 Kasım 2026. Planlama durumu: uygulanmadı. [Ay 5 sözleşmesi](../monthly-plans/month-05.md) kapsam ve güvenlik sınırlarında esas kaynaktır.

10 Kasım kapanış notu: yukarıdaki durum başlangıç planına aittir. Teknik öğrenme,
build/runtime ve CI kanıtları [Week 17 raporunda](week-17.md) kaydedildi. Planlanan
9 Kasım doğrulaması 10 Kasım'da yapıldı. PR/merge/release durumu raporda ayrı
tutulur. Aşağıdaki başlangıç checklist'i geriye dönük sonuç yerine kullanılmaz.

## Öğrenme ve uygulama yöntemi

Kavram → küçük örnek → OpsDesk uygulaması → kontrollü hata → test → öğrenenin
anlatımı sırası izlenir. GitHub Actions temelleri mevcut CI var diye atlanmaz.
Günlük tablo başlangıç sırasıdır; öğrenme kontrolü geçilmeden bağımlı işe geçilmez.

## Günlük çalışma

| Gün | Çalışma | Beklenen kanıt |
| --- | --- | --- |
| 4 Kasım | Mevcut image/build/CI yapısını incele; disk/Docker kullanılabilirliğini kontrol et; devreden riskleri kaydet. | Mimari sınır ve baseline; kaynak kod taşıma yok. |
| 5 Kasım | Process, PID, port, DNS, HTTP/TLS ve venv/container farkını küçük örnekte öğren. | Bir port çakışması ve DNS hatasının teşhisi. |
| 6 Kasım | Önce basit backend image: Dockerfile, layer, build context, .dockerignore; docker build/run. Ardından kilitli bağımlılıkları incele. | Image secrets/test verisi içermeden build olur. |
| 7 Kasım | Node build → Python runtime multi-stage; layer cache, non-root, mevcut React dist kopyası; health smoke. | Yeni React kodu olmadan çalışan mevcut UI/API. |
| 8 Kasım | GitHub Actions workflow/event/runner/job/step öğren; mevcut YAML incelemesi; Docker build job ekle; bilerek bozup logdan düzelt. | Ruff/pytest/Docker build sonuçları ve failed-build deneyi. |
| 9 Kasım | Container logs/SIGTERM kapanışı; README setup; bağımsız build/run tekrarı ve haftalık değerlendirme. | PR/CI ve Week 17 raporu; Week 18 config kararı. |

## Test ve kabul

- [ ] docker build; container health; non-root; eksik config güvenli hata; SIGTERM kapanışı; image içinde secret olmadığını doğrulama
- [ ] İlgili regression, Ruff ve mevcut frontend CI korunur.
- [ ] Yerel/dev/hosted veriye destructive test yapılmaz.
- [ ] Öğrenen kodun hata ve veri sınırını açıklayabilir.

## Öğrenme kanıtı

- [ ] Bir küçük uygulama adımını öğrenen yeniden yapar ve gerekçesini açıklar.
- [ ] Kontrollü uygulama/CI hatası logdan teşhis edilip düzeltilir.
- [ ] Notta tahmin, gözlenen sonuç ve çıkarılan ders ayrılır.
- [ ] Workflow, job ve step farkı nedir? Bir komutun exit code değeri CI sonucunu nasıl etkiler?

Yazılması planlanan konu notları: notes/docker/docker-foundations.md; notes/ci/github-actions-foundations.md. Bu plan notların tamamlandığını iddia etmez.

## Notlar ve kapanış

Haftalık kavram notlarını `notes/` altında konu bazlı tut; Week 17 raporunu gerçek çalışma başladığında oluştur. Günlük ayrı rapor açma. `feature/week-17-docker-foundation` önerilen feature branch adıdır; bu plan branch oluşturmaz. Küçük anlamlı commit, review ve normal PR merge kullan. Test sayısı/süre/yayın sonucu yalnızca çalıştırıldıktan sonra kaydedilir.

## Öğrenme soruları

- Docker neden venv değildir?
- EXPOSE ile port publish farkı nedir?
- Bir container içindeki localhost hangi makinedir?

Hafta ortasında kalan işleri ve kapasiteyi yeniden değerlendir. Sonraki haftanın başlangıç koşulu, bu haftanın bağımlılıklarının doğrulanmasıdır; takvim güvenli testlerin önüne geçmez.
