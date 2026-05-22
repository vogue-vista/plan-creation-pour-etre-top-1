import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="MetaTag SEO", page_icon="🔍", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span { font-family: 'Poppins', sans-serif !important; }
</style>
""", unsafe_allow_html=True)

PAYPAL_CLIENT_ID = "DEMO"  
PAYPAL_PLAN_ID = "DEMO"    

if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

st.title("🔍 MetaTag SEO")
st.subheader("Générez des balises Meta Title et Meta Description optimisées pour Google en 2 secondes.")

# CAS 1 : NON PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres Premium.")
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Dominez Google pour 20 $/mois")
        st.write("Ne devinez plus ce que l'algorithme Google veut voir. Générez des titres accrocheurs et des descriptions qui respectent scrupuleusement la longueur maximale de caractères.")
        components.html("""
        <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
            <div style="background-color: #ffc439; color: #003087; text-align: center; padding: 12px; font-family: Arial; font-weight: bold; border-radius: 4px; max-width: 300px; cursor: pointer;">
                🟨 S'abonner avec PayPal (Démo)
            </div>
        </a>
        """, height=150)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "seo20":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# CAS 2 : PAYÉ
else:
    st.write("✨ **Espace SEO Actif.** Indexez vos pages.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_inputs, col_options = st.columns(2)
        
        with col_inputs:
            sujet_page = st.text_input("Sujet ou titre de la page web :", placeholder="Ex: Guide complet pour apprendre la guitare en 30 jours")
            mots_cles = st.text_input("Mots-clés principaux à include (séparés par des virgules) :", placeholder="Ex: cours guitare, débutant, apprendre guitare")
            
        with col_options:
            type_page = st.selectbox("Type de page", ["Article de Blog", "Fiche Produit E-commerce", "Page d'accueil (Homepage)", "Page de Service"])
            intention = st.selectbox("Intention de recherche", ["Informative (Apprendre)", "Commerciale (Acheter / Comparer)", "Locale (Trouver un commerce)"])

        generer = st.button("🚀 Générer mes Balises SEO", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Clé GROQ_API_KEY manquante.")
        elif not sujet_page:
            st.error("⚠️ Entrez le sujet de votre page.")
        else:
            with st.spinner("Groq calcule la taille et rédige les balises..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un consultant SEO d'élite. Ton but est de fournir 3 propositions de balises Meta Title et Meta Description.
                    Règles ultra-strictes :
                    - Meta Title doit faire MOINS de 60 caractères.
                    - Meta Description doit faire MOINS de 160 caractères.
                    Inclus obligatoirement les mots-clés de l'utilisateur de manière naturelle. Indique le compteur de caractères pour chaque proposition pour prouver que les règles sont respectées.
                    Ne fais aucune intro ou conclusion amicale."""

                    prompt_utilisateur = f"Sujet: {sujet_page}\nMots-clés: {mots_cles}\nType: {type_page}\nIntention: {intention}"

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": prompt_utilisateur}
                        ],
                        temperature=0.5
                    )
                    
                    # LE CORRECTIF DU CROCHET EST BIEN APPLIQUÉ ICI :
                    seo_final = reponse.choices[0].message.content
                    st.success("✨ Vos balises SEO conformes sont prêtes !")
                    st.markdown(seo_final)
                    
                    st.text_area("Copier les balises :", value=seo_final, height=250)
                    
                    st.write("---")
                    st.info("""
                    ### 💡 Comment appliquer ces balises sur votre site ?
                    
                    Ces textes ne s'ajoutent pas automatiquement sur Google. Vous devez les intégrer vous-même sur votre plateforme :
                    
                    1. **Copiez** le titre et la description qui vous conviennent le mieux ci-dessus.
                    2. **Ouvrez les réglages de votre page web** sur votre outil habituel (WordPress, Shopify, Webflow, Wix...).
                    3. **Collez-les** dans les cases nommées **Meta Title** (ou Titre SEO) et **Meta Description** (ou Description SEO).
                    4. **Enregistrez la page.**
                    
                    *Note : Les robots de Google mettront entre quelques jours et deux semaines à visiter votre site pour enregistrer ces modifications et mettre à jour vos résultats de recherche.*
                    """)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
