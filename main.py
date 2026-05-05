import flet as ft
import os
import ssl
import yt_dlp

ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "DiyarBox Pro"
    page.theme_mode = "dark"
    # Tüm içeriği sayfada ortala
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Bileşenleri tanımlayalım
    status_text = ft.Text("DiyarBox v2.1", size=20, weight="bold", color="blue")
    
    url_input = ft.TextField(
        label="Video Linkini Buraya Yapıştır",
        width=350,
        border_radius=15,
        text_align=ft.TextAlign.LEFT
    )

    # İlerleme Çubuğu (Başlangıçta gizli ve temiz görünüm)
    pb = ft.ProgressBar(width=350, value=0, color="blue", visible=False)
    progress_percentage = ft.Text("", size=14)

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                float_p = float(p) / 100
                pb.value = float_p
                progress_percentage.value = f"İndiriliyor: %{p}"
                page.update()
            except:
                pass
        elif d['status'] == 'finished':
            pb.value = 1.0
            progress_percentage.value = "İşlem Tamamlanıyor..."
            page.update()

    def download_video(e):
        if not url_input.value:
            status_text.value = "⚠️ Lütfen link girin!"
            page.update()
            return
        
        try:
            pb.visible = True
            pb.value = 0
            status_text.value = "⏳ Hazırlanıyor..."
            page.update()

            # Telefon/PC dosya yolu kontrolü
            download_path = '%(title)s.%(ext)s' if os.name == 'nt' else '/storage/emulated/0/Download/%(title)s.%(ext)s'
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'progress_hooks': [progress_hook],
                'nocheckcertificate': True,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "✅ Galeriye Kaydedildi!"
            url_input.value = ""
            pb.visible = False
            progress_percentage.value = ""
        except Exception as ex:
            status_text.value = "❌ Hata: Linki kontrol edin"
            pb.visible = False
        page.update()

    # Arayüzü bir sütun içinde toplayarak dağılmasını önlüyoruz
    main_container = ft.Column(
        controls=[
            ft.Text("📥", size=50),
            status_text,
            ft.Divider(height=20, color="transparent"),
            url_input,
            ft.Container(height=10),
            ft.ElevatedButton(
                content=ft.Text("VİDEOYU İNDİR", weight="bold"),
                on_click=download_video,
                width=350,
                height=50,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
            ),
            ft.Container(height=20),
            pb,
            progress_percentage,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(main_container)

ft.app(target=main)
