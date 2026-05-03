import flet as ft
import os
import ssl
import yt_dlp

ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "DiyarBox Pro"
    page.theme_mode = "dark"
    page.horizontal_alignment = "center"
    
    # 1. İlerleme Çubuğu ve Yüzde Yazısı Bileşenleri
    pb = ft.ProgressBar(width=300, value=0, color="blue", visible=False)
    progress_text = ft.Text("", size=12, color="grey")
    status_text = ft.Text("DiyarBox v2.0", size=16)

    # 2. İlerlemeyi Yakalayan Fonksiyon
    def progress_hook(d):
        if d['status'] == 'downloading':
            # İndirme yüzdesini hesapla (0.0 ile 1.0 arası)
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                float_p = float(p) / 100
                pb.value = float_p
                progress_text.value = f"İndiriliyor: %{p}"
            except:
                pass
            page.update()
        elif d['status'] == 'finished':
            pb.value = 1
            progress_text.value = "Dosya birleştiriliyor..."
            page.update()

    def download_video(e):
        try:
            if not url_input.value:
                return
            
            # İndirme başladığında çubuğu göster
            pb.visible = True
            status_text.value = "🔄 İşlem Başladı"
            page.update()

            if os.name == 'nt':
                download_path = '%(title)s.%(ext)s'
            else:
                download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'progress_hooks': [progress_hook], # Kancayı buraya takıyoruz
                'nocheckcertificate': True,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "✅ Tamamlandı!"
            pb.visible = False
            progress_text.value = ""
        except Exception as ex:
            status_text.value = "❌ Hata oluştu"
            pb.visible = False
        page.update()

    url_input = ft.TextField(label="Video Linki", width=320)

    page.add(
        ft.Text("DiyarBox", size=40, weight="bold"),
        url_input,
        ft.Container(height=10),
        ft.ElevatedButton("İNDİR", on_click=download_video, width=300),
        ft.Container(height=20),
        status_text,
        pb,           # İlerleme çubuğu
        progress_text # Yüzde bilgisi
    )

ft.app(target=main)
