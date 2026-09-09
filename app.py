import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

# ==========================================
# 1. STYLE PREMIUM CERAH & KONTRAS MODERN (WHITE LABEL)
# ==========================================
st.set_page_config(page_title="Premium Checkout Page", page_icon="⚡", layout="centered")

# PERUBAHAN PALET WARNA: Latar belakang putih bersih, tombol Indigo mewah, teks tajam kontras
scalev_theme = """
            <style>
            #MainMenu, footer, header, #stDecoration, [data-testid="stHeader"] {
                visibility: hidden !important; height: 0px !important; opacity: 0 !important;
            }
            /* Latar belakang putih bersih (Bukan abu-abu) */
            .stApp {
                background-color: #FFFFFF;
                font-family: 'Inter', sans-serif;
            }
            /* Tombol Aksi Utama: Indigo / Ungu Royal Mewah */
            div.stButton > button:first-child {
                background-color: #4F46E5 !important;
                color: white !important;
                border-radius: 10px !important;
                width: 100% !important;
                padding: 14px !important;
                font-weight: bold !important;
                font-size: 16px !important;
                border: none !important;
                box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2) !important;
                transition: all 0.2s ease-in-out;
            }
            div.stButton > button:first-child:hover {
                background-color: #4338CA !important;
                box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3) !important;
            }
            /* Kotak Formulir: Putih dengan Border Halus Biru Muda agar Kontras */
            div[data-testid="stBlock"] {
                background-color: #F8FAFC !important;
                padding: 30px !important;
                border-radius: 16px !important;
                border: 1px solid #E2E8F0 !important;
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.02) !important;
                margin-bottom: 25px !important;
            }
            /* Label Teks Input */
            label {
                color: #1E293B !important;
                font-weight: 600 !important;
            }
            </style>
            """
st.markdown(scalev_theme, unsafe_allow_html=True)

PASSWORD_ADMIN_BENAR = "admin123"

# DATABASE STATE UTAMA
if "p_nama" not in st.session_state: st.session_state["p_nama"] = "Smart Tumbler LED Premium"
if "p_harga" not in st.session_state: st.session_state["p_harga"] = 149000
if "p_desc" not in st.session_state: st.session_state["p_desc"] = "Teknologi isolasi vakum dinding ganda menjaga suhu air panas tetap terjaga sepanjang hari."
if "p_img" not in st.session_state: st.session_state["p_img"] = "https://unsplash.com"
if "p_jenis" not in st.session_state: st.session_state["p_jenis"] = "Fisik"

if "meta_id" not in st.session_state: st.session_state["meta_id"] = "ID_PIXEL_DEFAULT"
if "wa_num" not in st.session_state: st.session_state["wa_num"] = "6281234567890"
if "admin_logged_in" not in st.session_state: st.session_state["admin_logged_in"] = False

# PIXEL TRACKING SYSTEM
def inject_pixel():
    html_p = f"""<script>
    !function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e);s.parentNode.insertBefore(t,s)}}(window,document,'script','https://facebook.net');
    fbq('init', '{st.session_state["meta_id"]}'); fbq('track', 'PageView');
    </script>"""
    components.html(html_p, height=0)

def fire_event(e_name):
    js_e = f"""<script>parent.fbq('track', '{e_name}', {{content_names: ['{st.session_state["p_nama"]}'], value: {st.session_state["p_harga"]}, currency: 'IDR'}});</script>"""
    components.html(js_e, height=0)
    st.toast(f"📡 Pixel Tracking: {e_name} Terkirim!", icon="🚀")

inject_pixel()

menu = st.sidebar.radio("Navigasi Toko:", ["🛍️ Lihat Toko (Tampilan Premium)", "⚙️ Pengaturan Toko (Admin)"])
# --- TAMPILAN HALAMAN DEPAN SINGLE-PAGE CHECKOUT ---
if menu == "🛍️ Lihat Toko (Tampilan Premium)":
    # 1. Tampilan Produk & Banner Utama
    st.image(st.session_state["p_img"], use_container_width=True)
    
    st.markdown(f"<h2 style='color: #0F172A; font-weight: 800;'>{st.session_state['p_nama']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #4F46E5; margin-top:-15px; font-weight: 700;'>Rp {st.session_state['p_harga']:,}</h3>", unsafe_allow_html=True)
    st.write(st.session_state["p_desc"])
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2. Kotak Formulir Pembelian Instan
    st.markdown("### 📝 **Formulir Pembelian Instan**")
    st.caption("Silakan isi data lengkap Anda di bawah ini untuk melakukan pemesanan:")
    
    with st.container():
        input_nama = st.text_input("Nama Lengkap Pembeli:")
        input_email = st.text_input("Alamat Email:")
        
        if st.session_state["p_jenis"] == "Fisik":
            input_alamat = st.text_area("Alamat Lengkap Pengiriman:")
        else:
            input_alamat = "Produk Digital (Kirim via Email)"
            
        pilihan_bayar = st.radio("Metode Pembayaran Mandiri:", ["Bayar Otomatis via QRIS", "Selesaikan Transaksi via WhatsApp"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if pilihan_bayar == "Bayar Otomatis via QRIS":
            st.info("Silakan pindai QRIS di bawah ini, kemudian klik tombol Konfirmasi Pembayaran.")
            st.image("https://wikimedia.org", width=220)
            
            if st.button("KONFIRMASI PEMBAYARAN SEKARANG ✅"):
                if input_nama and input_email:
                    fire_event("Purchase")
                    st.balloons()
                    st.success(f"Sukses! Pembayaran {input_nama} diterima. Produk digital/resi pengiriman akan segera dikirim.")
                else:
                    st.error("Gagal! Nama dan Email wajib diisi terlebih dahulu.")
                    
        elif pilihan_bayar == "Selesaikan Transaksi via WhatsApp":
            fire_event("InitiateCheckout")
            
            format_pesan = f"Halo Admin, saya memesan lewat Halaman Instan:\n\n🛍️ Produk: {st.session_state['p_nama']}\n💵 Total: Rp {st.session_state['p_harga']:,}\n\n👤 Nama: {input_nama}\n📧 Email: {input_email}\n🏠 Alamat: {input_alamat}"
            wa_url = f"https://wa.me{st.session_state['wa_num']}?text={urllib.parse.quote(format_pesan)}"
            
            # Tombol WhatsApp khusus dengan warna Hijau Emerald Segar & Kontras Tinggi
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color: #10B981; color: white; border: none; padding: 14px; width:100%; border-radius:10px; font-weight:bold; font-size:16px; box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2); cursor:pointer;">💬 Ambil Orderan via WhatsApp</button></a>', unsafe_allow_html=True)

# --- PANEL MANAJEMEN ADMIN TERKUNCI PASSWORD ---
elif menu == "⚙️ Pengaturan Toko (Admin)":
    st.markdown("## 🔒 **Masuk Panel Pengaturan Toko**")
    
    if not st.session_state["admin_logged_in"]:
        get_pass = st.text_input("Masukkan Kata Sandi Proteksi Admin:", type="password")
        if st.button("Buka Akses Dashboard 🔑"):
            if get_pass == PASSWORD_ADMIN_BENAR:
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("Maaf, kata sandi Anda salah!")
    else:
        st.success("Akses Diterima! Silakan ubah isi toko Anda di bawah ini:")
        if st.button("Keluar Sistem (Log Out) 🚪"):
            st.session_state["admin_logged_in"] = False
            st.rerun()
            
        st.divider()
        st.markdown("### 📋 **Pengaturan Produk & Informasi Toko**")
        
        new_nama = st.text_input("Nama Produk Toko:", value=st.session_state["p_nama"])
        new_harga = st.number_input("Harga Jual (Rp):", value=st.session_state["p_harga"], step=5000)
        new_desc = st.text_area("Deskripsi Utama Produk:", value=st.session_state["p_desc"])
        new_img = st.text_input("Link Foto/Banner URL Gambar:", value=st.session_state["p_img"])
        new_jenis = st.selectbox("Jenis Kategori Produk:", ["Fisik", "Digital"], index=0 if st.session_state["p_jenis"] == "Fisik" else 1)
        
        st.markdown("### 🔗 **Integrasi WhatsApp & Meta Pixel**")
        new_wa = st.text_input("Nomor Admin WA (Gunakan format 62):", value=st.session_state["wa_num"])
        new_pixel = st.text_input("ID Meta Pixel (Facebook Ads Tracking):", value=st.session_state["meta_id"])
        
        if st.button("Simpan Seluruh Konfigurasi Baru 💾"):
            st.session_state["p_nama"] = new_nama
            st.session_state["p_harga"] = new_harga
            st.session_state["p_desc"] = new_desc
            st.session_state["p_img"] = new_img
            st.session_state["p_jenis"] = new_jenis
            st.session_state["wa_num"] = new_wa
            st.session_state["meta_id"] = new_pixel
            st.success("Berhasil! Seluruh isi landing page dan formulir checkout Anda telah diperbarui.")
