import os
import ssl
import flet as ft
import yt_dlp

# SSL Sertifika hatalarını kökten çözelim
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "DiyarBox"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Giriş Alanı
    url_input = ft.TextField(
        label="Video Linkini Buraya Yapıştır",
        hint_text="YouTube, TikTok, Instagram...",
        width=320,
        border_radius=10,
        border_color=ft.colors.BLUE_400
    )
    
    status_text = ft.Text("DiyarBox Kullanıma Hazır", text_align=ft.TextAlign.CENTER)

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "⚠️ Link boş olamaz!"
                page.update()
                return

            status_text.value = "🔄 İndirme başlatıldı... Lütfen bekleyin."
            status_text.color = ft.colors.BLUE_200
            page.update()

            # Android için en garanti indirme yolu
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
            status_text.value = f"❌ Hata: {str(ex)[:100]}"
            status_text.color = ft.colors.RED_400
        
        page.update()

    # Arayüz (Hatalı İkon Kaldırıldı, Standart İkon Eklendi)
    page.add(
        ft.Divider(height=40, color="transparent"),
        # Hata veren ALL_INBOX_ROUNDED yerine en standart FILE_DOWNLOAD kullanıyoruz
        ft.Icon(ft.icons.FILE_DOWNLOAD, size=60, color=ft.colors.BLUE_400),
        ft.Text("DiyarBox", size=30, weight="bold"),
        ft.Text("Infinix Hot 30 Edition", size=12, color=ft.colors.GREY_500),
        ft.Divider(height=20, color="transparent"),
        url_input,
        ft.ElevatedButton(
            "İNDİR", 
            on_click=download_video,
            width=250,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        ft.Divider(height=20, color="transparent"),
        status_text
    )

ft.app(target=main)
