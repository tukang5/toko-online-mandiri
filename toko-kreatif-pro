import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# ==========================================
# 1. KONFIGURASI AWAL & DATA DEFAULT TOKO
# ==========================================
st.set_page_config(page_title="Toko Online Pro & Landing Page", page_icon="💰", layout="wide")

# ------------------------------------------
# HACK CSS: MENYEMBUNYIKAN SEMUA ATRIBUT STREAMLIT (WHITE LABEL)
# ------------------------------------------
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            #stDecoration {display:none;}
            [data-testid="stHeader"] {background-color: rgba(0,0,0,0); height: 0rem;}
            .viewerBadge_container__1QS1h {display: none !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Data bawaan (Default) sebelum diubah oleh Admin di dashboard
DEFAULT_META_ID = "NOMOR_PIXEL_META_ANDA"
DEFAULT_TIKTOK_ID = "NOMOR_PIXEL_TIKTOK_ANDA"
DEFAULT_WA = "6281234567890"

# Memastikan data live selalu sinkron dengan input dari Halaman Admin
if "meta_id_live" not in st.session_state:
    st.session_state["meta_id_live"] = DEFAULT_META_ID
if "tiktok_id_live" not in st.session_state:
    st.session_state["tiktok_id_live"] = DEFAULT_TIKTOK_ID
if "wa_live" not in st.session_state:
    st.session_state["wa_live"] = DEFAULT_WA

# Ambil nilai aktif yang sedang digunakan
ACTIVE_META_ID = st.session_state["meta_id_live"]
ACTIVE_TIKTOK_ID = st.session_state["tiktok_id_live"]
ACTIVE_WA = st.session_state["wa_live"]

# ==========================================
# 2. SISTEM PELACAKAN PIXEL (HTML INJECTION)
# ==========================================
def inject_pixels_base():
    """Menyuntikkan script dasar Meta & TikTok Pixel ke latar belakang aplikasi"""
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
    
    <!-- TikTok Pixel Code -->
    <script>
    !function (w, d, t) {{
      w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"],ttq.setAndDefer=function(t,e){{t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){{for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e}},ttq.load=function(e,n){{var r="https://tiktok.com",o=n&&n.mixpool;ttq._i=ttq._i||{{}},ttq._i[e]=[],ttq._i[e]._u=r,w[t]._v="1.3.1",w[t]._i=ttq._i,w[t]._a="c7d",var a=d.createElement("script");a.type="text/javascript",a.async=!0,a.src=r;var c=d.getElementsByTagName("script");c.parentNode.insertBefore(a,c)}};
      ttq.load('{ACTIVE_TIKTOK_ID}');
      ttq.page();
    }}(window, document, 'ttq');
    </script>
    """
    components.html(pixel_code, height=0)

def track_pixel_event(event_name, prod_name, value):
    """Memicu event konversi spesifik (AddToCart / Purchase) ke Meta & TikTok"""
    event_code = f"""
    <script>
    parent.fbq('track', '{event_name}', {{content_names: ['{prod_name}'], value: {value}, currency: 'IDR'}});
    parent.ttq.track('{event_name}', {{content_name: ['{prod_name}'], value: {value}, currency: 'IDR'}});
    </script>
    """
    components.html(event_code, height=0)
    st.toast(f"📡 Pixel Event Sent: {event_name} for {prod_name}", icon="📈")

# Jalankan skrip pelacakan dasar di latar belakang
inject_pixels_base()

# ==========================================
# 3. DATABASE PRODUK LOKAL
# ==========================================
products = {
    "fisik": {
        "nama": "Smart Tumbler LED Premium",
        "harga": 149000,
        "deskripsi": "Tumbler stainless steel anti karat dengan pengukur suhu otomatis pada tutupnya. Menjaga suhu air panas/dingin hingga 12 jam.",
        "gambar": "https://unsplash.com",
        "qris_mock": "https://wikimedia.org"
    },
    "digital": {
        "nama": "E-Book Masterclass Content Creator 2026",
        "harga": 99000,
        "deskripsi": "Strategi lengkap membangun personal branding & menghasilkan jutaan rupiah dari media sosial tanpa modal besar.",
        "gambar": "https://unsplash.com",
        "qris_mock": "https://wikimedia.org"
    }
}

# ==========================================
# 4. NAVIGASI SIDEBAR
# ==========================================
st.sidebar.title("📌 Menu Navigasi")
halaman = st.sidebar.radio("Pilih Halaman:", ["Landing Page (Promo)", "Halaman Check-out Langsung", "⚙️ Pengaturan Admin (Rahasia)"])

# --- HALAMAN 1: LANDING PAGE ---
if halaman == "Landing Page (Promo)":
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🚀 PROMO SPESIAL HARI INI 🚀</h1>", unsafe_allow_html=True)
    st.divider()

    # Produk Fisik Section
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(products["fisik"]["gambar"], use_column_width=True)
    with col2:
        st.markdown(f"## ⭐ {products['fisik']['nama']}")
        st.markdown(f"<h3 style='color: #E53935;'>Harga Hari Ini: Rp {products['fisik']['harga']:,}</h3>", unsafe_allow_html=True)
        st.write(products["fisik"]["deskripsi"])
        
        if st.button("BELI PRODUK FISIK SEKARANG 🛒", key="btn_lp_fisik", type="primary"):
            track_pixel_event("AddToCart", products["fisik"]["nama"], products["fisik"]["harga"])
            st.session_state["produk_pilihan"] = "fisik"
            st.success("Produk dipilih! Silakan masuk ke menu 'Halaman Check-out Langsung' di sebelah kiri untuk membayar.")

    st.divider()

    # Produk Digital Section
    col3, col4 = st.columns([1, 1.2])
    with col3:
        st.image(products["digital"]["gambar"], use_column_width=True)
    with col4:
        st.markdown(f"## ⚡ {products['digital']['nama']}")
        st.markdown(f"<h3 style='color: #E53935;'>Harga Hari Ini: Rp {products['digital']['harga']:,}</h3>", unsafe_allow_html=True)
        st.write(products["digital"]["deskripsi"])
        
        if st.button("AMBIL E-BOOK DIGITAL ⚡", key="btn_lp_digital", type="primary"):
            track_pixel_event("AddToCart", products["digital"]["nama"], products["digital"]["harga"])
            st.session_state["produk_pilihan"] = "digital"
            st.success("Produk dipilih! Silakan masuk ke menu 'Halaman Check-out Langsung' di sebelah kiri untuk membayar.")

# --- HALAMAN 2: CHECK-OUT & PEMBAYARAN ---
elif halaman == "Halaman Check-out Langsung":
    st.title("💳 Halaman Check-out & Pembayaran")
    
    pilihan = st.session_state.get("produk_pilihan", "fisik")
    produk_terpilih = products[pilihan]
    
    st.info(f"Produk yang akan Anda beli: **{produk_terpilih['nama']}** — Rp {produk_terpilih['harga']:,}")
    
    st.subheader("📋 Isi Data Pengiriman")
    nama_pembeli = st.text_input("Nama Lengkap:")
    email_pembeli = st.text_input("Alamat Email:")
    alamat_pembeli = st.text_area("Alamat Lengkap (Kosongkan jika produk digital):")
    
    st.subheader("💵 Pilih Metode Pembayaran")
    metode_bayar = st.radio("Metode:", ["QRIS Otomatis", "Check-out via WhatsApp"])
    
    if metode_bayar == "QRIS Otomatis":
        st.write("Silakan scan QRIS di bawah ini dengan E-Wallet/Mobile Banking Anda:")
        st.image(produk_terpilih["qris_mock"], width=250)
        
        if st.button("Konfirmasi Pembayaran Selesai ✅", type="primary"):
            if nama_pembeli and email_pembeli:
                track_pixel_event("Purchase", produk_terpilih["nama"], produk_terpilih["harga"])
                st.balloons()
                st.success(f"Terima kasih {nama_pembeli}! Pembayaran berhasil. Detail pesanan terkirim otomatis ke sistem.")
            else:
                st.warning("Mohon isi Nama Lengkap dan Email terlebih dahulu!")
                
    elif metode_bayar == "Check-out via WhatsApp":
        pesan_text = f"Halo Admin Toko, saya mau beli:\n\n" \
                     f"📦 Produk: {produk_terpilih['nama']}\n" \
                     f"💰 Total: Rp {produk_terpilih['harga']:,}\n\n" \
                     f"👤 Nama: {nama_pembeli}\n" \
                     f"📧 Email: {email_pembeli}\n" \
                     f"🏠 Alamat: {alamat_pembeli if alamat_pembeli else 'Produk Digital'}"
                     
        pesan_encode = urllib.parse.quote(pesan_text)
        tautan_wa = f"https://wa.me{ACTIVE_WA}?text={pesan_encode}"
        
        st.markdown(f'<a href="{tautan_wa}" target="_blank"><button style="background-color: #25D366; color: white; border: none; padding: 12px 24px; font-size: 16px; border-radius: 5px; cursor: pointer;">💬 Kirim Pesanan ke WhatsApp Admin</button></a>', unsafe_allow_html=True)
        track_pixel_event("InitiateCheckout", produk_terpilih["nama"], produk_terpilih["harga"])

# --- HALAMAN 3: DASHBOARD ADMIN (UNTUK PEMBELI TOKO) ---
elif halaman == "⚙️ Pengaturan Admin (Rahasia)":
    st.title("⚙️ Dashboard Pengaturan Pemilik Toko")
    st.write("Ubah ID pelacakan iklan dan nomor tujuan WhatsApp di sini tanpa perlu membongkar coding.")
    st.divider()
    
