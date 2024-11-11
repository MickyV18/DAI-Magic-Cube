# Magic Cube dengan Local Search

## Deskripsi Singkat

Program ini merupakan implementasi algoritma local search untuk mencari solusi Magic Cube berukuran 5x5x5. magic cube adalah kubus yang tersusun dari angka 1 hingga n³ (tanpa pengulangan) dengan properti bahwa jumlah angka-angka pada setiap baris, kolom, tiang, diagonal ruang, dan diagonal pada potongan bidang sama dengan magic number. Magic number dihitung dengan rumus:

```
M = (n × (n³ + 1)) / 2
```

Program mengimplementasikan beberapa algoritma local search:

- Steepest Ascent Hill-climbing
- Hill-climbing with Sideways Move
- Random Restart Hill-climbing
- Stochastic Hill-climbing
- Simulated Annealing
- Genetic Algorithm

## Cara Setup dan Menjalankan Program

### Prasyarat

- Python 3.x
- pip (Python package manager)

### Instalasi Dependencies

1. Clone repository ini

```bash
git clone [URL repository]
cd [nama-folder]
```

2. Install package yang dibutuhkan

```bash
pip install dash plotly numpy random time
```

### Menjalankan Program

1. Jalankan file Python utama

```bash
python Final.py
```

2. Buka browser dan akses

```
http://localhost:8050
```

3. Gunakan antarmuka web untuk:

- Memilih algoritma local search yang ingin digunakan
- Melihat visualisasi kubus sebelum dan sesudah optimasi
- Mengamati progress iterasi melalui grafik
- Melihat statistik performa seperti objective function, jumlah elemen yang mencapai magic number, dan durasi eksekusi

## Pembagian Tugas

| Nama                      | NIM      | Tugas                                                                                                                                                    |
| ------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Arvyno Pranata Limahardja | 18222007 | 1. Optimasi algoritma semua varian algoritma Hill-climbing dan Simulated Annealing<br>2. Optimasi Objective Function<br>3. Pengerjaan Laporan            |
| Bastian Natanael Sibarani | 18222053 | 1. Optimasi algoritma Genetic Algorithm<br>2. Membantu optimasi algoritma Simulated Annealing<br>3. Optimasi Objective Function<br>4. Pengerjaan Laporan |
| Naomi Pricilla Agustine   | 18222065 | 1. Desain Website<br>2. Pengerjaan Laporan                                                                                                               |
| Micky Valentino           | 18222093 | 1. Pengerjaan Website<br>2. Debugging Random Restart Hill Climbing                                                                                       |
