import streamlit as st
import numpy as np
import pickle
# https://www.kaggle.com/datasets/mujtabamatin/air-quality-and-pollution-assessment/code

# Chargement des modèles
path = "Air_qualityV1.sav"
path_scale = "scale.sav"
model = pickle.load(open(path, 'rb'))
scaler = pickle.load(open(path_scale, 'rb'))


# Fonction de prédiction
def predict_quality_air(temp, hum, pm2, pm10, no2, so2, co, pro_ar, pop):
    quality_class = ["BONNE", "DANGEREUSE", "MODÉRÉE", "MAUVAISE"]
    emoji = ['🤗😊', '😑', '😑😣', '😔😓']
    data = scaler.transform([[temp, hum, pm2, pm10, no2, so2, co, pro_ar, pop]])
    prediction = model.predict(np.reshape(data, (1, -1)))
    quality = int(prediction[0])
    return quality_class[quality], emoji[quality]

# Interface principale
st.set_page_config(page_title="Détection de la Qualité de l'Air", page_icon="🌍", layout="centered")
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: white;
            background-color: #007BFF;
            padding: 10px;
            border-radius: 10px;
        }
        .info {
            text-align: center;
            font-size: 16px;
            color: white;
            background-color: #28a745;
            padding: 10px;
            border-radius: 10px;
        }
        body {
            background-image: url('2001.jpg');
            background-size: cover;
        }
    </style>
""", unsafe_allow_html=True)



st.sidebar.header("Explication des ribriques", divider='rainbow')
st.sidebar.markdown("""
    *Caractéristiques principales* :
                    
    - **Température (°C)**: Température moyenne de la région.
    - **Humidité (%)**: Humidité relative enregistrée dans la région.
    - **Concentration PM2.5 (µg/m³)** : Niveau de particules fines en suspension.
    - **Concentration PM10 (µg/m³)** : Niveau de particules plus grossières en suspension.
    - **Concentration NO2 (ppb)** : Niveau de dioxyde d'azote.
    - **Concentration SO2 (ppb)** : Niveau de dioxyde de soufre.
    - **Concentration CO (ppm)** : Niveau de monoxyde de carbone.
    - **Proximité des zones industrielles (km)** : Distance jusqu'à la zone industrielle la plus proche.
    - **Densité de population (habitants/km²)** : Nombre d'habitants par kilomètre carré dans la région.
""")

# Interface Streamlit
def main():
    # Titre principal
    st.markdown(
        """
        <h1 style="text-align:center; color: white; background-color: teal; padding: 15px; border-radius: 10px;">
            🌍 Système d'Évaluation de la qualité de l'air et de la pollution 🌿
        </h1>
        
        """, unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center; color:gray;'>Analyse en temps réel de la qualité de l'air dans votre région</h4>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Formulaire d'entrée utilisateur
    st.subheader("Entrez les valeurs suivantes :")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp = st.number_input("Température (°C)", min_value=-50.0, max_value=50.0, value=25.0, step=0.1)
        hum = st.number_input("Humidité (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        pm2 = st.number_input("PM2.5 (µg/m³)", min_value=0.0, max_value=500.0, value=10.0, step=0.1)
        

    with col2:
        pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0, max_value=500.0, value=20.0, step=0.1)
        no2 = st.number_input("NO2 (ppb)", min_value=0.0, max_value=100.0, value=0.5, step=0.01)
        so2 = st.number_input("SO2 (ppb)", min_value=0.0, max_value=100.0, value=0.2, step=0.01)
        
    with col3:
        pro_ar = st.number_input("Proximité des zones industrielles (Km)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        pop = st.number_input("Densité de population (h/km²)", min_value=0.0, value=1000.0, step=1.0)
        co = st.number_input("CO (ppm)", min_value=0.0, max_value=100.0, value=0.1, step=0.01)

    # Bouton de prédiction
    if st.button("Prédire la qualité de l'air"):
        quality, reaction = predict_quality_air(temp, hum, pm2, pm10, no2, so2, co, pro_ar, pop)
        st.success(f"🌤️ La qualité de l'air est : **{quality}** {reaction}")

    # Section "À propos"
    if st.button("À propos"):
        st.markdown(
            """
            <div style="background-color:black; padding:15px; border-radius:10px;">
                <h4>📌 À propos du projet</h4>
                <p>
                    Cet outil permet aux experts environnementaux de surveiller la qualité de l'air dans leur région afin de mieux anticiper les risques potentiels.
                </p>
                <h5>📊 Catégories de qualité de l'air :</h5>
                <ul>
                    <li><strong>BONNE</strong> 😊 : Qualité de l'air excellente</li>
                    <li><strong>MODEREE</strong> 😑 : Acceptable, mais pourrait poser un risque pour les plus sensibles</li>
                    <li><strong>DANGEREUSE</strong> 😣 : Dangereuse pour la santé</li>
                    <li><strong>MAUVAISE</strong> 😔 : Mauvaise qualité, impact probable sur la santé</li>
                </ul>
                <p><i>⚠️ Note : Ces prédictions sont basées sur des estimations et peuvent varier.</i></p>
            </div>
            """, unsafe_allow_html=True
        )

# Exécution de l'application
if __name__ == "__main__":
    main()
