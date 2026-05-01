import os
import ssl
import flet as ft
import yt_dlp

# SSL Sertifika hatasını bypass et
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    # Sayfa ayarlarını en basit halde tutalım
    page.title = "DiyarBox"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Durum takibi için etiket
    status_text = ft.Text("Sistem Hazır", color=ft.colors.GREY_400)
    
    # Link giriş kutusu
    url_input = ft.TextField(
        label="Video Linki",
        hint_text="Yapıştırın...",
        width=300
    )

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "⚠️ Link girmediniz!"
                page.update()
                return

            status_text.value = "⏳ İndiriliyor... Lütfen bekleyin."
            status_text.color = ft.colors.BLUE_400
            page.update()

            # Android için kesin yol
            download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'

            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'nocheckcertificate': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "✅ Başarıyla İndirildi!"
            status_text.color = ft.colors.GREEN_400
            url_input.value = ""
        except Exception as ex:
            # Hata mesajını kısa tutalım ki ekrana sığsın
            status_text.value = f"❌ Hata: {str(ex)[:50]}"
            status_text.color = ft.colors.RED_400
        
        page.update()

    # Tasarımı ekle (En basit haliyle)
    page.add(
        ft.Column(
            [
                ft.Text("DiyarBox", size=30, weight="bold"),
                ft.Text("v1.2 - Kararlı Sürüm", size=12),
                ft.Divider(height=20),
                url_input,
                ft.ElevatedButton("VİDEOYU İNDİR", on_click=download_video, width=300),
                ft.Divider(height=10),
                status_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Uygulama başlatma
ft.app(target=main)
