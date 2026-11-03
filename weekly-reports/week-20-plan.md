# Week 20 plan — Celery, retry/idempotency ve sistem kabulü

24–30 Kasım 2026. Planlama durumu: uygulanmadı. [Ay 5 sözleşmesi](../monthly-plans/month-05.md) kapsam ve güvenlik sınırlarında esas kaynaktır.

## Öğrenme ve uygulama yöntemi

Kavram → küçük örnek → OpsDesk uygulaması → kontrollü hata → test → öğrenenin
anlatımı sırası izlenir. GitHub Actions temelleri mevcut CI var diye atlanmaz.
Günlük tablo başlangıç sırasıdır; öğrenme kontrolü geçilmeden bağımlı işe geçilmez.

## Günlük çalışma

| Gün | Çalışma | Beklenen kanıt |
| --- | --- | --- |
| 24 Kasım | Task/queue/broker/worker kavramları; gerçek broker ve worker ile küçük log task; Compose worker ekle. | Mesajın API process dışında işlendiğini göster; simülasyon olduğunu açıkla. |
| 25 Kasım | Kontrollü geçici/kalıcı hata; sınırlı retry, backoff/jitter ve timeout; worker loglarını incele. | Retry sayısı ve tükenme davranışı gözlemlenir; her hata yeniden denenmez. |
| 26 Kasım | Event ID ve kalıcı simulated-notification sonucu; unique constraint ile duplicate/concurrent işleme. | Aynı event tekrar geldiğinde tek mantıksal sonuç; gerçek email yok. |
| 27 Kasım | Öğrenme kontrolü; Ticket commit sonrası publish hatasını üret; küçük outbox şeması ve transaction entegrasyonu. | Commit/publish boşluğu açıklanır; rollback event bırakmaz; HTTP/task idempotency ayrılır. |
| 28 Kasım | Küçük dispatcher; broker kesintisi/publish-gap/worker restart ve tekrar teslim testleri. | Pending/failed iş gözlemlenebilir; kayıp başarı iddiası yok. |
| 29 Kasım | Actions gerçek worker smoke, hata log artifact, timeout/cleanup; tam Compose ve request/event/task log ilişkisi. | Eager-only test yeterli sayılmaz; secret-safe loglar. |
| 30 Kasım | Ay kabul koşulları, README, haftalık/aylık rapor ve mimari anlatımı. | Başarısız gate varsa tarih revize edilir; CV yalnızca doğrulanmış kapsamı söyler. |

## Test ve kabul

- [ ] real broker and worker; commit/rollback boundary; retry exhausted; duplicate concurrent task; restart; publish-gap recovery; unchanged unrelated tenant
- [ ] İlgili regression, Ruff ve mevcut frontend CI korunur.
- [ ] Yerel/dev/hosted veriye destructive test yapılmaz.
- [ ] Öğrenen kodun hata ve veri sınırını açıklayabilir.

## Öğrenme kanıtı

- [ ] Bir küçük uygulama adımını öğrenen yeniden yapar ve gerekçesini açıklar.
- [ ] Kontrollü uygulama/CI hatası logdan teşhis edilip düzeltilir.
- [ ] Notta tahmin, gözlenen sonuç ve çıkarılan ders ayrılır.
- [ ] Worker neden ayrı process olmalıdır? Job timeout ile task timeout hangi sınırları korur?

Yazılması planlanan konu notları: notes/celery/retry-idempotency.md; notes/celery/commit-publish-gap.md. Bu plan notların tamamlandığını iddia etmez.

## Notlar ve kapanış

Haftalık kavram notlarını `notes/` altında konu bazlı tut; Week 20 raporunu gerçek çalışma başladığında oluştur. Günlük ayrı rapor açma. `feature/week-20-celery-reliable-jobs` önerilen feature branch adıdır; bu plan branch oluşturmaz. Küçük anlamlı commit, review ve normal PR merge kullan. Test sayısı/süre/yayın sonucu yalnızca çalıştırıldıktan sonra kaydedilir.

## Öğrenme soruları

- Retry neden duplicate sonuç üretebilir?
- Outbox hangi commit/publish boşluğunu çözer?
- Simulated notification idempotency neden gerçek email exactly-once garantisi değildir?

Hafta ortasında kalan işleri ve kapasiteyi yeniden değerlendir. Sonraki haftanın başlangıç koşulu, bu haftanın bağımlılıklarının doğrulanmasıdır; takvim güvenli testlerin önüne geçmez.
