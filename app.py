import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import hashlib
import urllib.parse
import pandas as pd
import plotly.graph_objects as go
import re

# ==========================================
# 1. STYLE PREMIUM CERAH ALA SCALEV (WHITE LABEL)
# ==========================================
st.set_page_config(page_title="Scalev Pro SaaS Platform", page_icon="⚡", layout="wide")

scalev_premium_style = """
            <style>
            #MainMenu, footer, header, #stDecoration, [data-testid="stHeader"] {
                visibility: hidden !important; height: 0px !important; opacity: 0 !important;
            }
            .stApp { background-color: #FFFFFF; font-family: 'Inter', sans-serif; }
            
            /* Style Card Finansial / Metric Tab */
            .scalev-card {
                background-color: #F8FAFC;
                padding: 22px;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
                text-align: center;
                margin-bottom: 15px;
            }
            .card-title { color: #64748B; font-size: 13px; font-weight: 600; text-transform: uppercase; }
            .card-value { color: #0F172A; font-size: 26px; font-weight: 700; margin-top: 5px; }
            
            /* Tombol Aksi Utama: Indigo Mewah */
            div.stButton > button:first-child {
                background-color: #4F46E5 !important;
                color: white !important;
                border-radius: 10px !important;
                width: 100% !important;
                padding: 12px !important;
                font-weight: bold !important;
                border: none !important;
            }
            </style>
            """
st.markdown(scalev_premium_style, unsafe_allow_html=True)

# ==========================================
# 2. DATABASE SYSTEM ENGINE (SQLITE MULTI-USER)
# ==========================================
DB_FILE = "scalev_pro_database.db"

def init_db():
    """Menginisialisasi seluruh tabel relasional multi-user di server cloud"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY, password TEXT, wa_number TEXT, meta_pixel TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS landing_pages (
                    username TEXT PRIMARY KEY, prod_nama TEXT, prod_harga INTEGER, prod_desc TEXT, prod_img TEXT, html_embed TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, pembeli_nama TEXT, pembeli_email TEXT, status TEXT, tanggal TEXT)""")
    
    # MENDAFTARKAN AKUN SUPER ADMIN OTOMATIS KE DATABASE PUSAT
    super_user = "superadmin"
    super_pass_hash = hashlib.sha256(str.encode("super123")).hexdigest()
    c.execute("SELECT * FROM users WHERE username=?", (super_user,))
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (super_user, super_pass_hash, "6281234567890", "SUPER_PANEL"))
        
    conn.commit()
    conn.close()

init_db()

def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

if "user_aktif" not in st.session_state: st.session_state["user_aktif"] = None
if "is_logged_in" not in st.session_state: st.session_state["is_logged_in"] = False
# ==========================================
# 3. ADVANCED RENDER EMBED ENGINE (PUBLIC ROUTE PAGE CLIENT)
# ==========================================
query_params = st.query_params
if "page" in query_params:
    target_user = query_params["page"]
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT prod_nama, prod_harga, prod_desc, prod_img, html_embed FROM landing_pages WHERE username=?", (target_user,))
    lp_data = c.fetchone()
    c.execute("SELECT wa_number, meta_pixel FROM users WHERE username=?", (target_user,))
    user_data = c.fetchone()
    conn.close()
    
    if lp_data and user_data:
        p_nama, p_harga, p_desc, p_img, h_embed = lp_data
        u_wa, u_pixel = user_data
        
        # Jalankan Meta Pixel Pembeli otomatis jika diisi
        if u_pixel and u_pixel != "Belum Diatur":
            pixel_script = f"""<script>
            !function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e);s.parentNode.insertBefore(t,s)}}(window,document,'script','https://facebook.net');
            fbq('init', '{u_pixel}'); fbq('track', 'PageView');
            </script>"""
            components.html(pixel_script, height=0)
            
        st.image(p_img, use_container_width=True)
        st.title(p_nama)
        st.subheader(f"Rp {p_harga:,.0f}")
        st.write(p_desc)
        
        # SISTEM ENGINGE RENDER EMBED HTML / IFRAME VIDEO & MAPS
        if h_embed and h_embed.strip() != "":
            st.markdown("---")
            calculated_height = 450
            if "height=" in h_embed:
                match = re.search(r'height=["\'](\d+)(px)?["\']', h_embed)
                if match: calculated_height = int(match.group(1))
            components.html(h_embed, height=calculated_height, scrolling=True)
            
        st.markdown("---")
        st.markdown("### 📝 Halaman Formulir Pembelian Instan")
        c_nama = st.text_input("Nama Lengkap Pembeli:")
        c_email = st.text_input("Alamat Email:")
        
        if st.button("Selesaikan Pesanan & Kirim ke WhatsApp Admin 💬", type="primary"):
            if c_nama and c_email:
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("INSERT INTO orders (username, pembeli_nama, pembeli_email, status, tanggal) VALUES (?, ?, ?, 'Pending', date('now'))", (target_user, c_nama, c_email))
                conn.commit()
                conn.close()
                
                pesan_wa = f"Halo Kak, saya order:\n📦 {p_nama}\n💰 Total: Rp {p_harga:,}\n\n👤 Nama: {c_nama}\n📧 Email: {c_email}"
                link_wa = f"https://wa.me{u_wa}?text={urllib.parse.quote(pesan_wa)}"
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{link_wa}\'" />', unsafe_allow_html=True)
            else:
                st.error("Mohon lengkapi Nama dan Email Anda untuk memesan.")
        st.stop()

# ==========================================
# 4. PORTAL AUTENTIKASI MULTI-USER SAAS
# ==========================================
if not st.session_state["is_logged_in"]:
    st.title("⚡ Scalev Pro SaaS Builder Platform")
    st.caption("Buat akun mandiri, buat landing page kustom, dan lacak data penjualan dengan grafik profesional.")
    
    tab_masuk, tab_daftar = st.tabs(["🔒 Masuk Dashboard Akun", "📝 Registrasi Anggota Baru"])
    
    with tab_daftar:
        reg_user = st.text_input("Buat Username Baru:", key="reg_u")
        reg_pass = st.text_input("Buat Kata Sandi Akun:", type="password", key="reg_p")
        reg_wa = st.text_input("Masukkan Nomor WhatsApp (Format: 628xxx):", key="reg_w")
        
        if st.button("Daftarkan Akun Toko Saya 🚀", key="btn_reg_act"):
            if reg_user and reg_pass and reg_wa:
                try:
                    conn = sqlite3.connect(DB_FILE)
                    c = conn.cursor()
                    c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (reg_user, make_hash(reg_pass), reg_wa, "Belum Diatur"))
                    c.execute("INSERT INTO landing_pages VALUES (?, ?, ?, ?, ?, ?)", 
                              (reg_user, "Nama Produk Anda di Sini", 0, "Silakan tulis copywriting deskripsi penawaran produk Anda di sini.", "https://unsplash.com", ""))
                    conn.commit()
                    conn.close()
                    st.success("🎉 Registrasi sukses! Silakan beralih ke tab 'Masuk Dashboard Akun'.")
                except sqlite3.IntegrityError:
                    st.error("Gagal! Username telah digunakan oleh member lain. Gunakan nama lain.")
            else:
                st.warning("Semua kolom registrasi wajib diisi!")

    with tab_masuk:
        login_user = st.text_input("Username Anda:", key="log_u")
        login_pass = st.text_input("Kata Sandi Akun:", type="password", key="log_p")
        
        if st.button("Masuk Ke Kendali Dashboard 🔑", key="btn_login_act"):
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (login_user, make_hash(login_pass)))
            user_valid = c.fetchone()
            conn.close()
            
            if user_valid:
                st.session_state["user_aktif"] = login_user
                st.session_state["is_logged_in"] = True
                st.success("Berhasil masuk sistem!")
                st.rerun()
            else:
                st.error("Akses ditolak! Username atau kata sandi salah.")
else:
    # ==========================================
    # 5. HALAMAN UTAMA KENDALI YANG SUDAH LOGIN
    # ==========================================
    USER_NOW = st.session_state["user_aktif"]
    
    st.sidebar.title(f"👤 Akun: {USER_NOW}")
    if st.sidebar.button("Keluar Aplikasi (Log Out) 🚪", key="btn_logout"):
        st.session_state["is_logged_in"] = False
        st.session_state["user_aktif"] = None
        st.rerun()
        
    # LOGIKA PEMBAGIAN MENU ANTARA SUPERADMIN VS MEMBER BIASA
    if USER_NOW == "superadmin":
        menu_saas = st.sidebar.radio("Navigasi Super Admin:", ["👑 Kontrol Pusat Member & Transaksi"])
    else:
        menu_saas = st.sidebar.radio("Navigasi Fitur:", ["📈 Analitik & Ringkasan Data", "📝 Pembuat Canvas Landing Page", "⚙️ Integrasi Kontak & Iklan"])
        
    # --- PROSES RENDER TAMPILAN PUSAT KONTROL SUPER ADMIN ---
    if USER_NOW == "superadmin" and menu_saas == "👑 Kontrol Pusat Member & Transaksi":
        st.title("👑 Dashboard Pusat Kontrol Super Admin")
        st.caption("Pantau seluruh performa aktivitas pendaftaran member dan database transaksi global.")
        st.divider()
        
        conn = sqlite3.connect(DB_FILE)
        df_semua_member = pd.read_sql_query("SELECT username, wa_number FROM users WHERE username != 'superadmin'", conn)
        df_semua_order = pd.read_sql_query("SELECT * FROM orders", conn)
        conn.close()
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f'<div class="scalev-card"><div class="card-title">Total Seluruh Anggota Member</div><div class="card-value">{len(df_semua_member)}</div></div>', unsafe_allow_html=True)
        with col_s2:
            st.markdown(f'<div class="scalev-card"><div class="card-title">Total Seluruh Transaksi Global</div><div class="card-value">{len(df_semua_order)}</div></div>', unsafe_allow_html=True)
            
        st.subheader("📋 Daftar Seluruh Anggota Member Aktif")
        st.dataframe(df_semua_member, use_container_width=True)
        st.subheader("📋 Log Semua Transaksi Masuk Secara Global")
        st.dataframe(df_semua_order, use_container_width=True)

    # --- PROSES RENDER TAMPILAN DASHBOARD PENGGUNA MEMBER BIASA ---
    elif menu_saas == "📈 Analitik & Ringkasan Data":
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT prod_harga FROM landing_pages WHERE username=?", (USER_NOW,))
        lp_harga = c.fetchone()[0]
        df_orders = pd.read_sql_query("SELECT * FROM orders WHERE username='" + USER_NOW + "'", conn)
        conn.close()
        
        st.markdown("#### 📊 Dashboard Performa Bisnis Anda")
        total_order = len(df_orders)
        omzet_simulasi = total_order * lp_harga
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1: st.markdown(f'<div class="scalev-card"><div class="card-title">Total Orders Masuk</div><div class="card-value">{total_order}</div></div>', unsafe_allow_html=True)
        with col_m2: st.markdown(f'<div class="scalev-card"><div class="card-title">Pesanan Berhasil</div><div class="card-value">{total_order}</div></div>', unsafe_allow_html=True)
        with col_m3: st.markdown(f'<div class="scalev-card"><div class="card-title">Estimasi Omzet Penjualan</div><div class="card-value">Rp {omzet_simulasi:,}</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>#### 📉 Grafik Pertumbuhan Omzet Harian", unsafe_allow_html=True)
        if not df_orders.empty:
            df_grouped = df_orders.groupby("tanggal").count().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_grouped["tanggal"], y=df_grouped["id"] * lp_harga, mode='lines+markers', name='Omzet', line=dict(color='#4F46E5', width=3)))
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', margin=dict(l=10, r=10, t=10, b=10), height=230)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada transaksi harian masuk. Grafik iklan akan otomatis bergerak setelah ada pembelian.")

    elif menu_saas == "📝 Pembuat Canvas Landing Page":
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT prod_nama, prod_harga, prod_desc, prod_img, html_embed FROM landing_pages WHERE username=?", (USER_NOW,))
        lp_nama, lp_harga, lp_desc, lp_img, lp_embed = c.fetchone()
        conn.close()
        
        st.markdown("#### 📝 Modifikasi Konten Penawaran & HTML Embed")
        tautan_promosi = f"https://streamlit.app{USER_NOW}"
        st.success(f"🔗 **Link Iklan Landing Page Publik Anda:** {tautan_promosi}")
        
        new_nama = st.text_input("Nama Produk Jualan Anda:", value=lp_nama)
        new_harga = st.number_input("Harga Jual (Rupiah):", value=int(lp_harga), step=5000)
        new_desc = st.text_area("Tulis Teks Deskripsi/Copywriting Iklan:", value=lp_desc)
        new_img = st.text_input("Tautan URL Foto Utama Gambar Produk:", value=lp_img)
        new_embed = st.text_area("Masukkan Kode Embed HTML / Javascript Kustom:", value=lp_embed)
        
        if st.button("Publikasikan Seluruh Perubahan Landing Page 🚀", type="primary", key="btn_save_lp"):
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("UPDATE landing_pages SET prod_nama=?, prod_harga=?, prod_desc=?, prod_img=?, html_embed=? WHERE username=?", 
                      (new_nama, new_harga, new_desc, new_img, new_embed, USER_NOW))
            conn.commit()
            conn.close()
            st.success("🎉 Sukses! Perubahan landing page Anda telah diperbarui secara instan.")

    elif menu_saas == "⚙️ Integrasi Kontak & Iklan":
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT wa_number, meta_pixel FROM users WHERE username=?", (USER_NOW,))
        u_wa, u_pixel = c.fetchone()
        conn.close()
        
        st.markdown("#### 🔗 Pengaturan Kontak Bisnis & Pelacakan Piksel Iklan")
        new_wa = st.text_input("Nomor WhatsApp Tujuan Pembayaran (Format 62):", value=u_wa)
        new_pixel = st.text_input("Nomor ID Meta Pixel Aktif (Facebook Ads):", value=u_pixel)
        
        if st.button("Kunci Pengaturan Kontak & Iklan Saya 💾", type="primary", key="btn_save_ads"):
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("UPDATE users SET wa_number=?, meta_pixel=? WHERE username=?", (new_wa, new_pixel, USER_NOW))
            conn.commit()
            conn.close()
            st.success("🎉 Selamat! Konfigurasi kontak WhatsApp dan Facebook Ads berhasil diperbarui.")
