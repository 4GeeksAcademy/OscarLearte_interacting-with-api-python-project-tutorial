# Importación de Librerías

import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Carga de variables de entorno desde .env
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Autenticación con Spotipy
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Id del artista
artist_id = "5zixe6AbgXPqt4c1uSl94L"

# Top tracks (top 10) para España (ES)
top = sp.artist_top_tracks(artist_id, country="ES")
tracks = top.get("tracks", [])[:10]

# Transformar a DataFrame con nombre, popularidad y duración en minutos.
def ms_to_min(ms: int) -> float:
    return round(ms / 1000 / 60, 3)

rows = []
for t in tracks:
    rows.append({
        "track_name": t["name"],
        "popularity": t["popularity"],
        "duration_min": ms_to_min(t["duration_ms"]),
        "id": t["id"],
        "preview_url": t.get("preview_url")
    })
df = pd.DataFrame(rows)

# Ordenar por popularidad creciente y mostrar top-3
df_sorted_by_pop = df.sort_values(by="popularity", ascending=True, ignore_index=True)
print("\nTop 3 (menor popularidad entre las top tracks):")
print(df_sorted_by_pop.head(3)[["track_name", "popularity", "duration_min"]])

# Análisis estadístico e Impresión.
corr = df["duration_min"].corr(df["popularity"])
print(f"\nCorrelación Pearson duración_min vs popularidad: {corr:.3f}")

plt.figure()
plt.scatter(df["duration_min"], df["popularity"])
plt.title(f"Connor Price – Duración (min) vs Popularidad\nr = {corr:.3f}")
plt.xlabel("Duración (min)")
plt.ylabel("Popularidad (0–100)")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()