import flet as ft

def main(page: ft.Page):
    page.title = "Lawhatul Mafatih Mobile - Font Sizing Board"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # PERBAIKAN UTAMA: Mengunci font agar terbaca sempurna di sistem web browser kawan
    page.fonts = {
        "Uthman Taha": "Uthman Taha_V22.ttf"
    }
    
    # Memaksa seluruh teks di aplikasi otomatis menggunakan font kustom ini
    page.theme = ft.Theme(font_family="Uthman Taha")

    # DATA KAMUS INTEGRAL NOMOR AYAT RASM USMANI (PDF Halaman 1)
    map_nomor_ayat = {
        "1": "\u0661", "2": "\u0662", "3": "\u0663", "4": "\u0664", "5": "\u0665",
        "6": "\u0666", "7": "\u0667", "8": "\u0668", "9": "\u0669", "0": "\u0660"
    }
    
    # [Sisa kode nomor 2 sampai nomor 10 Anda tetap sama persis kawan...]

    # 2. STRUKTUR DATA UTAMA UNTUK MENAMPUNG TEKS INDEPENDEN 5 BARIS LAUH
    isi_lauh = {1: "", 2: "", 3: "", 4: "", 5: ""}
    baris_aktif = 1 
    ukuran_font_lauh = 26 # Ukuran dasar huruf Arab di papan Lauh

    # 3. AREA INPUT INDEPENDENT (Pencegat Sandi Otomatis)
    input_sandi = ft.TextField(
        label=f"Ketik Arab via HP + Klik Tombol Harakat di Bawah",
        autofocus=True,
        shift_enter=True,
        border_color=ft.Colors.GREEN_400,
        focused_border_color=ft.Colors.GREEN_700,
        width=360
    )

    # KAMUS UTAMA TANDA BACA MURNI RASM USMANI VERSI MADINAH
    sandy_map = {
        "ft": "\u064e\u0670", "vv": "\u0651", "vf": "\u0651\u064e", "vk": "\u0651\u0650", 
        "vd": "\u0651\u064f", "ff": "\u064e", "kk": "\u0650", "do": "\u064f", 
        "xx": "\u06e1", "cc": "\u0652", "mm": "\u0653", "hh": "\u0671", 
        "yy": "\u06e6", "uu": "\u06e5",
        "fn": "\u064b", "kn": "\u064d", "dn": "\u064c", 
        "fj": "\u064e\u064e", "kj": "\u0650\u0650", "dj": "\u065e",
        "ss": "\u06d6", "qq": "\u06d7", "jj": "\u06da", "ll": "\u06d8", 
        "ww": "\u06dc", "__": "\u06e4", "as": "\u06e9"
    }

    # 4. JANTUNG METODE: Mesin Pencegat Kombinasi Tanda Baca Murni Mushaf Madinah
    def mesin_sandi_otomatis(e):
        nonlocal baris_aktif
        teks = input_sandi.value
        if not teks: return

        for sandi, karakter in sandy_map.items():
            if teks.endswith(sandi):
                input_sandi.value = teks[:-2] + karakter
                input_sandi.update()
                isi_lauh[baris_aktif] = input_sandi.value
                perbarui_papan_lauh()
                return

        if teks[-1] in map_nomor_ayat:
            input_sandi.value = teks[:-1] + map_nomor_ayat[teks[-1]]
            input_sandi.update()
            isi_lauh[baris_aktif] = input_sandi.value
            perbarui_papan_lauh()
            return

        isi_lauh[baris_aktif] = teks
        perbarui_papan_lauh()

    input_sandi.on_change = mesin_sandi_otomatis

    komponen_teks_arab = {}
    komponen_baris_container = {}

    # 5. VISUALISASI LAYOUT LAUH (2 Kolom: Teks Kiri & Nomor Urut Kanan Murni RTL)
    daftar_baris_visual = []
    for i in range(1, 6):
        komponen_teks_arab[i] = ft.Text(
            value="", font_family="Uthman Taha", size=ukuran_font_lauh, 
            text_align=ft.TextAlign.RIGHT, no_wrap=True 
        )
        
        komponen_baris_container[i] = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(controls=[komponen_teks_arab[i]], alignment=ft.MainAxisAlignment.END, scroll=ft.ScrollMode.ADAPTIVE),
                        expand=True, padding=ft.Padding(left=10, right=10, top=0, bottom=0), alignment=ft.Alignment(1.0, 0.0) 
                    ),
                    ft.Container(
                        content=ft.Text(f"{i}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_800),
                        alignment=ft.Alignment(0.0, 0.0), width=35, height=50, bgcolor=ft.Colors.GREEN_50, border_radius=4
                    ),
                ]
            ),
            border=ft.Border(bottom=ft.BorderSide(1.5, ft.Colors.GREY_300)), padding=5, bgcolor=ft.Colors.WHITE
        )
        daftar_baris_visual.append(komponen_baris_container[i])

    papan_lauh_container = ft.Column(controls=daftar_baris_visual, spacing=0)

    # 6. FUNGSI UNTUK REFRESH TAMPILAN PAPAN LAUH DIGITAL + UPDATE UKURAN FONT
    def perbarui_papan_lauh():
        for i in range(1, 6):
            komponen_teks_arab[i].value = isi_lauh[i]
            komponen_teks_arab[i].size = ukuran_font_lauh
            if i == baris_aktif:
                komponen_baris_container[i].bgcolor = ft.Colors.YELLOW_50
            else:
                komponen_baris_container[i].bgcolor = ft.Colors.WHITE
        page.update()

    # 7. NAVIGASI PINDAH BARIS
    def ganti_baris(e):
        nonlocal baris_aktif
        baris_aktif = int(e.control.key)
        input_sandi.label = f"Ketik Sandi untuk Baris {baris_aktif} di Sini"
        input_sandi.value = isi_lauh[baris_aktif] 
        input_sandi.focus()
        perbarui_papan_lauh()

    navigasi_baris = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.TextButton(
                content=ft.Text(f"Baris {i}", color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD), 
                key=str(i), on_click=ganti_baris
            )
            for i in range(1, 6)
        ]
    )

    # 7B. FITUR BARU: FUNGSI TOMBOL AKSI PENGUBAH UKURAN HURUF PAPAN LAUH
    def perbesar_font(e):
        nonlocal ukuran_font_lauh
        if ukuran_font_lauh < 50:
            ukuran_font_lauh += 4
            perbarui_papan_lauh()

    def perkecil_font(e):
        nonlocal ukuran_font_lauh
        if ukuran_font_lauh > 18:
            ukuran_font_lauh -= 4
            perbarui_papan_lauh()

    panel_pengatur_font = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER, spacing=15,
        controls=[
            ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_color=ft.Colors.GREEN_700, icon_size=28, on_click=perkecil_font),
            ft.Text("Ukuran Tulisan Lauh", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
            ft.IconButton(icon=ft.Icons.ADD_CIRCLE_OUTLINE, icon_color=ft.Colors.GREEN_700, icon_size=28, on_click=perbesar_font)
        ]
    )

    # 8. AKSI KETIKA TOMBOL KEYBOARD VISUAL DIKLIK
    def tombol_keyboard_diklik(e):
        karakter_unicode = e.control.key
        
        # LOGIKA BARU: Jika tombol yang diklik adalah BACKSPACE kustom kawan
        if karakter_unicode == "BACKSPACE":
            if input_sandi.value:
                # Memotong 1 karakter paling terakhir dari kanan kawan
                input_sandi.value = input_sandi.value[:-1]
        else:
            # Jika tombol harakat biasa, tambahkan karakternya seperti biasa
            input_sandi.value = (input_sandi.value or "") + karakter_unicode
            
        input_sandi.update()
        isi_lauh[baris_aktif] = input_sandi.value
        perbarui_papan_lauh()
        input_sandi.focus()

    def buat_tombol_key(label, unicode_key, warna_bg, warna_teks=ft.Colors.BLACK):
        return ft.Container(
            content=ft.Text(label, size=24, weight=ft.FontWeight.BOLD, color=warna_teks, font_family="Uthman Taha"),
            alignment=ft.Alignment(0.0, 0.0), width=64, height=42, bgcolor=warna_bg, border_radius=6,
            key=unicode_key, on_click=tombol_keyboard_diklik
        )
    # 9. STRUKTUR KEYBOARD VISUAL MATRIKS 20 KEYS
    keyboard_visual_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER, spacing=6,
                    controls=[
                        buat_tombol_key("َٰ", sandy_map["ft"], ft.Colors.GREEN_100, ft.Colors.GREEN_900), 
                        buat_tombol_key("َ", sandy_map["ff"], ft.Colors.GREY_200),
                        buat_tombol_key("ِ", sandy_map["kk"], ft.Colors.GREY_200),
                        buat_tombol_key("ُ", sandy_map["do"], ft.Colors.GREY_200),
                        buat_tombol_key("ۡ", sandy_map["xx"], ft.Colors.GREEN_200, ft.Colors.GREEN_900), 
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER, spacing=6,
                    controls=[
                        buat_tombol_key("ّ", sandy_map["vv"], ft.Colors.ORANGE_50),
                        buat_tombol_key("َّ", sandy_map["vf"], ft.Colors.ORANGE_50),
                        buat_tombol_key("ِّ", sandy_map["vk"], ft.Colors.ORANGE_50),
                        buat_tombol_key("ُّ", sandy_map["vd"], ft.Colors.ORANGE_50),
                        buat_tombol_key("ٓ", sandy_map["mm"], ft.Colors.BLUE_50), 
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER, spacing=6,
                    controls=[
                        buat_tombol_key("ً", sandy_map["fn"], ft.Colors.PURPLE_50),   
                        buat_tombol_key("ٍ", sandy_map["kn"], ft.Colors.PURPLE_50),   
                        buat_tombol_key("ََ", sandy_map["fj"], ft.Colors.PURPLE_100), 
                        buat_tombol_key("ِِ", sandy_map["kj"], ft.Colors.PURPLE_100), 
                        buat_tombol_key("ٌ", sandy_map["dn"], ft.Colors.PURPLE_50),   
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER, spacing=6,
                    controls=[
                        buat_tombol_key("ج", sandy_map["jj"], ft.Colors.BLUE_50),
                        buat_tombol_key("قلى", sandy_map["qq"], ft.Colors.BLUE_50), 
                        buat_tombol_key("صلى", sandy_map["ss"], ft.Colors.BLUE_50), 
                        buat_tombol_key("۩", sandy_map["as"], ft.Colors.RED_50, ft.Colors.RED_800), 
                        buat_tombol_key("ۦ", sandy_map["yy"], ft.Colors.AMBER_100, ft.Colors.AMBER_900), 
                    ]
                )
            ]
        ),
        padding=10, bgcolor=ft.Colors.GREY_100, border_radius=12, width=360
    )
    # 10. FUNGSI SYSTEM ACTION UTAMA (CLIPBOARD & UTILITIES)
    def salin_ke_clipboard(e):
        teks_gabungan = ""
        for i in range(1, 6):
            if isi_lauh[i].strip(): 
                teks_gabungan += f"{isi_lauh[i]}\n"
        if teks_gabungan:
            page.set_clipboard_data(teks_gabungan.strip())
            sb = ft.SnackBar(content=ft.Text("Masya Allah! Semua baris berhasil disalin kawan.", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.GREEN_700)
            page.overlay.append(sb)
            sb.open = True
        else:
            sb = ft.SnackBar(content=ft.Text("Papan Lauh masih kosong kawan.", weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.RED_600)
            page.overlay.append(sb)
            sb.open = True
        page.update()

    # DI SINI BATAS PERUBAHANNYA: Mengarah langsung ke file PDF di folder assets kawan
    def buka_panduan_pdf(e):
        url_panduan = "/panduan-madinah.pdf"
        page.launch_url(url_panduan)

    def hapus_semua(e):
        nonlocal baris_aktif
        for i in range(1, 6): 
            isi_lauh[i] = ""
        baris_aktif = 1
        input_sandi.value = ""
        input_sandi.label = "Ketik Sandi untuk Baris 1 di Sini"
        perbarui_papan_lauh()

    btn_reset = ft.IconButton(icon=ft.Icons.DELETE_SWEEP, icon_color=ft.Colors.RED_400, icon_size=32, on_click=hapus_semua)

    perbarui_papan_lauh()

    # 11. SUSUN STRUKTUR SEMUA KOMPONEN KE TAMPILAN LAYAR SECARA VERTIKAL LURUS
    page.add(
        ft.Container(height=10),
        ft.Text("لوحة المفاتيح", size=28, font_family="Uthman Taha", color=ft.Colors.GREEN_800),
        ft.Text("LAWHATUL MAFATIH - DIGITAL LAUH", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_600),
        ft.Container(height=10),
        ft.Container(
            content=papan_lauh_container, 
            border=ft.Border(top=ft.BorderSide(1, ft.Colors.GREEN_600), bottom=ft.BorderSide(1, ft.Colors.GREEN_600)), 
            width=360, 
            bgcolor=ft.Colors.WHITE
        ),
        ft.Container(height=5),
        navigasi_baris, 
        ft.Container(height=5),
        input_sandi,    
        ft.Container(height=5),
        
        panel_pengatur_font,
        ft.Container(height=5),
        
        keyboard_visual_container,
        ft.Container(height=10),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                # PERBAIKAN FINAL: Menggunakan ElevatedButton stabil dengan fungsi URL langsung kawan
                ft.ElevatedButton(
                    content=ft.Text("PDF Panduan Madinah", color=ft.Colors.GREEN_800, weight=ft.FontWeight.BOLD), 
                    icon=ft.Icons.PICTURE_AS_PDF, 
                    icon_color=ft.Colors.RED_ACCENT, 
                    bgcolor=ft.Colors.GREEN_50,
                    url="/panduan-madinah.pdf"
                ),
                ft.VerticalDivider(width=5),
                ft.ElevatedButton(
                    content=ft.Text("Salin Hasil Lauh", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD), 
                    icon=ft.Icons.COPY_ALL, 
                    icon_color=ft.Colors.WHITE, 
                    bgcolor=ft.Colors.GREEN_600, 
                    on_click=salin_ke_clipboard
                ),
                ft.VerticalDivider(width=5),
                btn_reset
            ]
        )
    )

# Baris eksekusi aplikasi untuk mengaktifkan folder server aset internal kawan
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080, assets_dir="assets")

