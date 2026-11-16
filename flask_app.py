from flask import Flask, render_template_string, request

app = Flask(__name__)

# Structure commune : menu latéral + zone de contenu
BASE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ titre }} · Mon espace</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: "Segoe UI", Arial, sans-serif; background: #fff7ed; color: #1f2937; display: flex; min-height: 100vh; }
  aside { width: 240px; background: #1e293b; color: #f8fafc; padding: 32px 20px; position: fixed; top: 0; bottom: 0; }
  aside .logo { font-size: 1.3rem; font-weight: 700; margin-bottom: 32px; }
  aside .logo span { color: #fb7185; }
  aside a { display: block; color: #cbd5e1; text-decoration: none; padding: 12px 14px; border-radius: 10px; margin-bottom: 6px; }
  aside a:hover { background: #334155; color: #ffffff; }
  aside a.actif { background: #fb7185; color: #ffffff; font-weight: 600; }
  main { margin-left: 240px; padding: 48px 56px; width: 100%; max-width: 1000px; }
  h1 { font-size: 2.4rem; margin: 0 0 12px; color: #1e293b; }
  h1 span { color: #fb7185; }
  p.intro { font-size: 1.15rem; color: #475569; max-width: 560px; }
  .cartes { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 20px; margin-top: 32px; }
  .carte { background: #ffffff; border-radius: 16px; padding: 24px; box-shadow: 0 4px 14px rgba(0,0,0,0.07); border-top: 5px solid #fb7185; }
  .carte h3 { margin: 0 0 8px; }
  .carte p { margin: 0; color: #64748b; }
  .bloc { background: #ffffff; border-radius: 16px; padding: 28px; box-shadow: 0 4px 14px rgba(0,0,0,0.07); margin-top: 24px; }
  label { display: block; font-weight: 600; margin-bottom: 6px; }
  input, textarea { width: 100%; padding: 12px; border: 2px solid #e2e8f0; border-radius: 10px; font-size: 1rem; margin-bottom: 16px; font-family: inherit; }
  input:focus, textarea:focus { outline: none; border-color: #fb7185; }
  button { background: #fb7185; color: #ffffff; border: none; padding: 12px 24px; border-radius: 10px; font-size: 1rem; font-weight: 600; cursor: pointer; }
  button:hover { background: #e11d48; }
  .merci { background: #dcfce7; color: #166534; padding: 14px 18px; border-radius: 10px; margin-top: 20px; }
  .heure { font-size: 4.5rem; font-weight: 800; color: #fb7185; letter-spacing: 2px; }
  .date { font-size: 1.2rem; color: #64748b; text-transform: capitalize; }
  ul.infos { list-style: none; padding: 0; margin: 0; }
  ul.infos li { padding: 14px 0; border-bottom: 1px solid #f1f5f9; word-break: break-word; }
  ul.infos li:last-child { border-bottom: none; }
  ul.infos strong { display: block; color: #64748b; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
  @media (max-width: 760px) {
    body { display: block; }
    aside { position: static; width: 100%; padding: 16px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
    aside .logo { width: 100%; margin-bottom: 8px; }
    aside a { margin: 0; padding: 8px 12px; }
    main { margin-left: 0; padding: 28px 20px; }
    .heure { font-size: 3rem; }
  }
</style>
</head>
<body>
<aside>
  <div class="logo">Mon <span>espace</span></div>
  <a href="/" class="{{ 'actif' if actif == 'accueil' }}">🏠 Accueil</a>
  <a href="/a-propos" class="{{ 'actif' if actif == 'apropos' }}">👤 À propos</a>
  <a href="/contact" class="{{ 'actif' if actif == 'contact' }}">✉️ Contact</a>
  <a href="/heure" class="{{ 'actif' if actif == 'heure' }}">⏰ Heure</a>
  <a href="/mon-navigateur" class="{{ 'actif' if actif == 'navigateur' }}">🔍 Mon navigateur</a>
</aside>
<main>
{{ contenu|safe }}
</main>
</body>
</html>"""


def page(titre, actif, contenu, **variables):
    # On fabrique d'abord le contenu, puis on le place dans la structure commune
    html = render_template_string(contenu, **variables)
    return render_template_string(BASE, titre=titre, actif=actif, contenu=html)


@app.get("/")
def accueil():
    return page("Accueil", "accueil", """
        <h1>Salut, bienvenue sur <span>mon site</span> 👋</h1>
        <p class="intro">Je découvre comment fonctionne le Web : un serveur, un navigateur,
        et du code qui fait le lien entre les deux.</p>
        <div class="cartes">
          <div class="carte"><h3>🌍 Le Web</h3><p>Une adresse, une page.</p></div>
          <div class="carte"><h3>🐍 Flask</h3><p>Du Python qui fabrique les pages.</p></div>
          <div class="carte"><h3>🚀 Déploiement</h3><p>GitHub envoie tout seul mon code en ligne.</p></div>
        </div>
    """)


@app.get("/a-propos")
def a_propos():
    return page("À propos", "apropos", """
        <h1>À <span>propos</span></h1>
        <div class="bloc">
          <p>Je m'appelle <strong>Ange</strong> et je suis étudiante en informatique.</p>
          <p>Ce que j'aime :</p>
          <ul>
            <li>Programmer</li>
            <li>Apprendre de nouvelles choses</li>
            <li>(ajoute ce que tu veux)</li>
          </ul>
        </div>
    """)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    prenom = None
    if request.method == "POST":
        prenom = request.form.get("prenom", "").strip()
    return page("Contact", "contact", """
        <h1>Me <span>contacter</span></h1>
        <div class="bloc">
          <form method="post">
            <label for="prenom">Ton prénom</label>
            <input type="text" id="prenom" name="prenom" required>
            <label for="message">Ton message</label>
            <textarea id="message" name="message" rows="4"></textarea>
            <button type="submit">Envoyer</button>
          </form>
          {% if prenom %}
            <div class="merci">Merci {{ prenom }} ! Ton message a bien été reçu. ✅</div>
          {% endif %}
        </div>
    """, prenom=prenom)


@app.get("/heure")
def heure():
    return page("Heure", "heure", """
        <h1>Quelle <span>heure</span> est-il ?</h1>
        <div class="bloc">
          <div class="heure" id="heure">--:--:--</div>
          <div class="date" id="date"></div>
          <p>Cette heure vient de ton navigateur, pas du serveur : elle se met à jour chaque seconde grâce à du JavaScript.</p>
        </div>
        <script>
          function maj() {
            var d = new Date();
            document.getElementById("heure").textContent = d.toLocaleTimeString("fr-FR");
            document.getElementById("date").textContent =
              d.toLocaleDateString("fr-FR", { weekday: "long", day: "numeric", month: "long", year: "numeric" });
          }
          maj();
          setInterval(maj, 1000);
        </script>
    """)


@app.get("/mon-navigateur")
def mon_navigateur():
    adresse = request.headers.get("X-Forwarded-For", request.remote_addr)
    navigateur = request.headers.get("User-Agent", "inconnu")
    langue = request.headers.get("Accept-Language", "inconnue")
    return page("Mon navigateur", "navigateur", """
        <h1>Ce que le serveur <span>sait de toi</span></h1>
        <div class="bloc">
          <ul class="infos">
            <li><strong>Adresse IP</strong>{{ adresse }}</li>
            <li><strong>Navigateur</strong>{{ navigateur }}</li>
            <li><strong>Langues acceptées</strong>{{ langue }}</li>
          </ul>
        </div>
    """, adresse=adresse, navigateur=navigateur, langue=langue)


# ---------------------------------------------------------------
#  Ne pas modifier : utile seulement pour lancer le site
#  sur votre propre ordinateur (python flask_app.py)
# ---------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
