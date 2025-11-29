#!/usr/bin/env python3
"""
Tüm servisleri sırayla çalıştıran orchestrator script
Her servis bitince diğeri başlar
"""

import subprocess
import sys
import os
from datetime import datetime

def log(message):
    """Log mesajı yazdır"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

def run_service(name, command, cwd):
    """
    Bir servisi çalıştır ve bitene kadar bekle
    
    Args:
        name: Servis adı
        command: Çalıştırılacak komut (list)
        cwd: Çalışma dizini
    
    Returns:
        bool: Başarılı ise True
    """
    log(f"{'='*80}")
    log(f"🚀 {name} BAŞLIYOR...")
    log(f"{'='*80}")
    
    start_time = datetime.now()
    
    try:
        # Servisi çalıştır ve bitene kadar bekle
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=False,  # Output'u doğrudan göster
            text=True
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        log(f"")
        log(f"✅ {name} BAŞARIYLA TAMAMLANDI!")
        log(f"⏱️  Süre: {duration:.2f} saniye ({duration/60:.2f} dakika)")
        log(f"")
        
        return True
        
    except subprocess.CalledProcessError as e:
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        log(f"")
        log(f"❌ {name} HATA VERDI!")
        log(f"⏱️  Süre: {duration:.2f} saniye")
        log(f"🔴 Hata kodu: {e.returncode}")
        log(f"")
        
        return False
    
    except Exception as e:
        log(f"")
        log(f"❌ {name} BEKLENMEYEN HATA!")
        log(f"🔴 Hata: {str(e)}")
        log(f"")
        
        return False

def main():
    """Ana fonksiyon - tüm servisleri sırayla çalıştır"""
    
    log("")
    log("=" * 80)
    log("🎯 TÜM SERVİSLER ORCHESTRATOR")
    log("=" * 80)
    log("")
    
    overall_start = datetime.now()
    
    # Servis listesi - sırayla çalışacak
    services = [
        {
            "name": "SRSERVICE",
            "command": [
                "/home/ahmet/Desktop/Myservices/SRservice/.venv/bin/python",
                "main_service.py"
            ],
            "cwd": "/home/ahmet/Desktop/Myservices/SRservice/functions"
        },
        {
            "name": "FIXTURE 2X",
            "command": [
                "/var/www/spradar/venv/bin/python3",
                "main.py"
            ],
            "cwd": "/var/www/spradar/modules/fixture2x"
        },
        {
            "name": "COMMENTARY",
            "command": [
                "/var/www/spradar/venv/bin/python3",
                "commentary_main.py",
                "--auto"
            ],
            "cwd": "/var/www/spradar/modules/commentary"
        },
        {
            "name": "COMEBACK",
            "command": [
                "/var/www/spradar/venv/bin/python3",
                "comeback_main_interactive.py",
                "--auto"
            ],
            "cwd": "/var/www/spradar/modules/SpecialBet/Comeback"
        }
    ]
    
    # İstatistikler
    total_services = len(services)
    successful = 0
    failed = 0
    
    # Her servisi sırayla çalıştır
    for i, service in enumerate(services, 1):
        log(f"📊 SERVİS {i}/{total_services}")
        
        success = run_service(
            service["name"],
            service["command"],
            service["cwd"]
        )
        
        if success:
            successful += 1
        else:
            failed += 1
            log(f"⚠️  {service['name']} başarısız oldu ama devam ediyoruz...")
            log("")
    
    # Genel özet
    overall_end = datetime.now()
    total_duration = (overall_end - overall_start).total_seconds()
    
    log("")
    log("=" * 80)
    log("📊 GENEL ÖZET")
    log("=" * 80)
    log(f"⏰ Başlangıç: {overall_start.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"⏰ Bitiş: {overall_end.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"⏱️  Toplam Süre: {total_duration:.2f} saniye ({total_duration/60:.2f} dakika)")
    log(f"")
    log(f"📈 Başarılı: {successful}/{total_services}")
    log(f"❌ Başarısız: {failed}/{total_services}")
    log(f"")
    
    if failed == 0:
        log("🎉 TÜM SERVİSLER BAŞARIYLA TAMAMLANDI!")
    else:
        log(f"⚠️  {failed} servis başarısız oldu!")
    
    log("=" * 80)
    log("")
    
    # Başarısız servis varsa exit code 1
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
