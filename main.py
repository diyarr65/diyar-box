import os
import ssl
import flet as ft
import yt_dlp

# SSL Sertifika Sorunlarını Giderme
ssl._create_default_https_context = ssl._create_unverified_context

def main(page: ft.Page):
    # Sayfa Genel Ayarları
    page.title = "DiyarBox"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 400
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # İndirme Fonksiyonu
    def download_video(e):
        if not url_input.value:
            status_text.value = "⚠️ Lütfen bir link yapıştırın!"
            status_text.color = ft.colors.AMBER_400
            page.update()
            return

        try:
            # Görsel Geri Bildirim: Butonu devre dışı bırak ve yükleniyor göster
            download_btn.disabled = True
            progress_bar.visible = True
            status_text.value = "🔄 Video işleniyor..."
            status_text.color = ft.colors.BLUE_200
            page.update()

            # Android İndirme Yolu
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
            status_text.color = ft.colors.GREEN_ACCENT_400
            url_input.value = "" # Girişi temizle
            
        except Exception as ex:
            status_text.value = f"❌ Hata: {str(ex)[:50]}..."
            status_text.color = ft.colors.RED_400
        
        finally:
            download_btn.disabled = False
            progress_bar.visible = False
            page.update()

    # Arayüz Elemanları
    url_input = ft.TextField(
        label="Video Linki",
        hint_text="YouTube, TikTok, Instagram...",
        prefix_icon=ft.icons.LINK,
        border_radius=15,
        border_color=ft.colors.BLUE_400,
        focused_border_color=ft.colors.BLUE_ACCENT_700,
        width=320,
    )

    download_btn = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.icons.DOWNLOAD), ft.Text("İNDİRMEYİ BAŞLAT", weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_700,
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        width=320,
        height=50,
        on_click=download_video
    )

    status_text = ft.Text("", size=14, italic=True)
    progress_bar = ft.ProgressBar(width=300, color="blue", visible=False)

    # Ana Tasarım (Container ile Arka Plan)
    main_container = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.icons.ALL_INBOX_ROUNDED, size=80, color=ft.colors.BLUE_400),
                ft.Text("DiyarBox", size=32, weight="bold", color=ft.colors.WHITE),
                ft.Text("Çok Amaçlı Medya İndirici", size=14, color=ft.colors.BLUE_100),
                ft.Divider(height=40, color="transparent"),
                url_input,
                ft.Divider(height=10, color="transparent"),
                download_btn,
                ft.Divider(height=20, color="transparent"),
                progress_bar,
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.colors.BLUE_900, ft.colors.BLACK],
        ),
        width=float("inf"),
        height=float("inf"),
        expand=True,
    )

    page.add(main_container)

ft.app(target=main)
