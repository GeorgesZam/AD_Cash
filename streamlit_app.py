import streamlit as st
from streamlit.components.v1 import html

# --- Custom CSS for Ultra Design ---
st.markdown(
    """
    <style>
    /* General */
    .reportview-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: #f0f0f0;
        font-family: 'Roboto', sans-serif;
    }
    /* Sidebar */
    .sidebar .sidebar-content {
        background: #162447;
    }
    .sidebar .sidebar-content h2 {
        color: #ffc947;
    }
    /* Buttons */
    .stButton>button {
        background-color: #ffc947;
        color: #162447;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    /* Forms */
    .stForm {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("Gagnez de l'argent")
menu = st.sidebar.radio(
    "Navigation", ["Accueil", "Jeux", "Vidéos/Séries", "Formulaire & Affiliation"]
)

# --- Header ---
st.markdown("# Bienvenue sur MoneyPlay! 💰🎮📺")

# --- Pages ---
if menu == "Accueil":
    st.markdown(
        """
        **MoneyPlay** est votre hub pour gagner de l'argent en vous divertissant !
        Sélectionnez une section dans la barre latérale pour commencer:
        - Jouez à des mini-jeux fun
        - Regardez des vidéos ou séries
        - Remplissez un court formulaire ou découvrez nos liens d'affiliation
        """
    )

elif menu == "Jeux":
    st.subheader("Mini-Jeux")
    st.markdown("Jouez à ce petit casse-briques intégrée:")
    # Embedded HTML game (example: Breakout)
    breakout_html = '''
    <iframe src="https://editor.p5js.org/embed/lU7dxv2fH" width="100%" height="500"></iframe>
    '''
    html(breakout_html, height=500)
    if st.button("Valider participation au jeu (10 points) 🚀"):
        st.success("Bravo ! Vos points ont été comptabilisés.")

elif menu == "Vidéos/Séries":
    st.subheader("Vidéos & Séries Sponsorisé(e)s")
    st.markdown("Regardez ces vidéos et gagnez des points:")
    # Example YouTube embeds
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if st.button("J'ai regardé la vidéo ! (5 points) 👀"):
        st.info("Votre visionnage a été enregistré.")

    st.markdown("---")
    st.markdown("**Séries recommandées**")
    series_html = '''
    <iframe src="https://player.vimeo.com/video/76979871" width="100%" height="400"></iframe>
    '''
    html(series_html, height=400)
    if st.button("Valider visionnage de la série (20 points) 🎉"):
        st.success("Vous avez gagné des points !")

else:
    st.subheader("Formulaire & Affiliations")
    with st.form(key="formulaire"):
        nom = st.text_input("Nom complet")
        email = st.text_input("Adresse email")
        pays = st.selectbox("Pays", ["France", "Belgique", "Suisse", "Canada", "Autre"])
        agree = st.checkbox("Je souhaite recevoir des offres spéciales.")
        submit = st.form_submit_button("Envoyer ✅")
    if submit:
        st.success(f"Merci {nom} ! Votre formulaire est bien reçu.")
        if agree:
            st.info("Vous allez recevoir nos meilleures offres par email.")

    st.markdown("---")
    st.markdown("**Découvrez nos offres partenaires:**")
    st.markdown("- [Offre A: Gagnez jusqu'à 50€ cashback](https://www.example.com/affiliationA)")
    st.markdown("- [Offre B: Réduction exclusive 20%](https://www.example.com/affiliationB)")
    st.markdown("- [Offre C: Inscription gratuite](https://www.example.com/affiliationC)")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 MoneyPlay. Tous droits réservés.")
