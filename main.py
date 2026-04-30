import os
import ssl
import flet as ft
import yt_dlp
import traceback

# SSL Sertifika hatalarını bypass et
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "DiyarBox"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Uygulama başladığında ilk burası çalışır
    def startup_check():
        status_text.value = "DiyarBox Hazır!"
        page.update()

    url_input = ft.TextField(
        label="Video Linkini Buraya Yapıştır",
        width=320,
        border_radius=10
    )
    
    status_text = ft.Text("Başlatılıyor...", text_align=ft.TextAlign.CENTER)

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "⚠️ Link boş olamaz!"
                page.update()
                return

            status_text.value = "🔄 İndirme başlatıldı..."
            page.update()

            # Infinix/Android için en stabil yol
            download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'

            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'nocheckcertificate': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "✅ Başarıyla İndirildi!"
            status_text.color = ft.colors.GREEN_400
            url_input.value = ""
        except Exception as ex:
            # Hata oluşursa tam hatayı ekrana yazdır ki görebilelim
            status_text.value = f"❌ Hata: {str(ex)}"
            status_text.color = ft.colors.RED_400
        
        page.update()

    # Ekran Tasarımı
    try:
        page.add(
            ft.Divider(height=40, color="transparent"),
            ft.Icon(ft.icons.ALL_INBOX_ROUNDED, size=60, color=ft.colors.BLUE_400),
            ft.Text("DiyarBox", size=30, weight="bold"),
            ft.Divider(height=20, color="transparent"),
            url_input,
            ft.ElevatedButton(
                "VİDEOYU İNDİR", 
                on_click=download_video,
                width=250,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
            ),
            ft.Divider(height=20, color="transparent"),
            status_text
        )
        startup_check()
    except Exception as e:
        # Eğer sayfa yüklenirken hata verirse bunu gösterir
        page.add(ft.Text(f"Kritik Hata: {traceback.format_exc()}"))

ft.app(target=main)
