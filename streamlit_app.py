import streamlit as st
import sqlite3
import time
import hashlib
from datetime import datetime
import random

# --------------------- Configuration initiale ---------------------
conn = sqlite3.connect('adcash.db', check_same_thread=False)
c = conn.cursor()

# Création des tables SQLite
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE, 
              password TEXT,
              email TEXT,
              points INTEGER DEFAULT 0,
              registration_date DATETIME)''')

c.execute('''CREATE TABLE IF NOT EXISTS activities
             (user_id INTEGER,
              activity_type TEXT,
              points_earned INTEGER,
              timestamp DATETIME)''')

# --------------------- Fonctions d'authentification ---------------------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def create_user(username, password, email):
    hashed_password = make_hashes(password)
    c.execute('INSERT INTO users (username, password, email, registration_date) VALUES (?,?,?,?)',
              (username, hashed_password, email, datetime.now()))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    data = c.fetchone()
    if data and check_hashes(password, data[2]):
        return data
    return None

# --------------------- Système de points ---------------------
def add_points(amount):
    user = st.session_state.user
    c.execute('UPDATE users SET points = points + ? WHERE id = ?',
             (amount, user[0]))
    conn.commit()
    st.session_state.user = list(user)
    st.session_state.user[4] += amount
    st.toast(f"+ {amount} points! 🎉", icon="✅")

# --------------------- Interface utilisateur ---------------------
def main_app():
    # --------------------- CSS Personnalisé ---------------------
    st.markdown("""
    <style>
        .main {
            background-image: linear-gradient(to right, #1a1a1a, #2d2d2d);
            color: #ffffff;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 25px;
            padding: 10px 24px;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------- Barre latérale ---------------------
    with st.sidebar:
        st.title("AD_Cash 🎮💰")
        menu = st.radio("Navigation", ["🏠 Accueil", "🎮 Jeux", "📺 Vidéos", "📝 Sondages", "💰 Mon Portefeuille"])
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            st.experimental_rerun()

    # --------------------- Pages ---------------------
    if menu == "🏠 Accueil":
        st.header("Bienvenue sur AD_Cash!")
        st.write(f"Bonjour {st.session_state.user[1]}! 👋")
        st.metric("Points accumulés", f"{st.session_state.user[4]} 🪙")

    elif menu == "🎮 Jeux":
        game_tab1, game_tab2, game_tab3 = st.tabs(["🎲 Jeux Instantanés", "🏆 Tournois", "📜 Historique"])
        with game_tab1:
            st.header("Jeu de dés")
            if st.button("Lancer les dés 🎲"):
                result = random.randint(1, 6)
                st.success(f"Résultat: {result}")
                if result == 6:
                    st.balloons()
                    add_points(50)
            st.write("Chaque 6 rapporte 50 points !")
        with game_tab2:
            st.header("Tournois")
            st.write("Section Tournois en cours de développement...")
        with game_tab3:
            st.header("Historique des Activités")
            c.execute('SELECT activity_type, points_earned, timestamp FROM activities WHERE user_id = ?', (st.session_state.user[0],))
            rows = c.fetchall()
            for act, pts, ts in rows:
                st.write(f"{ts}: {act} (+{pts} points)")

    elif menu == "📺 Vidéos":
        st.header("Regardez des vidéos sponsorisées")
        if st.button("Regarder (30s) - 10 points"):
            with st.spinner("Vidéo en cours..."):
                time.sleep(30)
                add_points(10)

    elif menu == "📝 Sondages":
        with st.form("survey_form"):
            st.write("## Questionnaire rémunéré")
            q1 = st.radio("Quelle est votre tranche d'âge?", ["18-25", "26-35", "36-45"])
            q2 = st.multiselect("Centres d'intérêt", ["Technologie", "Sport", "Cinéma"])
            if st.form_submit_button("Soumettre le questionnaire"):
                add_points(25)
                st.success("Merci! 25 points ajoutés!")

    elif menu == "💰 Mon Portefeuille":
        st.header("Gestion des gains")
        st.write(f"Solde actuel: {st.session_state.user[4]} points")
        with st.expander("Convertir en argent"):
            convert_amount = st.number_input("Points à convertir", min_value=100)
            if st.button("Confirmer conversion"):
                if st.session_state.user[4] >= convert_amount:
                    new_balance = st.session_state.user[4] - convert_amount
                    c.execute('UPDATE users SET points = ? WHERE id = ?', (new_balance, st.session_state.user[0]))
                    conn.commit()
                    st.success(f"Conversion réussie! Montant envoyé: {convert_amount*0.01}€")

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
                    st.session_state.logged_in = True
                    st.session_state.user = user
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
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if st.session_state.logged_in:
    main_app()
else:
    login_page()

conn.close()
