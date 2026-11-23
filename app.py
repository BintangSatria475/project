from pathlib import Path
import json
import html
import streamlit as st

APP_DIR = Path(__file__).parent
DATA_FILE = APP_DIR / "menus.json"
CSS_FILE = APP_DIR / "style.css"

st.set_page_config(
    page_title="Smart Kantin Planner",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_menus():
    """Load saved menus; create starter data on first run."""
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return [
        {"id": 1, "nama": "Nasi Goreng", "kategori": "Makanan", "harga": 15000, "stok": 20},
        {"id": 2, "nama": "Ayam Geprek", "kategori": "Makanan", "harga": 18000, "stok": 15},
        {"id": 3, "nama": "Es Teh", "kategori": "Minuman", "harga": 5000, "stok": 30},
        {"id": 4, "nama": "Mie Goreng", "kategori": "Makanan", "harga": 12000, "stok": 10},
    ]

def save_menus():
    DATA_FILE.write_text(
        json.dumps(st.session_state.menus, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

if "menus" not in st.session_state:
    st.session_state.menus = load_menus()

if CSS_FILE.exists():
    st.markdown(f"<style>{CSS_FILE.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
else:
    st.warning("File style.css belum ditemukan. Letakkan style.css satu folder dengan app.py.")

def rupiah(value):
    return "Rp " + f"{int(value):,}".replace(",", ".")

def status_stok(stok):
    if stok <= 0:
        return "Habis"
    if stok <= 10:
        return "Stok Rendah"
    return "Tersedia"

# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div class="brand-block">
            <div class="brand-icon">🍽️</div>
            <div><div class="brand-name">Smart Kantin</div>
            <div class="brand-subtitle">PLANNER</div></div>
        </div>
        <div class="side-label">MENU UTAMA</div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigasi",
        ["Dashboard", "Manajemen Menu", "Manajemen Stok", "Rekomendasi"],
        label_visibility="collapsed",
    )
    st.markdown(
        '<div class="sidebar-bottom"><b>SP</b><span>Smart Kantin Planner<br><small>Version 2.0 · Streamlit</small></span></div>',
        unsafe_allow_html=True,
    )

menus = st.session_state.menus
total_menu = len(menus)
total_stok = sum(int(m.get("stok", 0)) for m in menus)
total_makanan = sum(1 for m in menus if m.get("kategori") == "Makanan")
tersedia = [m for m in menus if int(m.get("stok", 0)) > 0]

# Header
st.markdown(
    f"""
    <div class="page-header">
      <div><div class="eyebrow">OVERVIEW</div>
      <h1>{html.escape(page)}</h1>
      <p>Selamat datang kembali! Berikut ringkasan kantin Anda.</p></div>
      <div class="admin-chip"><span class="admin-avatar">A</span><span><b>Admin Kantin</b><small>Administrator</small></span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "Dashboard":
    st.markdown('<div class="section-title"><div><div class="eyebrow">RINGKASAN</div><h2>Ringkasan Kantin</h2></div><span class="live-chip">● Sistem aktif</span></div>', unsafe_allow_html=True)
    cols = st.columns(4)
    stats = [
        ("▣", "Total Menu", total_menu, "Menu terdaftar", "purple"),
        ("🍱", "Total Makanan", total_makanan, "Jenis makanan", "orange"),
        ("▤", "Total Stok", total_stok, "Item dalam stok", "blue"),
        ("✦", "Menu Tersedia", len(tersedia), "Menu dengan stok tersedia", "green"),
    ]
    for col, (icon, label, value, caption, color) in zip(cols, stats):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-top"><span class="metric-icon {color}">{icon}</span><span class="metric-caption">SMART KANTIN</span></div><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-caption">{caption}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="content-panel"><div class="panel-heading"><div><div class="eyebrow">INVENTARIS</div><h2>Ringkasan Menu</h2><p>Daftar menu dan kondisi stok saat ini.</p></div></div></div>', unsafe_allow_html=True)
    if menus:
        rows = []
        for m in menus:
            rows.append({
                "Nama Menu": m["nama"],
                "Kategori": m["kategori"],
                "Harga": rupiah(m["harga"]),
                "Stok": m["stok"],
                "Status": status_stok(m["stok"]),
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada menu. Tambahkan menu melalui halaman Manajemen Menu.")

    st.markdown('<div class="content-panel"><div class="eyebrow">SARAN MENU</div><h2>Menu yang Tersedia</h2><p>Menu berikut masih memiliki stok dan dapat ditawarkan.</p></div>', unsafe_allow_html=True)
    if tersedia:
        rec_cols = st.columns(min(3, len(tersedia)))
        for i, m in enumerate(tersedia[:6]):
            with rec_cols[i % len(rec_cols)]:
                symbol = "🍱" if m["kategori"] == "Makanan" else "🥤"
                st.markdown(
                    f'<div class="recommend-card"><div class="recommend-symbol">{symbol}</div><div><b>{html.escape(m["nama"])}</b><small>{html.escape(m["kategori"])} · Stok {m["stok"]}</small></div><strong>{rupiah(m["harga"])}</strong></div>',
                    unsafe_allow_html=True,
                )
    else:
        st.info("Belum ada menu yang tersedia.")

elif page == "Manajemen Menu":
    st.markdown('<div class="content-panel"><div class="eyebrow">KATALOG</div><h2>Tambah Menu Kantin</h2><p>Masukkan informasi menu baru ke dalam daftar kantin.</p></div>', unsafe_allow_html=True)
    with st.form("add_menu_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            nama = st.text_input("Nama menu", placeholder="Contoh: Nasi Goreng")
            kategori = st.selectbox("Kategori", ["Makanan", "Minuman"])
        with c2:
            harga = st.number_input("Harga (Rp)", min_value=0, step=1000, value=15000)
            stok = st.number_input("Jumlah stok", min_value=0, step=1, value=20)
        submitted = st.form_submit_button("＋ Tambah Menu", use_container_width=True)
        if submitted:
            if not nama.strip():
                st.error("Nama menu wajib diisi.")
            else:
                next_id = max((int(m.get("id", 0)) for m in st.session_state.menus), default=0) + 1
                st.session_state.menus.append({
                    "id": next_id, "nama": nama.strip(), "kategori": kategori,
                    "harga": int(harga), "stok": int(stok)
                })
                save_menus()
                st.success(f"Menu {nama.strip()} berhasil ditambahkan.")
                st.rerun()

    st.markdown('<div class="content-panel"><div class="eyebrow">DAFTAR</div><h2>Menu Terdaftar</h2><p>Hapus menu yang sudah tidak dijual.</p></div>', unsafe_allow_html=True)
    if st.session_state.menus:
        for m in list(st.session_state.menus):
            left, middle, right = st.columns([4, 2, 1])
            with left:
                st.markdown(f"**{m['nama']}**  \n`{m['kategori']}`")
            with middle:
                st.write(f"{rupiah(m['harga'])} · Stok {m['stok']}")
            with right:
                if st.button("Hapus", key=f"delete_{m['id']}"):
                    st.session_state.menus = [x for x in st.session_state.menus if x["id"] != m["id"]]
                    save_menus()
                    st.rerun()
            st.divider()
    else:
        st.info("Belum ada menu.")

elif page == "Manajemen Stok":
    st.markdown('<div class="content-panel"><div class="eyebrow">INVENTARIS</div><h2>Daftar Menu dan Stok</h2><p>Perbarui jumlah stok dan pantau status ketersediaan menu.</p></div>', unsafe_allow_html=True)
    if st.session_state.menus:
        for m in list(st.session_state.menus):
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 2, 2])
                with c1:
                    st.markdown(f"**{m['nama']}**")
                    st.caption(m["kategori"] + " · " + rupiah(m["harga"]))
                with c2:
                    new_stock = st.number_input(
                        "Jumlah stok", min_value=0, step=1, value=int(m["stok"]),
                        key=f"stock_{m['id']}"
                    )
                with c3:
                    st.markdown(f"**{status_stok(int(new_stock))}**")
                    if st.button("Simpan Stok", key=f"save_stock_{m['id']}", use_container_width=True):
                        for item in st.session_state.menus:
                            if item["id"] == m["id"]:
                                item["stok"] = int(new_stock)
                                break
                        save_menus()
                        st.success(f"Stok {m['nama']} diperbarui.")
                        st.rerun()
    else:
        st.info("Belum ada menu untuk dikelola.")

else:
    st.markdown('<div class="content-panel"><div class="eyebrow">SARAN MENU</div><h2>Menu yang Tersedia</h2><p>Menu yang memiliki stok lebih dari nol dapat ditawarkan kepada pelanggan.</p></div>', unsafe_allow_html=True)
    if tersedia:
        for m in tersedia:
            symbol = "🍱" if m["kategori"] == "Makanan" else "🥤"
            c1, c2, c3 = st.columns([1, 4, 2])
            with c1:
                st.markdown(f"<div class='big-emoji'>{symbol}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"**{m['nama']}**")
                st.caption(f"{m['kategori']} · Stok tersedia: {m['stok']}")
            with c3:
                st.markdown(f"**{rupiah(m['harga'])}**")
            st.divider()
    else:
        st.info("Belum ada menu yang tersedia. Tambahkan menu atau perbarui stok terlebih dahulu.")

st.markdown('<div class="footer-note">© 2026 Smart Kantin Planner · Dibuat untuk pengelolaan kantin yang lebih mudah.</div>', unsafe_allow_html=True)
