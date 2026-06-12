import streamlit as st
import requests
import math

# Test Review PR Claude

# Configuration
st.set_page_config(page_title="Lille Humidité", page_icon="💧")

# CSS pour forcer le contraste et la visibilité
st.markdown("""
    <style>
    /* On force le fond de la page en gris très clair pour éviter le blanc sur blanc */
    .stApp {
        background-color: #f0f2f6 !important;
    }
    
    /* On force tout le texte en noir ou gris très foncé */
    h1, h2, h3, p, span, label {
        color: #1a1a1a !important;
    }

    /* Cadres des métriques météo */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #007bff !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.1) !important;
    }

    /* Grand cadre de résultat */
    .result-container {
        background-color: #007bff !important;
        color: white !important;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 20px rgba(0,123,255,0.3);
    }
    
    .result-container h1 {
        color: white !important;
        font-size: 4rem !important;
        margin: 0;
    }

    .result-container p {
        color: #e0e0e0 !important;
        font-size: 1.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=50.6292&longitude=3.0573&current=temperature_2m,relative_humidity_2m,dew_point_2m&timezone=Europe%2FParis"
    try:
        r = requests.get(url).json()
        return r['current']
    except: return None

def calc_rh(dp, t_int):
    # Formule Magnus-Tetens
    ps_dp = math.exp((17.625 * dp) / (243.04 + dp))
    ps_t = math.exp((17.625 * t_int) / (243.04 + t_int))
    return min(100.0, (ps_dp / ps_t) * 100)

# --- Contenu ---
st.write("# 🌡️ Lille Air Check")

data = get_weather()

if data:
    # Infos Lille en haut
    st.write("### Météo actuelle à Lille")
    c1, c2, c3 = st.columns(3)
    c1.metric("Temp. Ext.", f"{data['temperature_2m']}°C")
    c2.metric("Humidité Ext.", f"{data['relative_humidity_2m']}%")
    c3.metric("Point de Rosée", f"{data['dew_point_2m']}°C")

    st.write("---")

    # Curseur température
    st.write("### 🏠 Votre domicile")
    t_int = st.slider("Quelle température fait-il chez vous ?", 15.0, 30.0, 20.0, 0.5)

    # Calcul
    rh_cible = calc_rh(data['dew_point_2m'], t_int)

    # Résultat dans un gros bloc bleu pour être sûr de le voir
    st.markdown(f"""
        <div class="result-container">
            <p>HUMIDITÉ CIBLE CHEZ VOUS</p>
            <h1>{round(rh_cible, 1)}%</h1>
        </div>
    """, unsafe_allow_html=True)

    # Conseils
    if rh_cible < 35:
        st.info("💡 Air sec. L'air extérieur contient peu d'eau.")
    elif rh_cible > 60:
        st.error("⚠️ Risque de condensation ! Aérez pour évacuer l'eau.")
    else:
        st.success("✅ Taux idéal.")

    st.write("---")
    st.caption("Source : Open-Meteo | Physique : Point de Rosée")

else:
    st.error("Données météo indisponibles.")
