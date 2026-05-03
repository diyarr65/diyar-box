import flet as ft
import os
import ssl
import yt_dlp

# SSL Sertifika hatalarını bypass et
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    page.title = "DiyarBox"
    page.theme_mode = "dark"
    page.horizontal_alignment = "center"
    page.scroll = "auto"
    
    # Durum mesajı
    status_text = ft.Text("DiyarBox v1.9 Hazır ✅", size=16, color="white")
    
    # Link giriş kutusu
    url_input = ft.TextField(
        label="Video Linkini Yapıştır",
        hint_text="YouTube, TikTok, Instagram...",
        width=320,
        border_radius=10,
        border_color="blue"
    )

    def download_video(e):
        try:
            if not url_input.value:
                status_text.value = "⚠️ Link girmediniz!"
                status_text.color = "amber"
                page.update()
                return

            status_text.value = "🔄 İşleniyor... Lütfen bekleyin."
            status_text.color = "blue"
            page.update()

            # PC ve Telefon için dinamik yol ayarı
            if os.name == 'nt': 
                download_path = '%(title)s.%(ext)s'
            else: 
                download_path = '/storage/emulated/0/Download/%(title)s.%(ext)s'
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': download_path,
                'nocheckcertificate': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input.value])

            status_text.value = "✅ İndirme Başarılı!"
            status_text.color = "green"
            url_input.value = ""
            
        except Exception as ex:
            status_text.value = f"❌ Hata: {str(ex)[:60]}"
            status_text.color = "red"
        
        page.update()

    # Arayüz - Hata verebilecek tüm ikonları kaldırdık
    page.add(
        ft.Container(height=60),
        ft.Text("📥", size=60), # İkon yerine emoji kullandık, bu asla hata vermez
        ft.Text("DiyarBox", size=40, weight="bold"),
        ft.Text("YT • TikTok • Instagram", size=14, color="grey"),
        ft.Divider(height=30, color="transparent"),
        url_input,
        ft.Container(height=10),
        ft.ElevatedButton(
            "MEDYAYI İNDİR", 
            on_click=download_video, 
            width=300,
            height=55,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        ft.Divider(height=20, color="transparent"),
        status_text
    )

if __name__ == "__main__":
    ft.app(target=main)
