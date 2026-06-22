# AI Team Skills — Kurulum ve Kullanım Kılavuzu (v2.3.0)

Bu kılavuz, **AI Team Skills (v2.3.0)** sisteminin yeni veya mevcut bir projede nasıl kurulacağını, aktifleştirileceğini ve en doğru şekilde nasıl kullanılacağını adım adım açıklamaktadır.

---

## 📋 Gereksinimler
Sistemin betikleri ve CLI arayüzünün çalışması için sisteminizde aşağıdaki bileşenlerin yüklü olması gerekir:
1. **Node.js** (v18.0.0 veya üzeri)
2. **Python** (v3.10 veya üzeri)

---

## 🚀 1. Kurulum Adımları (Installation)

Sistemi projenize kurmak için aşağıdaki yöntemlerden birini seçebilirsiniz:

### Yöntem A: Global CLI ile Kurulum (Önerilen)
CLI arayüzü sayesinde tek bir komutla projeyi başlatabilir ve durumu izleyebilirsiniz.
1. Projenin ana klasöründeyken `cli` dizinine gidin ve bağımlılıkları yükleyip derleyin (veya global olarak kurun):
   ```bash
   # CLI aracını global olarak sisteme kurun
   npm install -g ./cli
   ```
2. Proje dizininize geri dönün ve entegrasyonu başlatın:
   ```bash
   # Projeyi başlatın (Örn: Windsurf/Trae/Cursor için)
   aiteam init --name "ProjeAdiniz" --ai windsurf
   ```

### Yöntem B: Kurulum Betikleri ile Kurulum (Script-Based)
Hiçbir global npm paketi kurmadan doğrudan PowerShell veya Bash betiklerini çalıştırabilirsiniz:
* **Windows (PowerShell)**:
  ```powershell
  .\install.ps1 auto
  ```
* **Linux/macOS (Bash)**:
  ```bash
  chmod +x install.sh
  ./install.sh . auto
  ```

---

## 🔄 2. IDE Asistanını Aktifleştirme (Auto-Activation)

Kurulum tamamlandıktan sonra, kullandığınız yapay zeka asistanının (Claude Code, Cursor, Windsurf, Trae vb.) skilleri ve rolleri otomatik yüklemesi için **yeni bir sohbet (chat) başlattığınızda** asistanınıza şu mesajı gönderin:

> **Aktivasyon Promptu:**
> *"Kök dizindeki `AI-TEAM.md` dosyasını oku, asistan durumunu analiz et ve AI Team kurallarını aktifleştir."*

Asistan bu komuttan sonra projedeki tüm rolleri üstlenecek ve `.ai-team/brain/` klasöründeki bellek veritabanını takip edecektir.

---

## 🧠 2.1. Akıllı Davranış — Core Protocols (v2.3.0)

v2.3.0 ile her ajan, domain işine başlamadan önce `.claude/skills/_core-protocols.md` dosyasındaki **dört kesişen protokolü** uygular. Bu protokoller, ekibin projenizi gerçekten "tanıyan" tek bir mühendis gibi davranmasını sağlar:

* **🔄 Süreklilik (Continuity)**: Yeni bir sohbet açıldığında model önce beyni okur (`project-profile.json` → `project-state.json` → ajan beyinleri) ve harekete geçmeden önce projenin nerede kaldığını yeniden kurar. Bağlam kaybolmaz.
* **🎯 Adaptasyon (Adaptation)**: Her öneri, `project-profile.json` içindeki gerçek teknoloji yığınına/kurallarına göre uyarlanır — genel ders kitabı tavsiyesi verilmez. Profil boşsa model yığını repo'dan tespit edip doldurur.
* **🌱 Kendini Geliştirme (Self-Evolution)**: Model öğrendiklerini sürekli beyne yazar; bir skill dosyasının kendisini değiştirmesi gerektiğinde sessizce düzenlemez — `proposed-improvements.md` dosyasına **öneri** bırakır ve size sorar.
* **❓ Soru Sorma (Clarification)**: Yanlış varsayımın pahalı veya geri dönülmez olduğu yerlerde (şema, public API, kimlik doğrulama, dış entegrasyon, mimari) model size sorar; ucuz/geri alınabilir seçimlerde varsayımını belirterek ilerler.

> **Project DNA**: `project-profile.json` dosyası projenizin yığınını, alanını (domain), kurallarını, sözlüğünü ve kararlarını tutar. Her oturum bu dosyayı **ilk** okuyarak projenin ne olduğunu anlar.

---

## 🔍 3. Entegrasyon ve Bütünlük Doğrulama Akışı

Tüm asistanlar ve skiller, kod üzerinde işlem yaparken projenin tamamı kapsamında aşağıdaki **4 adımı sırasıyla** izler:

1. **Entegrasyon Kontrolü**: Modüller arası import zincirleri, API rotaları ve provider wiring (bağlantı) kurulumlarının bütünlüğü denetlenir.
2. **Sorun Tespiti**: Derleme hataları, runtime istisnaları ve mantıksal tutarsızlıklar kök nedenleriyle belirlenir.
3. **Sistematik Düzeltme**: Hatalar kod standartlarına uygun ve yan etkisiz şekilde düzeltilir, açıklayıcı yorum satırları eklenir.
4. **Build Doğrulama**: Projenin sıfır hata/uyarı ile derlendiği (build) test edilerek doğrulanır.

---

## 📝 4. Kullanışlı Komutlar (Slash Commands)

Projenizin durumunu sorgulamak veya sprint yönetmek için IDE sohbet panelinde ya da terminalde aşağıdaki komutları kullanabilirsiniz:

| Komut | Terminal Karşılığı | Açıklama |
|---|---|---|
| `/team-status` | `aiteam status` | Tüm ekibin ilerleme durumunu ve aktif rolleri gösterir. |
| `/team-blockers` | `aiteam status` | Geliştirmeyi engelleyen kritik tıkanıklıkları (blockers) raporlar. |
| `/team-next` | `aiteam status` | Sırada yapılması gereken öncelikli sprint görevini getirir. |
| `/deploy-check` | `aiteam deploy-check` | Projenin canlıya çıkmaya hazır olup olmadığını Kalite Kapılarına göre sorgular. |
| `/team-adr` | `aiteam adr` | Yeni bir Mimari Karar Kaydı (Architecture Decision Record) şablonu oluşturur. |

---

## 📏 5. Altın Kurallar ve Sınırlar
* **1000 Satır Kuralı**: Bağlam (context) pencerelerini optimize etmek ve kod karmaşasını önlemek adına, hiçbir kaynak kod dosyası **1000 satırı aşamaz**. Aşma eğiliminde olan dosyalar derhal modüllere ayrılmalıdır.
* **Güvenlik Veto Yetkisi**: Güvenlik bileşeninde (`security`) açık veya tamamlanmamış bir sorun varsa `/deploy-check` dağıtımı kesin olarak bloklar. Güvenlik açıkları her şeyden önce giderilmelidir.
