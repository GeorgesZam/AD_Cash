import streamlit as st
import time
import random
from datetime import datetime

# --------------------- Stockage en mémoire ---------------------
if 'users' not in st.session_state:
    st.session_state.users = {}  # username -> {password, email, points, activities, registration_date}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# --------------------- Fonctions d'authentification ---------------------
def create_user(username, password, email):
    st.session_state.users[username] = {
        'password': password,
        'email': email,
        'points': 0,
        'activities': [],
        'registration_date': datetime.now()
    }

def login_user(username, password):
    user = st.session_state.users.get(username)
    if user and user['password'] == password:
        return username
    return None

# --------------------- Système de points ---------------------
def add_points(amount, activity_type=""):
    user_key = st.session_state.current_user
    user = st.session_state.users[user_key]
    user['points'] += amount
    if activity_type:
        user['activities'].append((activity_type, amount, datetime.now()))
    st.toast(f"+ {amount} points! 🎉", icon="✅")

# --------------------- Interface utilisateur ---------------------
def main_app():
    st.title("AD_Cash 🎮💰")

    with st.sidebar:
        menu = st.radio("Navigation", ["🏠 Accueil", "🎮 Jeux", "📺 Vidéos", "📝 Sondages", "💰 Mon Portefeuille"])
        if st.button("Déconnexion"):
            st.session_state.current_user = None
            st.rerun()

    user = st.session_state.users[st.session_state.current_user]

    if menu == "🏠 Accueil":
        st.header(f"Bienvenue {st.session_state.current_user}!")
        st.metric("Points accumulés", f"{user['points']} 🪙")

    elif menu == "🎮 Jeux":
        game_tab1, game_tab2, game_tab3 = st.tabs(["🎲 Jeux Instantanés", "🏆 Tournois", "📜 Historique"])
        with game_tab1:
            st.header("Jeu de dés")
            if st.button("Lancer les dés 🎲"):
                result = random.randint(1, 6)
                st.success(f"Résultat: {result}")
                if result == 6:
                    st.balloons()
                    add_points(50, "Dés 6")
            st.write("Chaque 6 rapporte 50 points !")
        with game_tab2:
            st.header("Tournois")
            st.write("Section Tournois en cours de développement...")
        with game_tab3:
            st.header("Historique des Activités")
            for act, pts, ts in user['activities']:
                st.write(f"{ts.strftime('%Y-%m-%d %H:%M:%S')}: {act} (+{pts} points)")

    elif menu == "📺 Vidéos":
        st.header("Regardez des vidéos sponsorisées")
        if st.button("Regarder (30s) - 10 points"):
            with st.spinner("Vidéo en cours..."):
                time.sleep(30)
                add_points(10, "Vidéo")

    elif menu == "📝 Sondages":
        with st.form("survey_form"):
            st.write("## Questionnaire rémunéré")
            q1 = st.radio("Quelle est votre tranche d'âge?", ["18-25", "26-35", "36-45"])
            q2 = st.multiselect("Centres d'intérêt", ["Technologie", "Sport", "Cinéma"])
            if st.form_submit_button("Soumettre le questionnaire"):
                add_points(25, "Sondage")
                st.success("Merci! 25 points ajoutés!")

    elif menu == "💰 Mon Portefeuille":
        st.header("Gestion des gains")
        st.write(f"Solde actuel: {user['points']} points")
        with st.expander("Convertir en argent"):
            convert_amount = st.number_input("Points à convertir", min_value=100)
            if st.button("Confirmer conversion"):
                if user['points'] >= convert_amount:
                    user['points'] -= convert_amount
                    st.success(f"Conversion réussie! Montant envoyé: {convert_amount*0.01}€")
                else:
                    st.error("Pas assez de points.")

# --------------------- Page de login ---------------------
def login_page():
    st.title("AD_Cash - Connexion")
    tab1, tab2 = st.tabs(["Connexion", "Inscription"])
    with tab1:
        with st.form("Login"):
            username = st.text_input("Nom d'utilisateur")
            password = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("Se connecter"):
                user = login_user(username, password)
                if user:
                    st.session_state.current_user = user
                    st.experimental_rerun()
                else:
                    st.error("Identifiants incorrects")
    with tab2:
        with st.form("Signup"):
            new_user = st.text_input("Nouvel utilisateur")
            new_email = st.text_input("Email")
            new_pass = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("Créer compte"):
                create_user(new_user, new_pass, new_email)
                st.success("Compte créé! Connectez-vous")

# --------------------- Execution principale ---------------------
if st.session_state.current_user:
    main_app()
else:
    login_page()
