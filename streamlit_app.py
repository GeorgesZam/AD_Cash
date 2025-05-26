import streamlit as st
import random

# --- Header ---
st.title("MoneyPlay: Gagnez de l'argent en vous amusant 💰🎮")

# --- Initialize session state ---
if 'balance' not in st.session_state:
    st.session_state.balance = 0.0
if 'size' not in st.session_state:
    st.session_state.size = 1
if 'food_positions' not in st.session_state or not st.session_state.food_positions:
    # Generate 10 random food positions in a 5x5 grid
    cells = [(i, j) for i in range(5) for j in range(5)]
    st.session_state.food_positions = set(random.sample(cells, 10))

# --- Tabs Navigation ---
tabs = st.tabs(["Accueil", "Jeux", "Vidéos/Séries", "Formulaire & Affiliation"])

# --- Page: Accueil ---
with tabs[0]:
    st.markdown(
        """
        **MoneyPlay** est votre hub pour gagner de l'argent en vous divertissant !

        **Que voulez-vous faire aujourd'hui ?**
        
        - 🎮 Jouer à des mini-jeux fun (chaque nourriture rapporte 1€, taille augmente)
        - 📺 Regarder des vidéos ou séries sponsorisées (5-20 points)
        - 📝 Remplir un formulaire et découvrir nos offres d'affiliation
        """
    )

# --- Page: Jeux ---
with tabs[1]:
    st.subheader("Jeu : Mange les aliments 🍎")
    st.markdown(f"**Solde** : €{st.session_state.balance:.2f}  &nbsp;&nbsp; **Taille** : {st.session_state.size}")
    st.markdown("Clique sur les aliments pour les manger et gagner de l'argent !\nNouvelle grille quand tout est mangé.")

    # Display grid
    for i in range(5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if (i, j) in st.session_state.food_positions:
                if col.button("🍎", key=f"btn_{i}_{j}"):
                    # Eat food
                    st.session_state.food_positions.remove((i, j))
                    st.session_state.balance += 1.0
                    st.session_state.size += 1
                    st.experimental_rerun()
            else:
                col.write(" ")

    # Respawn when empty
    if not st.session_state.food_positions:
        st.success("Grille terminée ! Nouveaux aliments arrivent...")
        cells = [(i, j) for i in range(5) for j in range(5)]
        st.session_state.food_positions = set(random.sample(cells, 10))

# --- Page: Vidéos/Séries ---
with tabs[2]:
    st.subheader("Vidéos & Séries Sponsorisé(e)s 🎬")
    st.markdown("Regardez ces vidéos et gagnez des points:")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    if st.button("J'ai regardé la vidéo ! (5 points) 👀"):
        st.info("Votre visionnage a été enregistré.")

    st.markdown("---")
    st.markdown("**Séries recommandées**")
    st.markdown("[Regarder la série sur Vimeo](https://vimeo.com/76979871)")
    if st.button("J'ai visionné la série ! (20 points) 🎉"):
        st.success("Vous avez gagné des points !")

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
st.markdown(f"© 2025 MoneyPlay. Tous droits réservés.")
