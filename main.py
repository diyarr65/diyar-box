
import os
import ssl

# SSL sertifika hatasını atlamak için
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_default_https_context = ssl._create_unverified_context

import flet as ft
# ... geri kalan kodlar aynı ...

import os
import ssl
import flet as ft
import yt_dlp

ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    # İkon ve karmaşık görselleri kaldırdık
    page.title = "YT Downloader"
    
    url_input = ft.TextField(label="YouTube Linkini Buraya Gir")
    status_text = ft.Text()

    def download_video(e):
        try:
            status_text.value = "İndirme başladı..."
            page.update()

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            ydl_opts = {
                'format': 'best',
                'outtmpl': f'{desktop}/%(title)s.%(ext)s',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "Masaüstüne başarıyla indi!"
        except Exception as ex:
            status_text.value = f"Hata: {str(ex)}"
        page.update()

    # Sadece metin kutusu ve buton
    page.add(
        ft.Text("YouTube Indirici", size=25),
        url_input,
        ft.ElevatedButton("Indir", on_click=download_video),
        status_text
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)