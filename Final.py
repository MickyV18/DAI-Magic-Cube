import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import random
import time

def inisialisasi_kubus(n):
    angka = random.sample(range(1, n**3 + 1), n**3)
    return np.array(angka).reshape((n, n, n))


# Function to calculate magic number
def hitung_magic_number(n):
    return (n * (n**3 + 1)) // 2

# Define the cek_spesifikasi function
def cek_spesifikasi(n, kubus):
    magic_number = hitung_magic_number(n)
    jumlah_skor = 0
    total_selisih = 0
    jumlah_315 = 0
    frekuensi_pemeriksaan = 0

    # Row calculation
    for i in range(n):
        for j in range(n):
            jumlah_baris = sum(kubus[i][j][k] for k in range(n))
            if jumlah_baris == magic_number:
                jumlah_skor += 1
                jumlah_315 += 1
            total_selisih += abs(jumlah_baris - magic_number)
            frekuensi_pemeriksaan += 1

    # Column calculation
    for i in range(n):
        for k in range(n):
            jumlah_kolom = sum(kubus[i][j][k] for j in range(n))
            if jumlah_kolom == magic_number:
                jumlah_skor += 1
                jumlah_315 += 1
            total_selisih += abs(jumlah_kolom - magic_number)
            frekuensi_pemeriksaan += 1

    # Tiang calculation
    for j in range(n):
        for k in range(n):
            jumlah_tiang = sum(kubus[i][j][k] for i in range(n))
            if jumlah_tiang == magic_number:
                jumlah_skor += 1
                jumlah_315 += 1
            total_selisih += abs(jumlah_tiang - magic_number)
            frekuensi_pemeriksaan += 1

    primary_score = (jumlah_skor / frekuensi_pemeriksaan) * 70
    avg_selisih = total_selisih / frekuensi_pemeriksaan
    max_possible_selisih = magic_number - 15
    proximity_ratio = 1 - (avg_selisih / max_possible_selisih)
    secondary_score = proximity_ratio * 30
    persentase_sukses = primary_score + secondary_score

    return round(persentase_sukses, 3), jumlah_315

# Helper functions
def swap_angka(n, kubus):
    flat_indices = np.random.choice(n**3, 2, replace=False)
    pos1 = np.unravel_index(flat_indices[0], (n, n, n))
    pos2 = np.unravel_index(flat_indices[1], (n, n, n))
    kubus[pos1], kubus[pos2] = kubus[pos2], kubus[pos1]
    return kubus

def generate_best_neighbors(n, kubus):
    # Menginisialisasi kubus terbaik dengan kubus yang menjadi input fungsi
    kubus_terbaik = np.copy(kubus)
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)

    # Memeriksa semua kemungkinan neighbor
    for i in range (n**3):
      for j in range (i + 1, n**3):
        # Menginisialisasi neighbor dari kubus yang menjadi input fungsi dengan melakukan penukaran indeks i dan j
        kubus_baru = np.copy(kubus)
        posisi1 = np.unravel_index(i, (n, n, n))
        posisi2 = np.unravel_index(j, (n, n, n))
        kubus_baru[posisi1], kubus_baru[posisi2] = kubus_baru[posisi2], kubus_baru[posisi1]

        # Menghitung skor kubus neighbor
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)

        # Jika skor baru lebih baik, update kubus terbaik
        if skor_kubus_baru > skor_kubus_terbaik:
          kubus_terbaik = np.copy(kubus_baru)
          skor_kubus_terbaik = skor_kubus_baru
          jumlah_315_terbaik = jumlah_315_baru

    return kubus_terbaik

def generate_best_neighbors_sideways(n, kubus):
    # Menginisialisasi kubus terbaik dengan kubus yang menjadi input fungsi
    kubus_terbaik = np.copy(kubus)
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)
    improvisasi_skor = False

    # Memeriksa semua kemungkinan neighbor
    for i in range (n**3):
      for j in range (i + 1, n**3):
        # Menginisialisasi neighbor dari kubus yang menjadi input fungsi dengan melakukan penukaran indeks i dan j
        kubus_baru = np.copy(kubus)
        posisi1 = np.unravel_index(i, (n, n, n))
        posisi2 = np.unravel_index(j, (n, n, n))
        kubus_baru[posisi1], kubus_baru[posisi2] = kubus_baru[posisi2], kubus_baru[posisi1]

        # Menghitung skor kubus neighbor
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)

        # Update jika menemukan skor yang lebih baik atau setidaknya skor sama tetapi jumlah magic number lebih banyak (dengan catatan, improvisasi_skor bernilai False)
        if skor_kubus_baru > skor_kubus_terbaik:
            kubus_terbaik = np.copy(kubus_baru)
            skor_kubus_terbaik = skor_kubus_baru
            jumlah_315_terbaik = jumlah_315_baru
            improvisasi_skor = True
        elif (skor_kubus_baru == skor_kubus_terbaik) and (jumlah_315_baru > jumlah_315_terbaik):
            kubus_terbaik = np.copy(kubus_baru)
            jumlah_315_terbaik = jumlah_315_baru

    return kubus_terbaik, improvisasi_skor

def sideways_move_hill_climbing(n, kubus, maks_iterasi_stagnan):
    # Memulai perhitungan waktu
    start_time = time.perf_counter()

    # Menginisialisasi array history untuk menyimpan informasi
    hist_iterasi_perbaikan = []
    hist_skor_kubus = []
    hist_jumlah_315 = []

    # Menginisialisasi array history untuk menyimpan informasi
    histori = {
        'skor_kubus_terbaik': None,
        'jumlah_315_terbaik': None,
        'kubus_terbaik': kubus,
        'iterasi': None,
        'iterasi_stagnan': None,
        'skor_kubus': [],
        'jumlah_315': [],
        'elapsed_time': None
    }

    # Menginisialisasi kubus_terbaik dengan kubus yang menjadi input fungsi
    kubus_terbaik = np.copy(kubus)

    # Menginisialisasi skor_kubus_terbaik dengan skor kubus yang menjadi input fungsi
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)

    # Menghitung jumlah iterasi
    iterasi = 0
    iterasi_stagnan = 0 # Mengamati iterasi yang menghasilkan kubus_baru dengan skor sama yang sama besar dengan kubus_terbaik

    # Melakukan iterasi sampai tidak ada perbaikan skor
    while (True):
        print("iterasi:", iterasi)
        # Memilih neighbor terbaik dari setiap kemungkinan neighbor dari current state kubus_terbaik
        kubus_baru, improvisasi_skor = generate_best_neighbors_sideways(n, kubus_terbaik)

        # Menghitung skor kubus baru
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)
        iterasi += 1

        # Menyimpan informasi kubus baru
        histori['skor_kubus'].append(skor_kubus_baru)
        histori['jumlah_315'].append(jumlah_315_baru)

        # Jika terdapat perbaikan
        if improvisasi_skor:
            # Menyimpan informasi kubus_terbaik
              kubus_terbaik = np.copy(kubus_baru)
              skor_kubus_terbaik = skor_kubus_baru
              jumlah_315_terbaik = jumlah_315_baru

              # Reset nilai iterasi_stagnan
              iterasi_stagnan = 0

              # Jika sudah mencapai skor sempurna (100%), hentikan iterasi
              if skor_kubus_terbaik == 100:
                  break

        # Jika tidak ada perbaikan tapi skor sama
        elif skor_kubus_baru == skor_kubus_terbaik:
            # Melakukan iterasi terhadap nilai iterasi_stagnan
            iterasi_stagnan += 1

            # Jika sudah mencapai iterasi_hasil_sama sebanyak maks_iterasi_hasil_sama, hentikan iterasi
            if iterasi_stagnan >= maks_iterasi_stagnan:
                break

        else: # Jika tidak ada perbaikan tapi skor lebih buruk, hentikan iterasi
            break

    # Update array histori
    histori['skor_kubus_terbaik'] = skor_kubus_terbaik
    histori['jumlah_315_terbaik'] = jumlah_315_terbaik
    histori['kubus_terbaik'] = kubus_terbaik
    histori['iterasi'] = iterasi
    histori['iterasi_stagnan'] = iterasi_stagnan

    # Menghitung hasil timing
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    histori['elapsed_time'] = round(elapsed_time, 3)

    return histori

def simulated_annealing(n, maks_iterasi, threshold_akurasi, temperatur_awal, minimum_temperatur, laju_penurunan, kubus):
    # Memulai perhitungan waktu
    start_time = time.perf_counter()

    # Menginisialisasi array history untuk menyimpan informasi
    histori = {
        'skor_kubus_terbaik': None,
        'jumlah_315_terbaik': None,
        'kubus_terbaik': kubus,
        'iterasi': None,
        'iterasi_local_optima': 0,
        'skor_kubus': [],
        'jumlah_315': [],
        'probabilitas': [],
        'temperatur': [],
        'elapsed_time': None
    }

    # Menginisialisasi kubus terbaik dan kubus sekarang dengan kubus yang menjadi input fungsi
    kubus_terbaik = np.copy(kubus)
    kubus_sekarang = np.copy(kubus)

    # Menginisialisasi skor awal
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)
    skor_sekarang = skor_kubus_terbaik
    jumlah_315_sekarang = jumlah_315_terbaik

    # Menginisialisasi parameter temperatur dan iterasi
    temperatur = temperatur_awal
    iterasi = 0
    rejected_streak = 0

    while (iterasi < maks_iterasi) and (temperatur > minimum_temperatur):
        # Membuat kubus_temp yang dihasilkan dengan fungsi swap_angka terhadap kubus_sekarang
        kubus_temp = swap_angka(n, np.copy(kubus_sekarang))
        skor_kubus_temp, jumlah_315_temp = cek_spesifikasi(n, kubus_temp)
        iterasi += 1

        # Menghitung perbedaan skor dan probabilitas penerimaan
        skor_delta = skor_kubus_temp - skor_sekarang
        if skor_delta > 0:
            probabilitas = 1.0
        else:
            # Menghitung probabilitas penerimaan solusi yang lebih buruk
            probabilitas = np.exp(skor_delta / temperatur)

        # Menyimpan informasi untuk history
        histori['skor_kubus'].append(skor_sekarang)
        histori['jumlah_315'].append(jumlah_315_sekarang)
        histori['probabilitas'].append(probabilitas)
        histori['temperatur'].append(temperatur)

        # Menentukan apakah menerima solusi baru
        if random.random() < probabilitas:
            # Menerima solusi baru
            kubus_sekarang = np.copy(kubus_temp)
            skor_sekarang = skor_kubus_temp
            jumlah_315_sekarang = jumlah_315_temp
            rejected_streak = 0

            # Update solusi terbaik jika ditemukan yang lebih baik
            if skor_sekarang > skor_kubus_terbaik:
                kubus_terbaik = np.copy(kubus_sekarang)
                skor_kubus_terbaik = skor_sekarang
                jumlah_315_terbaik = jumlah_315_sekarang

                # Berhenti jika sudah mencapai threshold akurasi
                if skor_kubus_terbaik >= threshold_akurasi:
                    break
        else:
            # Solusi ditolak, tambah penghitung penolakan berturut-turut
            rejected_streak += 1

        # Memeriksa apakah terjebak di local optima
        if rejected_streak >= 10:  # Threshold untuk mendeteksi local optima
            histori['iterasi_local_optima'] += 1
            rejected_streak = 0
            # Menaikkan temperatur sementara untuk keluar dari local optima
            temperatur = min(temperatur_awal, temperatur * 2)
        else:
            # Menurunkan temperatur sesuai jadwal pendinginan
            if temperatur > minimum_temperatur:
                temperatur = max(minimum_temperatur, temperatur * laju_penurunan)

    # Update array histori dengan hasil akhir
    histori['skor_kubus_terbaik'] = skor_kubus_terbaik
    histori['jumlah_315_terbaik'] = jumlah_315_terbaik
    histori['kubus_terbaik'] = kubus_terbaik
    histori['iterasi'] = iterasi

    # Menghitung waktu eksekusi
    end_time = time.perf_counter()
    histori['elapsed_time'] = round(end_time - start_time, 3)

    return histori



def stochastic_hill_climbing(n, maks_iterasi, threshold_akurasi, kubus):
    # Memulai perhitungan waktu
    start_time = time.perf_counter()

    # Menginisialisasi array history untuk menyimpan informasi
    histori = {
        'skor_kubus_terbaik': None,
        'jumlah_315_terbaik': None,
        'kubus_terbaik': kubus,
        'iterasi': None,
        'skor_kubus': [],
        'jumlah_315': [],
        'elapsed_time': None
    }

    # Menginisialisasi kubus_terbaik dengan kubus yang menjadi input fungsi
    kubus_terbaik = kubus

    # Menginisialisasi skor_kubus_terbaik dengan skor kubus yang menjadi input fungsi
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)

    # Menginisialisasi jumlah iterasi dengan nilai 0
    iterasi = 0

    while (iterasi < maks_iterasi):
        # Membuat konfigurasi kubus baru dengan menukar angka secara acak
        kubus_baru = swap_angka(n, np.copy(kubus_terbaik))
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)
        iterasi += 1

        # Menyimpan informasi kubus baru
        histori['skor_kubus'].append(skor_kubus_baru)
        histori['jumlah_315'].append(jumlah_315_baru)

        # Jika skor baru lebih baik atau sama dengan, update kubus terbaik
        if skor_kubus_baru > skor_kubus_terbaik:
            skor_kubus_terbaik = skor_kubus_baru
            jumlah_315_terbaik = jumlah_315_baru
            kubus_terbaik = np.copy(kubus_baru)

            # Jika skor sudah mencapai atau melebihi threshold, hentikan iterasi
            if (skor_kubus_terbaik >= threshold_akurasi):
                break

    # Update array histori
    histori['skor_kubus_terbaik'] = skor_kubus_terbaik
    histori['jumlah_315_terbaik'] = jumlah_315_terbaik
    histori['kubus_terbaik'] = kubus_terbaik
    histori['iterasi'] = iterasi

    # Menghitung hasil timing
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    histori['elapsed_time'] = round(elapsed_time, 3)

    return histori

def generate_best_neighbors_steepest(n, kubus):
    # Menginisialisasi kubus terbaik dengan kubus yang menjadi input fungsi
    kubus_terbaik = np.copy(kubus)
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)
    improvisasi_skor = False

    # Memeriksa semua kemungkinan neighbor
    for i in range (n**3):
      for j in range (i + 1, n**3):
        # Menginisialisasi neighbor dari kubus yang menjadi input fungsi dengan melakukan penukaran indeks i dan j
        kubus_baru = np.copy(kubus)
        posisi1 = np.unravel_index(i, (n, n, n))
        posisi2 = np.unravel_index(j, (n, n, n))
        kubus_baru[posisi1], kubus_baru[posisi2] = kubus_baru[posisi2], kubus_baru[posisi1]

        # Menghitung skor kubus neighbor
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)

        # Jika skor baru lebih baik, update kubus terbaik
        if skor_kubus_baru > skor_kubus_terbaik:
          kubus_terbaik = np.copy(kubus_baru)
          skor_kubus_terbaik = skor_kubus_baru
          jumlah_315_terbaik = jumlah_315_baru
          improvisasi_skor = True

    return kubus_terbaik, improvisasi_skor

def steepest_ascent_hill_climbing(n, kubus):
    # Memulai perhitungan waktu
    start_time = time.perf_counter()

    # Menginisialisasi array history untuk menyimpan informasi
    histori = {
        'skor_kubus_terbaik': None,
        'jumlah_315_terbaik': None,
        'kubus_terbaik': kubus,
        'iterasi': None,
        'skor_kubus': [],
        'jumlah_315': [],
        'elapsed_time': None
    }

    # Menginisialisasi kubus_terbaik dengan kubus yang menjadi input fungsi
    kubus_terbaik = np.copy(kubus)

    # Menginisialisasi skor_kubus_terbaik dengan skor kubus yang menjadi input fungsi
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)

    # Menghitung jumlah iterasi
    iterasi = 0

    # Melakukan iterasi sampai tidak ada perbaikan skor
    while (True):
        print("Iterasi:", iterasi)
        # Memilih neighbor terbaik dari setiap kemungkinan neighbor dari current state kubus_terbaik
        kubus_baru, improvisasi_skor = generate_best_neighbors_steepest(n, kubus_terbaik)

        # Menghitung skor kubus baru
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)
        iterasi += 1

        # Menyimpan informasi kubus baru
        histori['skor_kubus'].append(skor_kubus_baru)
        histori['jumlah_315'].append(jumlah_315_baru)

        if not improvisasi_skor:
            break

        kubus_terbaik = np.copy(kubus_baru)
        skor_kubus_terbaik = skor_kubus_baru
        jumlah_315_terbaik = jumlah_315_baru

        # Jika sudah mencapai skor sempurna (100%), hentikan iterasi
        if skor_kubus_terbaik == 100:
            break

    # Update array histori
    histori['skor_kubus_terbaik'] = skor_kubus_terbaik
    histori['jumlah_315_terbaik'] = jumlah_315_terbaik
    histori['kubus_terbaik'] = kubus_terbaik
    histori['iterasi'] = iterasi

    # Menghitung hasil timing
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    histori['elapsed_time'] = round(elapsed_time, 3)

    return histori

def random_restart_hill_climbing(n, maks_restart, threshold_akurasi, kubus):
    # Memulai perhitungan waktu
    start_time = time.perf_counter()

    # Menginisialisasi array history untuk menyimpan informasi
    histori = {
        'skor_kubus_terbaik': None,
        'jumlah_315_terbaik': None,
        'kubus_terbaik': kubus,
        'restart': None,
        'iterasi': [],
        'skor_kubus': [],
        'jumlah_315': [],
        'elapsed_time': None
    }

    # Menginisialisasi kubus_terbaik dengan kubus yang menjadi input fungsi
    kubus_terbaik = np.copy(kubus)

    # Menginisialisasi skor_kubus_terbaik dengan skor kubus yang menjadi input fungsi
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)

    # Menghitung jumlah iterasi
    restart = 0

    while (restart < maks_restart):
        # Membuat konfigurasi kubus baru secara acak untuk restart
        kubus_random = inisialisasi_kubus(n)

        # Melakukan hill climbing dari konfigurasi acak ini sampai mencapai local optimum
        histori_kubus_climbing = steepest_ascent_hill_climbing(n, kubus_random)
        restart += 1
        iterasi = histori_kubus_climbing['iterasi']
        skor_kubus_climbing = histori_kubus_climbing['skor_kubus_terbaik']
        jumlah_315_climbing = histori_kubus_climbing['jumlah_315_terbaik']
        kubus_climbing = histori_kubus_climbing['kubus_terbaik']

        # Menyimpan informasi kubus baru
        histori['iterasi'].append(iterasi)
        histori['skor_kubus'].append(skor_kubus_climbing)
        histori['jumlah_315'].append(jumlah_315_climbing)

        # Jika skor baru lebih baik, update kubus terbaik
        if (skor_kubus_climbing > skor_kubus_terbaik):
            kubus_terbaik = np.copy(kubus_climbing)
            skor_kubus_terbaik = skor_kubus_climbing
            jumlah_315_terbaik = jumlah_315_climbing

            # Jika skor sudah mencapai atau melebihi threshold, hentikan iterasi
            if (skor_kubus_terbaik >= threshold_akurasi):
                break

    # Update array histori
    histori['skor_kubus_terbaik'] = skor_kubus_terbaik
    histori['jumlah_315_terbaik'] = jumlah_315_terbaik
    histori['kubus_terbaik'] = kubus_terbaik
    histori['restart'] = restart

    # Menghitung hasil timing
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    histori['elapsed_time'] = round(elapsed_time, 3)

    return histori

def create_scatter_data(cube_size, numbers):
    # Create 3D scatter data
    normalized_values = (numbers.flatten() - numbers.min()) / (numbers.max() - numbers.min())
    colors = ["rgb(0, {}, {})".format(int(216 * val), int(230 * val)) for val in normalized_values]
    
    cube_data = go.Scatter3d(
        x=np.repeat(np.arange(cube_size), cube_size * cube_size),
        y=np.tile(np.repeat(np.arange(cube_size), cube_size), cube_size),
        z=np.tile(np.arange(cube_size), cube_size * cube_size),
        mode='markers+text',
        text=numbers.flatten(),
        textposition="top center",
        marker=dict(size=5, color=colors),
    )
    
    axis_lines = [
        go.Scatter3d(
            x=[0, cube_size-1], y=[0, 0], z=[0, 0],
            mode='lines',
            line=dict(color='red', width=4),
            name='X Axis'
        ),
        go.Scatter3d(
            x=[0, 0], y=[0, cube_size-1], z=[0, 0],
            mode='lines',
            line=dict(color='green', width=4),
            name='Y Axis'
        ),
        go.Scatter3d(
            x=[0, 0], y=[0, 0], z=[0, cube_size-1],
            mode='lines',
            line=dict(color='blue', width=4),
            name='Z Axis'
        )
    ]
    
    # Create layout for 3D scatter plot
    layout = go.Layout(
        scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis'
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )

    # Return a complete figure
    return go.Figure(data=[cube_data] + axis_lines, layout=layout)


# Function to initialize a new 5x5x5 cube of numbers
cube_size = 5

numbers = inisialisasi_kubus(cube_size)

# Calculate initial success percentage and element count
initial_persentase_sukses, initial_jumlah_315 = cek_spesifikasi(cube_size, numbers)


scatter_data = create_scatter_data(cube_size, numbers)
layout = go.Layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)
fig = go.Figure(data=scatter_data, layout=layout)

# Add this line at the beginning of your app definition to suppress callback exceptions if needed
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Initialize different configurations for each "Before" cube
numberss = [inisialisasi_kubus(cube_size) for _ in range(3)]

app.layout = html.Div([
    html.H1("Diagonal Magic Cube", style={'textAlign': 'center', 'backgroundColor': '#587ca4', 'color': 'white', 'padding': '10px'}),

    html.Div([
        html.Button('Steepest Hill Climbing', id='button-best', n_clicks=0, disabled=False, style={'padding': '10px', 'margin': '5px', 'font-size': '16px'}),
        html.Button('Sideways Move Hill Climbing', id='button-sideways', n_clicks=0, disabled=False, style={'padding': '10px', 'margin': '5px', 'font-size': '16px'}),
        html.Button('Random Restart Hill Climbing', id='button-random-restart', n_clicks=0, disabled=False, style={'padding': '10px', 'margin': '5px', 'font-size': '16px'}),
        html.Button('Stochastic Hill Climbing', id='button-stochastic', n_clicks=0, disabled=False, style={'padding': '10px', 'margin': '5px', 'font-size': '16px'}),
        html.Button('Simulated Annealing', id='button-simulated', n_clicks=0, disabled=False, style={'padding': '10px', 'margin': '5px', 'font-size': '16px'}),
        html.Button('Reset', id='button-reset', n_clicks=0, disabled=False, style={'padding': '10px', 'margin': '5px', 'font-size': '16px', 'backgroundColor': '#e57373', 'color': 'white'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'padding': '10px'}),

    # Cube visualizations
    html.Div([
        html.Div([
            html.H3("Before", style={'textAlign': 'center'}),
            dcc.Graph(id='initial-cube-graph', figure=create_scatter_data(cube_size, numbers)),
            html.Div(
                f'Objective Function: {cek_spesifikasi(cube_size, numbers)[0]}% | Initial Jumlah Elemen 315: {cek_spesifikasi(cube_size, numbers)[1]}', 
                style={'textAlign': 'center', 'marginTop': '10px', 'backgroundColor': '#587ca4', 'color': 'white', 'padding': '10px', 'borderRadius': '5px'}
            )
        ], style={'flex': '1', 'padding': '10px', 'border': '2px solid #587ca4', 'borderRadius': '8px', 'margin': '10px'}),

        html.Div([
            html.H3("After", style={'textAlign': 'center'}),
            dcc.Graph(id='optimized-cube-graph', figure=create_scatter_data(cube_size, numbers)),
            html.Div(id='updated-output', style={'textAlign': 'center', 'marginTop': '10px', 'backgroundColor': '#587ca4', 'color': 'white', 'padding': '10px', 'borderRadius': '5px'})
        ], style={'flex': '1', 'padding': '10px', 'border': '2px solid #587ca4', 'borderRadius': '8px', 'margin': '10px'})
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
    # Progress Chart (Stochastic or Simulated Annealing)
        html.Div([
            html.H3("Progress Over Iterations", style={'textAlign': 'center'}),
            dcc.Graph(id='progress-chart')
        ], style={'padding': '20px', 'border': '2px solid #587ca4', 'borderRadius': '8px', 'margin': '10px'}),
    
    # Acceptance Probability Chart (only for Simulated Annealing)
    html.Div([
        html.H3("Acceptance Probability (Simulated Annealing)", style={'textAlign': 'center'}),
        dcc.Graph(id='probability-chart')
        ], style={'padding': '20px', 'border': '2px solid #587ca4', 'borderRadius': '8px', 'margin': '10px'})
    ], style={'display': 'block', 'justifyContent': 'center'})
])

@app.callback(
    [Output('optimized-cube-graph', 'figure'),
     Output('updated-output', 'children'),
     Output('progress-chart', 'figure'),
     Output('probability-chart', 'figure'),
     Output('button-stochastic', 'disabled'),
     Output('button-simulated', 'disabled'),
     Output('button-best', 'disabled'),
     Output('button-sideways', 'disabled'),
     Output('button-random-restart', 'disabled'),
     Output('button-reset', 'disabled')],
    [Input('button-stochastic', 'n_clicks'),
     Input('button-simulated', 'n_clicks'),
     Input('button-best', 'n_clicks'),
     Input('button-sideways', 'n_clicks'),
     Input('button-random-restart', 'n_clicks'),
     Input('button-reset', 'n_clicks')]
)
def update_cubes(n_clicks_stochastic, n_clicks_simulated, n_clicks_best, n_clicks_sideways, n_clicks_random_restart, n_clicks_reset):
    ctx = dash.callback_context
    if not ctx.triggered:
        empty_chart = go.Figure()
        empty_chart.update_layout(
            xaxis_title="Iteration",
            yaxis_title="Success Percentage"
        )
        return [create_scatter_data(cube_size, numbers), 
                f'Objective Function: {cek_spesifikasi(cube_size, numbers)[0]}% | Initial Jumlah Elemen 315: {cek_spesifikasi(cube_size, numbers)[1]}',
                empty_chart, empty_chart,
                False, False, False, False, False, False]

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'button-reset':
        empty_chart = go.Figure()
        empty_chart.update_layout(
            xaxis_title="Iteration",
            yaxis_title="Success Percentage"
        )
        return [create_scatter_data(cube_size, numbers), 
                f'Objective Function: {cek_spesifikasi(cube_size, numbers)[0]}% | Initial Jumlah Elemen 315: {cek_spesifikasi(cube_size, numbers)[1]}',
                empty_chart, empty_chart,
                False, False, False, False, False, True]

    optimized_figure = None
    success_text = None
    progress_figure = go.Figure()
    probability_figure = go.Figure()
    disable_all = [True, True, True, True, True, False]
    
    if button_id == 'button-stochastic':
        histori = stochastic_hill_climbing(cube_size, maks_iterasi=10000, threshold_akurasi=98, kubus=numbers)
        optimized_figure = create_scatter_data(cube_size, histori['kubus_terbaik'])
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, histori['kubus_terbaik'])
        durasi = histori['elapsed_time']
        iterasi = histori['iterasi']
        success_text = f'Objective Function: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {durasi} detik | Iterasi: {iterasi}'
        
        # Update progress chart
        progress_figure.add_trace(go.Scatter(y=histori['skor_kubus'], mode='lines', name='Success Percentage'))
        progress_figure.update_layout(title="Progress Over Iterations", xaxis_title="Iteration", yaxis_title="Success Percentage")
        
    elif button_id == 'button-simulated':
        histori = simulated_annealing(cube_size, maks_iterasi=10000, threshold_akurasi=100, temperatur_awal=100,  minimum_temperatur= 1e-10, laju_penurunan=0.95, kubus=numbers)
        optimized_figure = create_scatter_data(cube_size, histori['kubus_terbaik'])
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, histori['kubus_terbaik'])
        durasi = histori['elapsed_time']
        success_text = f'Objective Function: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {durasi} detik'
        
        # Update progress chart
        progress_figure.add_trace(go.Scatter(y=histori['skor_kubus'], mode='lines', name='Success Percentage'))
        progress_figure.update_layout(title="Progress Over Iterations", xaxis_title="Iteration", yaxis_title="Success Percentage")
        
        # Update acceptance probability chart
        probability_figure.add_trace(go.Scatter(y=histori['probabilitas'], mode='lines', name='Acceptance Probability'))
        probability_figure.update_layout(title="Acceptance Probability Over Iterations", xaxis_title="Iteration", yaxis_title="Acceptance Probability")

    elif button_id == 'button-best':
        histori = steepest_ascent_hill_climbing(cube_size, numbers)
        optimized_figure = create_scatter_data(cube_size, histori['kubus_terbaik'])
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, histori['kubus_terbaik'])
        durasi = histori['elapsed_time']
        iterasi = histori['iterasi']
        success_text = f'Objective Function: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {durasi} detik | Iterasi: {iterasi}'
        
        # Update progress chart
        progress_figure.add_trace(go.Scatter(y=histori['skor_kubus'], mode='lines', name='Success Percentage'))
        progress_figure.update_layout(title="Progress Over Iterations", xaxis_title="Iteration", yaxis_title="Success Percentage")
    
    elif button_id == 'button-sideways':
        histori = sideways_move_hill_climbing(cube_size, kubus=numbers, maks_iterasi_stagnan=50)
        optimized_figure = create_scatter_data(cube_size, histori['kubus_terbaik'])
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, histori['kubus_terbaik'])
        iterasi = histori['iterasi']
        durasi = histori['elapsed_time']
        success_text = f'Objective Function: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {durasi} detik | Iterasi: {iterasi}'

        # Update progress chart for Sideways Move Hill Climbing
        progress_figure.add_trace(go.Scatter(y=histori['skor_kubus'], mode='lines', name='Success Percentage'))
        progress_figure.update_layout(title="Progress Over Iterations", xaxis_title="Iteration", yaxis_title="Success Percentage")

    elif button_id == 'button-random-restart':
        histori = random_restart_hill_climbing(cube_size, maks_restart=10, threshold_akurasi=98, kubus=numbers)
        optimized_figure = create_scatter_data(cube_size, histori['kubus_terbaik'])
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, histori['kubus_terbaik'])
        durasi = histori['elapsed_time']
        success_text = f'Objective Function: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {durasi} detik'

        # Update progress chart for Random Restart Hill Climbing
        progress_figure.add_trace(go.Scatter(y=histori['skor_kubus'], mode='lines+markers', name='Success Percentage per Restart'))
        progress_figure.update_layout(title="Progress Across Restarts", xaxis_title="Restart", yaxis_title="Success Percentage")
    
    # Return updated figures and text
    return optimized_figure, success_text, progress_figure, probability_figure, *disable_all


if __name__ == '__main__':
    app.run_server(debug=True)
