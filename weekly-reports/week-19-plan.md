# Week 19 plan — Redis cache ve rate limiting

17–23 Kasım 2026. Planlama durumu: uygulanmadı. [Ay 5 sözleşmesi](../monthly-plans/month-05.md) kapsam ve güvenlik sınırlarında esas kaynaktır.

## Öğrenme ve uygulama yöntemi

Kavram → küçük örnek → OpsDesk uygulaması → kontrollü hata → test → öğrenenin
anlatımı sırası izlenir. GitHub Actions temelleri mevcut CI var diye atlanmaz.
Günlük tablo başlangıç sırasıdır; öğrenme kontrolü geçilmeden bağımlı işe geçilmez.

## Günlük çalışma

| Gün | Çalışma | Beklenen kanıt |
| --- | --- | --- |
| 17 Kasım | Scoped ticket-stats endpoint sözleşmesi ve cache olmadan sorgu. | Organizasyon/customer/staff sayım testleri; frontend değişikliği yok. |
| 18 Kasım | Redis key/value, TTL ve cache-aside; key kapsam tasarımı. | Yetki kontrolünden sonra hit/miss ve bounded timeout. |
| 19 Kasım | Commit sonrası invalidation; eşzamanlı eski cache yazma yarışı. | Create/rollback/TTL ve stale-fill testleri. |
| 20 Kasım | Login/register rate-limit sözleşmesi; eşik, anahtar, proxy ve store failure seçimi. | 429/Retry-After/503 politikası yazılı. |
| 21 Kasım | Atomik limiter uygulaması ve paralel istek testleri. | Expiry, doğru sayaç, proxy spoofing ve kesinti testleri. |
| 22 Kasım | Actions dependency cache/artifact ile Redis cache farkı; Redis entegrasyon CI ve bağlantı hatası teşhisi; broker izolasyonu. | Cache fallback ile limiter failure davranışı ayrı doğrulanır. |
| 23 Kasım | Notlar, regressions, PR ve haftalık rapor. | TTL/invalidation ve session/cache farkı öğrenen tarafından açıklanır. |

## Test ve kabul

- [ ] tenant/customer/staff separation; hit/miss; TTL; post-commit invalidation; rollback; race; Redis unavailable; concurrent limiter
- [ ] İlgili regression, Ruff ve mevcut frontend CI korunur.
- [ ] Yerel/dev/hosted veriye destructive test yapılmaz.
- [ ] Öğrenen kodun hata ve veri sınırını açıklayabilir.

## Öğrenme kanıtı

- [ ] Bir küçük uygulama adımını öğrenen yeniden yapar ve gerekçesini açıklar.
- [ ] Kontrollü uygulama/CI hatası logdan teşhis edilip düzeltilir.
- [ ] Notta tahmin, gözlenen sonuç ve çıkarılan ders ayrılır.
- [ ] Dependency cache ile uygulama cache farkı nedir? Cache miss neden test hatası olmak zorunda değildir?

Yazılması planlanan konu notları: notes/redis/cache-and-rate-limiting.md; notes/ci/cache-artifacts.md. Bu plan notların tamamlandığını iddia etmez.

## Notlar ve kapanış

Haftalık kavram notlarını `notes/` altında konu bazlı tut; Week 19 raporunu gerçek çalışma başladığında oluştur. Günlük ayrı rapor açma. `feature/week-19-redis-cache-limits` önerilen feature branch adıdır; bu plan branch oluşturmaz. Küçük anlamlı commit, review ve normal PR merge kullan. Test sayısı/süre/yayın sonucu yalnızca çalıştırıldıktan sonra kaydedilir.

## Öğrenme soruları

- Cache neden authorization yerine geçmez?
- TTL neden tek başına invalidation değildir?
- Limiter INCR ile expiry neden birlikte düşünülür?

Hafta ortasında kalan işleri ve kapasiteyi yeniden değerlendir. Sonraki haftanın başlangıç koşulu, bu haftanın bağımlılıklarının doğrulanmasıdır; takvim güvenli testlerin önüne geçmez.
