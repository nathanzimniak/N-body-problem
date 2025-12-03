import csv

def save_data(traj_x, traj_y, traj_z, times, N_bodies):
    # --- Export des données dans un fichier CSV ---
    output_file = "output.csv"
    
    with open(output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "body", "x", "y", "z"])
    
        for k, tk in enumerate(times):
            for i in range(N_bodies):
                writer.writerow([tk, i, traj_x[i][k], traj_y[i][k], traj_z[i][k]])
    
    print(f"Données enregistrées dans {output_file}")