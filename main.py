import os
import ssl
import flet as ft
import yt_dlp

# SSL hatalarını önlemek için
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "Sosyal Medya İndirici"
    page.theme_mode = ft.ThemeMode.DARK # Daha şık görünmesi için karanlık mod
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO # Ekran küçük gelirse kaydırılabilsin

    url_input = ft.TextField(
        label="Video Linkini Buraya Yapıştır",
        hint_text="YouTube, TikTok veya Instagram linki...",
        width=350,
        border_radius=10
    )
    status_text = ft.Text(text_align=ft.TextAlign.CENTER)
    progress_ring = ft.ProgressRing(visible=False) # İndirme yapılırken dönecek simge

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "Lütfen geçerli bir link girin!"
                page.update()
                return

            status_text.value = "Video bilgileri alınıyor ve indirme başlıyor..."
            status_text.color = ft.colors.BLUE_200
            progress_ring.visible = True
            page.update()

            # Android standart indirme klasörü
            download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'

            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'nocheckcertificate': True,
                'quiet': False,
                'no_warnings': True,
                # Instagram ve TikTok için bazen kullanıcı girişi gerekebilir 
                # ama genel videolar için bu ayarlar yeterlidir:
                'add_header': [
                    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                ]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "Başarıyla 'İndirilenler' klasörüne kaydedildi! ✅"
            status_text.color = ft.colors.GREEN_400
        except Exception as ex:
            status_text.value = f"Hata oluştu: {str(ex)}"
            status_text.color = ft.colors.RED_400
        
        progress_ring.visible = False
        page.update()

    # Arayüz Elemanları
    page.add(
        ft.Divider(height=20, color="transparent"),
        ft.Icon(ft.icons.DOWNLOAD_FOR_OFFLINE, size=50, color=ft.colors.BLUE_400),
        ft.Text("Video Downloader", size=28, weight=ft.FontWeight.BOLD),
        ft.Text("YouTube • Instagram • TikTok", size=14, color=ft.colors.GREY_400),
        ft.Divider(height=20, color="transparent"),
        url_input,
        ft.ElevatedButton(
            "Hemen İndir", 
            on_click=download_video,
            style=ft.ButtonStyle(
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        ),
        ft.Divider(height=20, color="transparent"),
        progress_ring,
        status_text
    )

ft.app(target=main)
