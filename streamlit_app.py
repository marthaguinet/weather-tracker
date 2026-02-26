import streamlit as st
import requests
import math

st.set_page_config(page_title="Lille Humidité Cible", page_icon="💧")

def get_lille_data():
    # API Open-Meteo pour Lille (Latitude 50.63, Longitude 3.06)
    url = "https://api.open-meteo.com/v1/forecast?latitude=50.6292&longitude=3.0573&current=temperature_2m,dew_point_2m&timezone=Europe%2FParis"
    try:
        data = requests.get(url).json()
        return data['current']['temperature_2m'], data['current']['dew_point_2m']
    except:
        return None, None

def calc_rh(dp, t_int):
    # Formule physique pour retrouver le %RH à partir du point de rosée
    # Basé sur la pression de vapeur saturante
    ps_dp = math.exp((17.625 * dp) / (243.04 + dp))
    ps_t = math.exp((17.625 * t_int) / (243.04 + t_int))
    return min(100.0, (ps_dp / ps_t) * 100)

st.title("💧 Humidité Cible à Lille")

t_ext, dp_ext = get_lille_data()

if t_ext is not None:
    st.metric("Extérieur (Lille)", f"{t_ext} °C", help=f"Point de rosée actuel : {dp_ext}°C")
    
    st.write("---")
    
    # Saisie de ta température intérieure
    t_int = st.number_input("Ta température intérieure (°C)", min_value=10.0, max_value=35.0, value=20.0, step=0.5)
    
    # Calcul
    rh_cible = calc_rh(dp_ext, t_int)
    
    # Affichage du résultat
    st.subheader(f"Humidité relative chez toi :")
    st.title(f"{round(rh_cible, 1)} %")
    
    st.info(f"Si ton hygromètre affiche plus de {round(rh_cible, 1)}%, il est temps d'ouvrir les fenêtres pour évacuer l'humidité intérieure.")
else:
    st.error("Erreur de connexion aux données météo.")
