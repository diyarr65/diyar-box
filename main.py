import os
import ssl
import flet as ft
import yt_dlp

# SSL sertifika hatasını atlamak için
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "YT Downloader"
    # Telefon ekranına uygun hizalama
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    url_input = ft.TextField(label="YouTube Linkini Buraya Gir", width=350)
    status_text = ft.Text()

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "Lütfen bir link girin!"
                page.update()
                return

            status_text.value = "İndirme başladı..."
            page.update()

            # ANDROID UYUMLU YOL: /storage/emulated/0/Download
            # Bu klasör tüm Android cihazlarda standart indirme klasörüdür.
            download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'

            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'nocheckcertificate': True,
                'quiet': False,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "Video 'İndirilenler' klasörüne kaydedildi!"
        except Exception as ex:
            status_text.value = f"Hata: {str(ex)}"
        page.update()

    page.add(
        ft.Text("YouTube İndirici", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20, color="transparent"),
        url_input,
        ft.ElevatedButton(
            "Videoyu İndir", 
            on_click=download_video,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        ft.Divider(height=20, color="transparent"),
        status_text
    )

# view=ft.AppView.WEB_BROWSER kısmını kaldırdık, varsayılan mobildir.
ft.app(target=main)
