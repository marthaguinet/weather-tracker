import streamlit as st
import requests
import math

# Configuration de la page
st.set_page_config(page_title="Lille Air Check", page_icon="💧", layout="centered")

# CSS Avancé pour un look moderne
st.markdown("""
    <style>
    /* Force le fond en blanc/gris très clair */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Style des cartes de métriques */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }

    /* Cadre de résultat principal */
    .result-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin: 20px 0;
        border-left: 8px solid #007bff;
    }

    .result-value {
        font-size: 4rem;
        font-weight: 800;
        color: #007bff;
        margin: 0;
    }

    .result-label {
        font-size: 1.2rem;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Personnalisation du slider */
    .stSlider {
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def get_lille_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=50.6292&longitude=3.0573&current=temperature_2m,relative_humidity_2m,dew_point_2m&timezone=Europe%2FParis"
    try:
        data = requests.get(url).json()
        return data['current']
    except:
        return None

def calc_rh(dp, t_int):
    A, B = 17.625, 243.04
    ps_dp = math.exp((A * dp) / (B + dp))
    ps_t = math.exp((A * t_int) / (B + t_int))
    return min(100.0, (ps_dp / ps_t) * 100)

# --- CONTENU DE LA PAGE ---
st.markdown("<h1 style='text-align: center; color: #1e3d59;'>💧 Lille Air Quality</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Calcul de l'humidité intérieure idéale via le point de rosée</p>", unsafe_allow_html=True)

weather = get_lille_weather()

if weather:
    # 1. Dashboard Extérieur
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Temp. Lille", f"{weather['temperature_2m']}°C")
    with col2:
        st.metric("Humidité Lille", f"{weather['relative_humidity_2m']}%")
    with col3:
        st.metric("Point de Rosée", f"{weather['dew_point_2m']}°C")

    st.write("")
    
    # 2. Entrée utilisateur
    st.markdown("### 🏠 Réglage de votre intérieur")
    t_int = st.select_slider(
        "Quelle température fait-il chez vous ?",
        options=[i/2 for i in range(30, 61)], # De 15.0 à 30.0
        value=20.0
    )

    # 3. Calcul et Affichage stylisé
    rh_cible = calc_rh(weather['dew_point_2m'], t_int)
    
    st.markdown(f"""
        <div class="result-card">
            <p class="result-label">Humidité cible conseillée</p>
            <p class="result-value">{round(rh_cible, 1)}%</p>
        </div>
    """, unsafe_allow_html=True)

    # 4. Alertes visuelles
    if rh_cible < 35:
        st.info("💡 **Note :** L'air sera sec. Hydratez-vous bien !")
    elif rh_cible > 55:
        st.warning("⚠️ **Attention :** Risque de buée sur les vitres. Pensez à aérer 5 min.")
    else:
        st.success("✅ **Parfait :** C'est le taux idéal pour Lille aujourd'hui.")

    # 5. Footer & Source
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; color: #7f8c8d; font-size: 0.8rem;'>
            Données en temps réel : <b>Open-Meteo</b> (Station Lille-Lesquin)<br>
            <i>Physique : Formule de Magnus-Tetens</i>
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("Impossible de récupérer la météo. Réessayez dans un instant.")
