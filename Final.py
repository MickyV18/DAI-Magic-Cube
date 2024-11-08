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

def simulated_annealing(n, maks_iterasi, threshold_akurasi, temperatur_awal, laju_penurunan, kubus):
    kubus_terbaik = np.copy(kubus)
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)
    minimum_temperatur = 1e-8
    temperatur = temperatur_awal
    iterasi = 0

    # Membuat kubus_baru dengan initial state yang baru
    kubus_baru = np.copy(kubus)
    skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)
    
    # Track progress and probability data
    progress_data = []
    probability_data = []

    while (iterasi < maks_iterasi) and (temperatur > minimum_temperatur):

        # Membuat kubus_temp yang dihasilkan dengan fungsi swap_angka terhadap kubus_baru
        kubus_temp = swap_angka(n, np.copy(kubus_baru))
        skor_kubus_temp, jumlah_315_temp = cek_spesifikasi(n, kubus_temp)

        # Menghitung perbedaan antara skor kubus_temp dan kubus_baru
        skor_delta = skor_kubus_temp - skor_kubus_baru

        # Menerima kubus_temp dengan skor yang lebih baik atau dengan probabilitas jika skor lebih rendah
        if skor_delta > 0:
            kubus_baru = np.copy(kubus_temp)
            skor_kubus_baru = skor_kubus_temp
            jumlah_315_baru = jumlah_315_temp
        else:
            probabilitas = np.exp(skor_delta / temperatur)
            probability_data.append({
                'iteration': iterasi,
                'probability': probabilitas
            })
            
            # Print probabilitas dan temperatur untuk setiap iterasi jika skor lebih rendah
            print(f"Iteration {iterasi}: Probabilitas menerima skor lebih rendah = {probabilitas}, Temperatur = {temperatur}")
            
            if random.random() < probabilitas:
                kubus_baru = np.copy(kubus_temp)
                skor_kubus_baru = skor_kubus_temp
                jumlah_315_baru = jumlah_315_temp

        # Memperbarui kubus terbaik jika skor yang baru ditemukan lebih baik
        if skor_kubus_baru > skor_kubus_terbaik:
            kubus_terbaik = np.copy(kubus_baru)
            skor_kubus_terbaik = skor_kubus_baru
            jumlah_315_terbaik = jumlah_315_baru

            # Menampilkan informasi pada kubus dengan skor terbaik baru
            print(f"\nPerbaikan pada iterasi ke-{iterasi}:")
            print(f"Skor kubus terbaik baru: {skor_kubus_terbaik}")
            print(f"Jumlah magic number terbaik baru: {jumlah_315_terbaik}")

        # Menurunkan temperatur seiring berjalannya iterasi
        temperatur *= laju_penurunan
        iterasi += 1

        # Record progress setiap 10 iterasi
        if iterasi % 10 == 0:
            progress_data.append({
                'iteration': iterasi,
                'score': skor_kubus_terbaik
            })

    # Cetak hasil akhir
    if iterasi == maks_iterasi:
        print(f"\nBatas maksimum iterasi ({maks_iterasi}) tercapai.")
    else:
        print(f"\nAlgoritma selesai pada iterasi {iterasi}.")

    # Cetak visualisasi kondisi terbaik kubus
    print(f"\nSkor hasil kubus terbaik: {skor_kubus_terbaik}")
    print(f"Jumlah magic number terbaik: {jumlah_315_terbaik}")

    return kubus_terbaik, progress_data, probability_data



def stochastic_hill_climbing(n, maks_iterasi, threshold_akurasi, kubus):
    kubus_terbaik = kubus
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)
    iterasi = 0
    
    # Track progress for every iteration
    progress_data = [{
        'iteration': 0,
        'score': skor_kubus_terbaik
    }]

    while iterasi < maks_iterasi:
        kubus_baru = swap_angka(n, np.copy(kubus_terbaik))
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)
        iterasi += 1

        if skor_kubus_baru > skor_kubus_terbaik:
            skor_kubus_terbaik = skor_kubus_baru
            jumlah_315_terbaik = jumlah_315_baru
            kubus_terbaik = np.copy(kubus_baru)

            print(f"\nImprovement at iteration {iterasi}:")
            print(f"New cube score: {skor_kubus_terbaik}")
            print(f"Magic number count: {jumlah_315_terbaik}")

            if skor_kubus_terbaik >= threshold_akurasi:
                print(f"Threshold accuracy ({threshold_akurasi}%) reached at iteration {iterasi}!")
                break
        
        # Record progress for every iteration
        progress_data.append({
            'iteration': iterasi,
            'score': skor_kubus_terbaik
        })

    if iterasi == maks_iterasi:
        print(f"\nMaximum iteration limit ({maks_iterasi}) reached.")
    else:
        print(f"\nAlgorithm completed at iteration {iterasi}.")

    print(f"\nBest cube score: {skor_kubus_terbaik}")
    print(f"Magic number count: {jumlah_315_terbaik}")

    return kubus_terbaik, progress_data

def steepest_ascent_hill_climbing(n, kubus):
    # Initialize the best cube with the input cube
    kubus_terbaik = np.copy(kubus)

    # Initialize the best cube score with the input cube score
    skor_kubus_terbaik, jumlah_315_terbaik = cek_spesifikasi(n, kubus_terbaik)

    # Initialize the best cube status with True to start iteration
    status_kubus_terbaik = True

    # Count the number of iterations
    iterasi = 0

    # Iterate until there is no score improvement
    while status_kubus_terbaik:
        # Select the best neighbor from all possible neighbors of the current best cube state
        kubus_baru = generate_best_neighbors(n, kubus_terbaik)

        # Calculate the score of the new cube
        skor_kubus_baru, jumlah_315_baru = cek_spesifikasi(n, kubus_baru)
        iterasi += 1

        # If the new score is better, update the best cube
        if skor_kubus_baru > skor_kubus_terbaik:
            kubus_terbaik = np.copy(kubus_baru)
            skor_kubus_terbaik = skor_kubus_baru
            jumlah_315_terbaik = jumlah_315_baru

            print(f"\nImprovement in iteration {iterasi}:")
            print(f"New best cube score: {skor_kubus_terbaik}")
            print(f"Magic number count: {jumlah_315_terbaik}")

            # Stop if the perfect score (100%) is reached
            if skor_kubus_terbaik == 100:
                print(f"\nPerfect solution found in iteration {iterasi}!")
                break

        else:
            # If there is no improvement, stop the iteration
            status_kubus_terbaik = False
            print(f"\nAlgorithm completed in iteration {iterasi}.")
            break

    print(f"\nBest cube score: {skor_kubus_terbaik}")
    print(f"Best magic number count: {jumlah_315_terbaik}")

    return kubus_terbaik

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
                f'Persentase Sukses: {cek_spesifikasi(cube_size, numbers)[0]}% | Initial Jumlah Elemen 315: {cek_spesifikasi(cube_size, numbers)[1]}', 
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
     Output('button-reset', 'disabled')],
    [Input('button-stochastic', 'n_clicks'),
     Input('button-simulated', 'n_clicks'),
     Input('button-best', 'n_clicks'),
     Input('button-reset', 'n_clicks')]
)

def update_cubes(n_clicks_stochastic, n_clicks_simulated, n_clicks_best, n_clicks_reset):
    ctx = dash.callback_context
    if not ctx.triggered:
        empty_chart = go.Figure()
        empty_chart.update_layout(
            xaxis_title="Iteration",
            yaxis_title="Success Percentage"
        )
        return [create_scatter_data(cube_size, numbers), 
                f'Persentase Sukses: {cek_spesifikasi(cube_size, numbers)[0]}% | Initial Jumlah Elemen 315: {cek_spesifikasi(cube_size, numbers)[1]}',
                empty_chart, empty_chart,
                False, False, False, False]

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'button-reset':
        empty_chart = go.Figure()
        empty_chart.update_layout(
            xaxis_title="Iteration",
            yaxis_title="Success Percentage"
        )
        return [create_scatter_data(cube_size, numbers), 
                f'Persentase Sukses: {cek_spesifikasi(cube_size, numbers)[0]}% | Initial Jumlah Elemen 315: {cek_spesifikasi(cube_size, numbers)[1]}',
                empty_chart, empty_chart,
                False, False, False, True]

    optimized_figure = None
    success_text = None
    progress_figure = None
    probability_figure = None
    disable_all = [True, True, True, False]

    # Start measuring time
    start_time = time.time()

    if button_id == 'button-stochastic':
        optimized_cube, progress_data = stochastic_hill_climbing(cube_size, maks_iterasi=10000, threshold_akurasi=98, kubus=numbers)
        optimized_figure = create_scatter_data(cube_size, optimized_cube)
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, optimized_cube)

        # Calculate duration
        duration = time.time() - start_time

        success_text = f'Persentase Sukses: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {round(duration, 2)} detik'
        
        # Create progress chart
        progress_figure = go.Figure()
        progress_figure.add_trace(go.Scatter(
            x=[d['iteration'] for d in progress_data],
            y=[d['score'] for d in progress_data],
            mode='lines+markers',
            name='Stochastic Hill Climbing'
        ))
        progress_figure.update_layout(
            title='Progress of Stochastic Hill Climbing',
            xaxis_title='Iteration',
            yaxis_title='Success Percentage'
        )
        
        # Empty probability chart for stochastic hill climbing
        probability_figure = go.Figure()
        probability_figure.update_layout(
            title='No Probability Data for Stochastic Hill Climbing',
            xaxis_title='Iteration',
            yaxis_title='Acceptance Probability'
        )

    elif button_id == 'button-simulated':
        optimized_cube, progress_data, probability_data = simulated_annealing(cube_size, maks_iterasi=1000, threshold_akurasi=100, temperatur_awal=1000, laju_penurunan=0.99, kubus=numbers)
        optimized_figure = create_scatter_data(cube_size, optimized_cube)
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, optimized_cube)
        
        duration = time.time() - start_time
        
        success_text = f'Persentase Sukses: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {round(duration, 2)} detik'
        
        # Create progress chart
        progress_figure = go.Figure()
        progress_figure.add_trace(go.Scatter(
            x=[d['iteration'] for d in progress_data],
            y=[d['score'] for d in progress_data],
            mode='lines+markers',
            name='Simulated Annealing'
        ))
        progress_figure.update_layout(
            title='Progress of Simulated Annealing',
            xaxis_title='Iteration',
            yaxis_title='Success Percentage'
        )
        
        # Create probability chart
        probability_figure = go.Figure()
        probability_figure.add_trace(go.Scatter(
            x=[d['iteration'] for d in probability_data],
            y=[d['probability'] for d in probability_data],
            mode='lines',
            name='Acceptance Probability'
        ))
        probability_figure.update_layout(
            title='Acceptance Probability over Iterations',
            xaxis_title='Iteration',
            yaxis_title='Probability',
            yaxis=dict(range=[0, 1])
        )

    elif button_id == 'button-best':
        optimized_cube = steepest_ascent_hill_climbing(cube_size, numbers)
        optimized_figure = create_scatter_data(cube_size, optimized_cube)
        persentase_sukses, jumlah_315 = cek_spesifikasi(cube_size, optimized_cube)
        duration = time.time() - start_time
        success_text = f'Persentase Sukses: {persentase_sukses}% | Jumlah Elemen 315: {jumlah_315} | Durasi: {round(duration, 2)} detik'
        
        # Empty charts for steepest ascent
        progress_figure = go.Figure()
        progress_figure.update_layout(
            title='No Progress Chart for Steepest Ascent',
            xaxis_title='Iteration',
            yaxis_title='Success Percentage'
        )
        
        probability_figure = go.Figure()
        probability_figure.update_layout(
            title='No Probability Data for Steepest Ascent',
            xaxis_title='Iteration',
            yaxis_title='Acceptance Probability'
        )

    return optimized_figure, success_text, progress_figure, probability_figure, *disable_all

if __name__ == '__main__':
    app.run_server(debug=True)
