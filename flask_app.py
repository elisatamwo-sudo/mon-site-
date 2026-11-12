from flask import Flask, render_template_string, request
from markupsafe import escape

app = Flask(__name__)

# Modèle commun à toutes les pages (menu + mise en forme)
BASE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ titre }} - Mon site</title>
<style>
  body { font-family: "Segoe UI", Arial, sans-serif; background: #eef2ff; color: #374151; margin: 0; padding: 40px 16px; }
  .carte { max-width: 860px; margin: 0 auto; background: #ffffff; border-radius: 24px; padding: 32px 56px 56px; box-shadow: 0 10px 40px rgba(30, 58, 138, 0.12); }
  nav { border-bottom: 1px solid #e5e7eb; padding-bottom: 20px; margin-bottom: 32px; }
  nav a { color: #374151; text-decoration: none; font-weight: 600; margin-right: 28px; }
  nav a:hover { color: #4f46e5; }
  h1 { color: #1e3a8a; font-size: 2.8rem; }
  a { color: #4f46e5; }
  input, button { font-size: 1rem; padding: 8px 12px; }
  .heure { font-size: 3rem; font-weight: bold; color: #1e3a8a; }
</style>
</head>
<body>
<div class="carte">
  <nav>
    <a href="/">Accueil</a>
    <a href="/presentation">Présentation</a>
    <a href="/formulaire">Formulaire</a>
    <a href="/horloge">Horloge</a>
    <a href="/qui-suis-je">Qui suis-je ?</a>
  </nav>
  {{ contenu|safe }}
</div>
</body>
</html>"""


def page(titre, contenu):
    return render_template_string(BASE, titre=titre, contenu=contenu)


@app.get("/")
def accueil():
    return page("Accueil", """
        <h1>Bienvenue sur mon site !</h1>
        <p>Ce site me sert à découvrir le fonctionnement du Web.</p>
        <p>Un lien vers un autre site :
           <a href="https://fr.wikipedia.org/wiki/Histoire_du_Web">l'histoire du Web</a>.</p>
    """)


@app.get("/presentation")
def presentation():
    return page("Présentation", """
        <h1>Présentation</h1>
        <p>Je m'appelle (ton prénom) et je suis étudiante en informatique.</p>
        <p>Mes centres d'intérêt :</p>
        <ul>
          <li>La programmation</li>
          <li>Les réseaux</li>
          <li>(ajoute ce que tu veux)</li>
        </ul>
    """)


@app.route("/formulaire", methods=["GET", "POST"])
def formulaire():
    message = ""
    if request.method == "POST":
        nom = request.form.get("nom", "")
        message = f"<p><strong>Bonjour {escape(nom)} !</strong> Ton formulaire a bien été reçu.</p>"
    return page("Formulaire", f"""
        <h1>Formulaire</h1>
        <form method="post">
          <label>Ton prénom : <input type="text" name="nom"></label>
          <button type="submit">Envoyer</button>
        </form>
        {message}
    """)


@app.get("/horloge")
def horloge():
    return page("Horloge", """
        <h1>Horloge</h1>
        <p>L'heure de ton ordinateur, mise à jour chaque seconde :</p>
        <div class="heure" id="heure"></div>
        <script>
          function afficher() {
            document.getElementById("heure").textContent =
              new Date().toLocaleTimeString("fr-FR");
          }
          afficher();
          setInterval(afficher, 1000);
        </script>
    """)


@app.get("/qui-suis-je")
def qui_suis_je():
    adresse = request.headers.get("X-Forwarded-For", request.remote_addr)
    navigateur = request.headers.get("User-Agent", "inconnu")
    return page("Qui suis-je ?", f"""
        <h1>Qui suis-je ?</h1>
        <p>Voici ce que le serveur sait de toi :</p>
        <ul>
          <li>Ton adresse IP : <strong>{escape(adresse)}</strong></li>
          <li>Ton navigateur : <strong>{escape(navigateur)}</strong></li>
        </ul>
    """)


# ---------------------------------------------------------------
#  Ne pas modifier : utile seulement pour lancer le site
#  sur votre propre ordinateur (python flask_app.py)
# ---------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
