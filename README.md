# Simulasi Evakuasi Modular (Pygame + A* Pathfinding + Flood BFS)

Proyek ini adalah simulasi evakuasi pada grid 2D dengan kondisi lingkungan yang berubah secara dinamis akibat banjir. Agen akan mencari rute teraman menuju **goal** menggunakan algoritma **A\*** sambil banjir menyebar menggunakan **BFS flood fill**. Visualisasi berjalan menggunakan **Pygame**.

---

##  Fitur Utama

### Dinamika Banjir (BFS Flood Spread)
- Air menyebar dari sel sumber air menggunakan BFS.
- Setiap sel banjir naik level dari:
  - **Dry** : Putih
  - **Shallow** : Biru muda
  - **Medium** : Biru medium
  - **Deep** (tidak bisa dilewati) : Biru gelap
- Kedalaman air mempengaruhi **cost** dan rute yang diambil agen.

### Algoritma A\* (A Star)
- Digunakan untuk mencari jalur paling aman dan efisien.
- Heuristic menggunakan **Euclidean distance**.
- Mempertimbangkan:
  - **Tembok** : Cell hitam
  - **Level banjir**
  - **Cost cell**
  - **Pergerakan 8 arah** (termasuk diagonal)

### Visualisasi Real-Time (Pygame)
- Grid 2D dinamis
- Agent (start)
- Goal (target evakuasi)
- Air menyebar setiap interval waktu
- Agen bergerak mengikuti jalur A\* terbaru

---

## Kontrol Pengguna

| Input | Fungsi |
|-------|--------|
| **Left Click** | Menentukan posisi Start (Agen) |
| **Right Click** | Menentukan Goal |
| **Ctrl + Click** | Toggle Tembok |
| **Shift + Click** | Toggle Sumber Air |
| **Space** | Start / Pause Simulasi |
| **R** | Reset map |
| **T** | Generate map random |

---

## Struktur Kode

```
├── main.py # Loop utama + UI + interaksi pengguna
├── models.py # Kelas Cell & Environment
├── algorithms.py # BFS Flood + A* Pathfinding
├── config.py # Konfigurasi global (grid, warna, cost, dll)
└── README.md
```


---

## Instalasi

Pastikan Python sudah terinstall.

### 1. Install dependency
```bash
pip install pygame
```
### 2. Jalankan Simulasi
```
python main.py
```

## Dokumentasi

