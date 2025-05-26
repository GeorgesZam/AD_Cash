import streamlit as st
import sqlite3
import time
from streamlit_lottie import st_lottie
import requests
import hashlib
from datetime import datetime

# --------------------- Configuration initiale ---------------------
conn = sqlite3.connect('adcash.db')
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

# --------------------- Animations Lottie ---------------------
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_coins = load_lottie('https://assets1.lottiefiles.com/packages/lf20_4kx2q32n.json')
lottie_welcome = load_lottie('https://assets8.lottiefiles.com/packages/lf20_hi95bvmx/Hello.json')

# --------------------- Fonctions d'authentification ---------------------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

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

# --------------------- Interface utilisateur ---------------------
def main_app():
    st.session_state.current_page = 'home'
    
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
        
        .tab-content {
            animation: fadeIn 1s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------- Barre latérale ---------------------
    with st.sidebar:
        st_lottie(lottie_coins, height=150, key="sidebar-coins")
        menu = st.radio("Navigation", ["🏠 Accueil", "🎮 Jeux", "📺 Vidéos", "📝 Sondages", "💰 Mon Portefeuille"])
        
        if st.button("Déconnexion"):
            st.session_state.logged_in = False
            st.experimental_rerun()

    # --------------------- Pages ---------------------
    if menu == "🏠 Accueil":
        with st.container():
            cols = st.columns([1,3])
            with cols[0]:
                st_lottie(lottie_welcome, height=200)
            with cols[1]:
                st.title("Bienvenue sur AD_Cash!")
                st.write(f"Bonjour {st.session_state.user[1]}! 👋")
                
            # Widgets de progression
            st.subheader("Votre progression")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Points accumulés", f"{st.session_state.user[4]} 🪙")
            with col2:
                st.metric("Niveau actuel", "15 🏆")
            with col3:
                st.metric("Classement", "#45 📈")

    elif menu == "🎮 Jeux":
        # Système d'onglets pour les jeux
        game_tab1, game_tab2, game_tab3 = st.tabs(["🎲 Jeux Instantanés", "🏆 Tournois", "📜 Historique"])
        
        with game_tab1:
            st.header("Jeux Rapides")
            # Jeu de dés
            if st.button("Lancer les dés 🎲"):
                result = random.randint(1,6)
                st.success(f"Résultat: {result}")
                if result == 6:
                    st.balloons()
                    add_points(50)
            
            # Jeu de mémoire
            st.subheader("Jeu de mémoire")
            # Implémentation du jeu de mémoire ici...

    elif menu == "📺 Vidéos":
        # Système de visionnage avec minuterie
        st.header("Regardez des vidéos et gagnez")
        video_col = st.columns(3)
        
        with video_col[0]:
            st.video("https://youtu.be/sample-video1")
            if st.button("Regarder (30s) - 10 points"):
                with st.spinner("Vidéo en cours..."):
                    time.sleep(30)
                    add_points(10)
        
        # Ajouter plus de contenu vidéo...

    elif menu == "📝 Sondages":
        # Système de formulaire dynamique
        with st.form("survey_form"):
            st.write("## Questionnaire rémunéré")
            q1 = st.radio("Quelle est votre tranche d'âge?", ["18-25", "26-35", "36-45"])
            q2 = st.multiselect("Centres d'intérêt", ["Technologie", "Sport", "Cinéma"])
            
            if st.form_submit_button("Soumettre le questionnaire"):
                add_points(25)
                st.success("Merci! 25 points ajoutés!")

    elif menu == "💰 Mon Portefeuille":
        # Tableau de bord financier
        st.header("Gestion des gains")
        st.write(f"Solde actuel: {st.session_state.user[4]} points")
        
        # Conversion en argent réel
        with st.expander("Convertir en argent"):
            convert_amount = st.number_input("Points à convertir", min_value=100)
            if st.button("Confirmer conversion"):
                if st.session_state.user[4] >= convert_amount:
                    new_balance = st.session_state.user[4] - convert_amount
                    c.execute('UPDATE users SET points = ? WHERE id = ?', 
                             (new_balance, st.session_state.user[0]))
                    conn.commit()
                    st.success(f"Conversion réussie! Montant envoyé: {convert_amount*0.01}€")

# --------------------- Système de points ---------------------
def add_points(amount):
    c.execute('UPDATE users SET points = points + ? WHERE id = ?',
             (amount, st.session_state.user[0]))
    conn.commit()
    st.session_state.user = list(st.session_state.user)
    st.session_state.user[4] += amount
    st.toast(f"+ {amount} points! 🎉", icon="✅")

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
