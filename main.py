import os
import ssl
import flet as ft
import yt_dlp
import traceback

# SSL Sertifika hatasını bypass et
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    # En temel sayfa ayarları
    page.title = "DiyarBox"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    # Durum mesajı (Sistemin çalıştığını anlamak için)
    status_text = ft.Text("DiyarBox Başlatıldı...", color=ft.colors.GREEN_200)
    
    # Link giriş kutusu (En sade haliyle)
    url_input = ft.TextField(
        label="Video Linki (YT, TikTok, IG)",
        width=300,
        border_radius=10
    )

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "⚠️ Link girmediniz!"
                status_text.color = ft.colors.AMBER_400
                page.update()
                return

            status_text.value = "⏳ İndiriliyor... Lütfen bekleyin."
            status_text.color = ft.colors.BLUE_400
            page.update()

            # Android için kesin ve güvenli yol
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
            # Hata olursa ekranda göster
            status_text.value = f"❌ Hata: {str(ex)[:100]}"
            status_text.color = ft.colors.RED_400
        
        page.update()

    # Arayüz oluşturma (Hata yakalayıcı içine alındı)
    try:
        page.add(
            ft.Column(
                [
                    ft.Divider(height=40, color="transparent"),
                    ft.Text("DiyarBox", size=35, weight="bold"),
                    ft.Text("Multi-Downloader", size=14, color=ft.colors.GREY_500),
                    ft.Divider(height=20, color="transparent"),
                    url_input,
                    ft.ElevatedButton(
                        "İNDİRMEYİ BAŞLAT", 
                        on_click=download_video, 
                        width=300,
                        height=50
                    ),
                    ft.Divider(height=20, color="transparent"),
                    status_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    except Exception as fatal:
        # Eğer uygulama hiç açılmazsa hatayı metin olarak ekrana basar
        page.add(ft.Text(f"Başlatma Hatası: {traceback.format_exc()}"))

ft.app(target=main)
