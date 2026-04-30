import os
import ssl
import flet as ft
import yt_dlp

# SSL sertifika hatalarını kökten çözelim
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "Sosyal Medya İndirici"
    # Siyah ekran sorununu önlemek için temayı varsayılan bırakalım
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    url_input = ft.TextField(
        label="Link Yapıştır (YouTube, TikTok, IG)",
        width=300
    )
    status_text = ft.Text(text_align=ft.TextAlign.CENTER)

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "Lütfen link girin!"
                page.update()
                return

            status_text.value = "İndiriliyor... Lütfen bekleyin."
            page.update()

            # En güvenli Android yolu
            download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'

            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'nocheckcertificate': True,
                # TikTok/IG için gerekli olan kimlik
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "Video İndirilenler'e kaydedildi! ✅"
        except Exception as ex:
            status_text.value = f"Hata: {str(ex)}"
        page.update()

    page.add(
        ft.Text("Video Downloader", size=25, weight="bold"),
        url_input,
        ft.ElevatedButton("İndir", on_click=download_video),
        status_text
    )

ft.app(target=main)
