import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# ==========================================
# 1. KONFIGURASI AWAL & DATA DEFAULT TOKO
# ==========================================
st.set_page_config(page_title="Toko Online Pro & Landing Page", page_icon="💰", layout="wide")

# HACK CSS VERSI HP: MENYEMBUNYIKAN ATRIBUT STREAMLIT DENGAN AMAN
hide_streamlit_style = """
            <style>
            #MainMenu, footer, header, #stDecoration, [data-testid="stHeader"], .viewerBadge_container__1QS1h {
                visibility: hidden !important;
                opacity: 0 !important;
                pointer-events: none !important;
                height: 0px !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------------------------------
# INISIALISASI DATABASE DENGAN NAMA 100% NETRAL (SIAP JUAL)
# ------------------------------------------
if "prod_fisik_nama" not in st.session_state:
    st.session_state["prod_fisik_nama"] = "Nama Produk Fisik Anda di Sini"
if "prod_fisik_harga" not in st.session_state:
    st.session_state["prod_fisik_harga"] = 0
if "prod_fisik_desc" not in st.session_state:
    st.session_state["prod_fisik_desc"] = "Silakan masuk ke menu 'Pengaturan Admin (Rahasia)' untuk mengganti nama, harga, deskripsi, dan foto produk fisik ini dengan milik Anda sendiri."
if "prod_fisik_img" not in st.session_state:
    st.session_state["prod_fisik_img"] = "https://unsplash.com" # Gambar placeholder netral

if "prod_digi_nama" not in st.session_state:
    st.session_state["prod_digi_nama"] = "Nama Produk Digital Anda di Sini"
if "prod_digi_harga" not in st.session_state:
    st.session_state["prod_digi_harga"] = 0
if "prod_digi_desc" not in st.session_state:
    st.session_state["prod_digi_desc"] = "Silakan masuk ke menu 'Pengaturan Admin (Rahasia)' untuk mengganti nama, harga, deskripsi, dan foto produk digital ini dengan milik Anda sendiri."
if "prod_digi_img" not in st.session_state:
    st.session_state["prod_digi_img"] = "https://unsplash.com" # Gambar placeholder netral

# Data Pixel & WhatsApp Default
if "meta_id_live" not in st.session_state:
    st.session_state["meta_id_live"] = "NOMOR_PIXEL_META_ANDA"
if "tiktok_id_live" not in st.session_state:
    st.session_state["tiktok_id_live"] = "NOMOR_PIXEL_TIKTOK_ANDA"
if "wa_live" not in st.session_state:
    st.session_state["wa_live"] = "6281234567890"

# Menghubungkan variabel aktif dengan session state
ACTIVE_META_ID = st.session_state["meta_id_live"]
ACTIVE_TIKTOK_ID = st.session_state["tiktok_id_live"]
ACTIVE_WA = st.session_state["wa_live"]

# ==========================================
# 2. SISTEM PELACAKAN PIXEL (HTML INJECTION)
# ==========================================
def inject_pixels_base():
    pixel_code = f"""
    <!-- Meta Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e);
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://facebook.net');
    fbq('init', '{ACTIVE_META_ID}');
    fbq('track', 'PageView');
    </script>
    """
    components.html(pixel_code, height=0)

def track_pixel_event(event_name, prod_name, value):
    event_code = f"""
    <script>
    parent.fbq('track', '{event_name}', {{content_names: ['{prod_name}'], value: {value}, currency: 'IDR'}});
    </script>
    """
    components.html(event_code, height=0)
    st.toast(f"📡 Pixel Event Sent: {event_name}", icon="📈")

inject_pixels_base()

# ==========================================
# 3. NAVIGASI SIDEBAR
# ==========================================
st.sidebar.title("📌 Menu Navigasi")
halaman = st.sidebar.radio("Pilih Halaman:", ["Landing Page (Promo)", "Halaman Check-out Langsung", "⚙️ Pengaturan Admin (Rahasia)"])

# --- HALAMAN 1: LANDING PAGE ---
if halaman == "Landing Page (Promo)":
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🚀 PROMO SPESIAL HARI INI 🚀</h1>", unsafe_allow_html=True)
    st.divider()

    # Tampilkan Produk Fisik
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(st.session_state["prod_fisik_img"], use_container_width=True)
    with col2:
        st.markdown(f"## ⭐ {st.session_state['prod_fisik_nama']}")
        st.markdown(f"<h3 style='color: #E53935;'>Harga Hari Ini: Rp {st.session_state['prod_fisik_harga']:,}</h3>", unsafe_allow_html=True)
        st.write(st.session_state["prod_fisik_desc"])
        
        if st.button("BELI PRODUK FISIK SEKARANG 🛒", key="btn_lp_phys_v3", type="primary"):
            track_pixel_event("AddToCart", st.session_state["prod_fisik_nama"], st.session_state["prod_fisik_harga"])
            st.session_state["produk_pilihan"] = "fisik"
            st.success("Produk dipilih! Silakan masuk ke menu 'Halaman Check-out Langsung' di sebelah kiri.")

    st.divider()

    # Tampilkan Produk Digital
    col3, col4 = st.columns([1, 1.2])
    with col3:
        st.image(st.session_state["prod_digi_img"], use_container_width=True)
    with col4:
        st.markdown(f"## ⚡ {st.session_state['prod_digi_nama']}")
        st.markdown(f"<h3 style='color: #E53935;'>Harga Hari Ini: Rp {st.session_state['prod_digi_harga']:,}</h3>", unsafe_allow_html=True)
        st.write(st.session_state["prod_digi_desc"])
        
        if st.button("AMBIL PRODUK DIGITAL ⚡", key="btn_lp_digi_v3", type="primary"):
            track_pixel_event("AddToCart", st.session_state["prod_digi_nama"], st.session_state["prod_digi_harga"])
            st.session_state["produk_pilihan"] = "digital"
            st.success("Produk dipilih! Silakan masuk ke menu 'Halaman Check-out Langsung' di sebelah kiri.")

# --- HALAMAN 2: CHECK-OUT & PEMBAYARAN ---
elif halaman == "Halaman Check-out Langsung":
    st.title("💳 Halaman Check-out & Pembayaran")
    
    pilihan = st.session_state.get("produk_pilihan", "fisik")
    
    if pilihan == "fisik":
        nama_p = st.session_state["prod_fisik_nama"]
        harga_p = st.session_state["prod_fisik_harga"]
    else:
        nama_p = st.session_state["prod_digi_nama"]
        harga_p = st.session_state["prod_digi_harga"]
        
    st.info(f"Produk yang akan Anda beli: **{nama_p}** — Rp {harga_p:,}")
    
    st.subheader("📋 Isi Data Pengiriman")
    nama_pembeli = st.text_input("Nama Lengkap:")
    email_pembeli = st.text_input("Alamat Email:")
    alamat_pembeli = st.text_area("Alamat Lengkap:")
    
    st.subheader("💵 Pilih Metode Pembayaran")
    metode_bayar = st.radio("Metode:", ["QRIS Otomatis", "Check-out via WhatsApp"])
    
    if metode_bayar == "QRIS Otomatis":
        st.write("Silakan scan QRIS di bawah ini dengan E-Wallet/Mobile Banking Anda:")
        st.image("https://wikimedia.org", width=250)
        
        if st.button("Konfirmasi Pembayaran Selesai ✅", type="primary"):
            if nama_pembeli and email_pembeli:
                track_pixel_event("Purchase", nama_p", harga_p)
                st.balloons()
                st.success(f"Terma kasih {nama_pembeli}! Pembayaran berhasil.")
            else:
                st.warning("Mohon isi Nama Lengkap dan Email terlebih dahulu!")
                
    elif metode_bayar == "Check-out via WhatsApp":
        pesan_text = f"Halo Admin Toko, saya mau beli:\n\n📦 Produk: {nama_p}\n💰 Total: Rp {harga_p:,}\n\n👤 Nama: {nama_pembeli}\n📧 Email: {email_pembeli}"
        pesan_encode = urllib.parse.quote(pesan_text)
        tautan_wa = f"https://wa.me{ACTIVE_WA}?text={pesan_encode}"
        
        st.markdown(f'<a href="{tautan_wa}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 5px; cursor: pointer;">💬 Kirim Pesanan ke WhatsApp Admin</button></a>', unsafe_allow_html=True)

# --- HALAMAN 3: DASHBOARD ADMIN (KELOLA TOTAL INTERFACES) ---
elif halaman == "⚙️ Pengaturan Admin (Rahasia)":
    st.title("⚙️ Dashboard Pengaturan Pemilik Toko")
    st.write("Kelola produk, ubah nomor WhatsApp, dan atur ID Pixel tanpa menyentuh coding.")
    st.divider()
    
    # BAGIAN A: PENGATURAN PRODUK FISIK
    st.subheader("📦 1. Kelola Produk Fisik")
    edit_f_nama = st.text_input("Nama Produk Fisik:", value=st.session_state["prod_fisik_nama"])
    edit_f_harga = st.number_input("Harga Produk Fisik (Rupiah):", value=st.session_state["prod_fisik_harga"], step=1000)
    edit_f_desc = st.text_area("Deskripsi Produk Fisik:", value=st.session_state["prod_fisik_desc"])
    edit_f_img = st.text_input("URL Link Foto Produk Fisik:", value=st.session_state["prod_fisik_img"])
    
    st.divider()
    
    # BAGIAN B: PENGATURAN PRODUK DIGITAL
    st.subheader("⚡ 2. Kelola Produk Digital")
    edit_d_nama = st.text_input("Nama Produk Digital:", value=st.session_state["prod_digi_nama"])
    edit_d_harga = st.number_input("Harga Produk Digital (Rupiah):", value=st.session_state["prod_digi_harga"], step=1000)
    edit_d_desc = st.text_area("Deskripsi Produk Digital:", value=st.session_state["prod_digi_desc"])
    edit_d_img = st.text_input("URL Link Foto Produk Digital:", value=st.session_state["prod_digi_img"])
    
    st.divider()
    
    # BAGIAN C: PENGATURAN UTILITAS KONEKSI
    st.subheader("🔗 3. Pengaturan Kontak & Iklan")
    input_meta = st.text_input("Meta Pixel ID Aktif:", value=ACTIVE_META_ID)
    input_tiktok = st.text_input("TikTok Pixel ID Aktif:", value=ACTIVE_TIKTOK_ID)
    input_wa = st.text_input("Nomor WhatsApp Toko (Gunakan format 62):", value=ACTIVE_WA)
    
    if st.button("Simpan Semua Perubahan Toko 💾", type="primary"):
