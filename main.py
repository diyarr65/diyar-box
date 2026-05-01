import flet as ft

def main(page: ft.Page):
    # Sayfa ayarları
    page.title = "DiyarBox"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Bileşenler
    title = ft.Text("DiyarBox", size=40, weight="bold")
    subtitle = ft.Text("v1.5 - Stable", size=14, color=ft.colors.GREY_500)

    url_input = ft.TextField(
        label="Video Linkini Yapıştır",
        width=320,
        border_radius=10
    )

    status_text = ft.Text(
        "Hazır ✅",
        size=16,
        color=ft.colors.WHITE
    )

    # Buton fonksiyonu
    def download_video(e):
        if not url_input.value:
            status_text.value = "⚠️ Link gir!"
            status_text.color = ft.colors.RED
            page.update()
            return

        # Simülasyon (çökme önlemek için)
        status_text.value = "⏳ İşlem başlatıldı..."
        status_text.color = ft.colors.BLUE
        page.update()

        # Sahte işlem gecikmesi
        import time
        time.sleep(2)

        status_text.value = "✅ İşlem tamamlandı (test)"
        status_text.color = ft.colors.GREEN
        url_input.value = ""
        page.update()

    download_button = ft.ElevatedButton(
        "VİDEOYU İNDİR",
        width=300,
        height=50,
        on_click=download_video
    )

    # Sayfaya ekle
    page.add(
        title,
        subtitle,
        ft.Divider(height=30, color="transparent"),
        url_input,
        download_button,
        ft.Divider(height=20, color="transparent"),
        status_text
    )


# 🔥 KRİTİK SATIR (siyah ekran fix)
ft.app(target=main, view=ft.AppView.FLET_APP)
