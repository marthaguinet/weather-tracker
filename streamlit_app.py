import streamlit as st
import requests
import math

# Configuration de la page
st.set_page_config(page_title="Lille Air Check", page_icon="💧", layout="centered")

# Style personnalisé pour améliorer l'UI
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .result-box {
        padding: 20px;
        border-radius: 15px;
        background-color: #e1f5fe;
        border: 1px solid #01579b;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

def get_lille_weather():
    # Coordonnées de Lille (Lesquin)
    url = "https://api.open-meteo.com/v1/forecast?latitude=50.6292&longitude=3.0573&current=temperature_2m,relative_humidity_2m,dew_point_2m&timezone=Europe%2FParis"
    try:
        data = requests.get(url).json()
        return data['current']
    except:
        return None

def calc_rh(dp, t_int):
    # Formule de Magnus-Tetens
    A, B = 17.625, 243.04
    ps_dp = math.exp((A * dp) / (B + dp))
    ps_t = math.exp((A * t_int) / (B + t_int))
    return min(100.0, (ps_dp / ps_t) * 100)

# --- HEADER ---
st.title("🌡️ Lille Air Check")
st.markdown("Comparez l'humidité extérieure de Lille avec votre intérieur via le **point de rosée**.")

weather = get_lille_weather()

if weather:
    t_ext = weather['temperature_2m']
    rh_ext = weather['relative_humidity_2m']
    dp_ext = weather['dew_point_2m']

    # --- SECTION MÉTÉO EXTÉRIEURE ---
    st.subheader("📍 Conditions actuelles à Lille")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temp. Ext.", f"{t_ext} °C")
    col2.metric("Humidité Ext.", f"{rh_ext} %")
    col3.metric("Pt de Rosée", f"{dp_ext} °C")
    
    st.caption("Source des données : [Open-Meteo (DWD/ICON)](https://open-meteo.com/)")

    st.divider()

    # --- SECTION CALCUL ---
    st.subheader("🏠 Votre Intérieur")
    t_int = st.slider("Température de votre domicile (°C)", 15.0, 28.0, 20.0, 0.5)
    
    rh_cible = calc_rh(dp_ext, t_int)

    # --- AFFICHAGE DU RÉSULTAT ---
    st.markdown(f"""
        <div class="result-box">
            <p style='margin-bottom:0; font-size: 1.2rem; color: #01579b;'>Humidité relative théorique chez vous :</p>
            <h1 style='margin-top:0; color: #01579b; font-size: 3.5rem;'>{round(rh_cible, 1)} %</h1>
        </div>
    """, unsafe_allow_html=True)

    # --- INTERPRÉTATION ---
    st.write("") # Espacement
    if rh_cible < 35:
        st.warning("🫁 **Air très sec.** L'air extérieur contient peu d'eau. En chauffant à cette température, l'air devient irritant pour les voies respiratoires.")
    elif 35 <= rh_cible <= 55:
        st.success("✨ **Air idéal.** C'est la zone de confort parfaite pour votre santé et votre logement.")
    else:
        st.error("⚠️ **Risque de condensation.** L'air extérieur est très chargé en eau. Si votre hygromètre réel dépasse ce chiffre, ouvrez vite les fenêtres !")

else:
    st.error("Impossible de joindre les serveurs météo. Vérifiez votre connexion.")

# --- FOOTER ---
st.divider()
st.markdown("""
    <small>💡 **Comment ça marche ?** L'air froid contient peu de vapeur d'eau. En entrant chez vous, cet air se réchauffe. 
    Son point de rosée reste fixe, ce qui fait chuter son humidité relative. Ce site vous donne le taux que vous devriez 
    avoir si votre air était 100% renouvelé.</small>
""", unsafe_allow_html=True)
