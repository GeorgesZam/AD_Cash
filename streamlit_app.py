import streamlit as st
import random

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
    /* Tabs */
    .stTabs [role="tablist"] {
        background: #162447;
        border-radius: 10px;
        padding: 5px;
    }
    .stTabs button[role="tab"] {
        background-color: #1e3c72;
        color: #ffc947;
        border-radius: 10px;
        padding: 8px 16px;
        margin-right: 4px;
        font-weight: bold;
        transition: transform 0.2s;
    }
    .stTabs button[role="tab"][aria-selected="true"] {
        background-color: #ffc947;
        color: #162447;
    }
    .stTabs button[role="tab"]:hover {
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

# --- Header ---
st.markdown("# Bienvenue sur MoneyPlay! 💰🎮📺")

# Initialize session state for game and points
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 10)
    st.session_state.attempts = 0
if 'points' not in st.session_state:
    st.session_state.points = 0

# --- Main Tabs ---
tabs = st.tabs(["Accueil", "Jeux", "Vidéos/Séries", "Formulaire & Affiliation"])

# --- Page: Accueil ---
with tabs[0]:
    st.markdown(
        """
        **MoneyPlay** est votre hub pour gagner de l'argent en vous divertissant !

        **Que voulez-vous faire aujourd'hui ?**
        
        - 🎮 Jouer à des mini-jeux fun (10 points par victoire)
        - 📺 Regarder des vidéos ou séries sponsorisées (5-20 points)
        - 📝 Remplir un formulaire et découvrir nos offres d'affiliation
        """
    )

# --- Page: Jeux ---
with tabs[1]:
    st.subheader("Jeu : Devinez le nombre 🎲")
    st.markdown("**Objectif** : Devinez le nombre entre 1 et 10. Chaque victoire rapporte 10 points.")
    guess = st.number_input("Votre proposition :", min_value=1, max_value=10, step=1)
    if st.button("Valider ma proposition"):
        st.session_state.attempts += 1
        if guess == st.session_state.target:
            st.success(f"Bravo ! Vous avez trouvé en {st.session_state.attempts} essai(s).")
            st.session_state.points += 10
            # Réinitialiser pour nouvelle partie
            st.session_state.target = random.randint(1, 10)
            st.session_state.attempts = 0
        elif guess < st.session_state.target:
            st.warning("C'est plus !")
        else:
            st.warning("C'est moins !")
    st.markdown(f"**Points actuels** : {st.session_state.points}")

# --- Page: Vidéos/Séries ---
with tabs[2]:
    st.subheader("Vidéos & Séries Sponsorisé(e)s 🎬")
    st.markdown("Regardez ces vidéos et gagnez des points:")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if st.button("J'ai regardé la vidéo ! (5 points) 👀"):
        st.session_state.points += 5
        st.info(f"Votre visionnage a été enregistré. Points totaux : {st.session_state.points}")

    st.markdown("---")
    st.markdown("**Séries recommandées**")
    # Exemple sans iframe, juste lien et image
    st.markdown("[Regarder la série sur Vimeo](https://vimeo.com/76979871)")
    if st.button("J'ai visionné la série ! (20 points) 🎉"):
        st.session_state.points += 20
        st.success(f"Vous avez gagné des points ! Total : {st.session_state.points}")

# --- Page: Formulaire & Affiliation ---
with tabs[3]:
    st.subheader("Formulaire & Affiliations 📋")
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
st.markdown(f"© 2025 MoneyPlay. Tous droits réservés. Points totaux : {st.session_state.points}")
