#!/usr/bin/env python3
"""
Gera o blog da ARVIA Capital a partir de ferramentas/posts/*.html.

Cada post começa com um comentário <!--{ ...json... }--> com:
  titulo, titulo_seo, descricao, data (AAAA-MM-DD), categoria, resumo, faq [[pergunta, resposta], ...]
seguido do corpo em HTML.

Uso:  python3 ferramentas/blog.py            (gera blog/ e atualiza sitemap.xml)
Para trocar o domínio, altere BASE abaixo e rode de novo.
"""
import json, re, html, pathlib, datetime

BASE = "https://luccaademiconpgua-source.github.io/landingpage/"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
POSTS = RAIZ / "ferramentas" / "posts"
LEGAL = "https://luccaademiconpgua-source.github.io/calculadora-de-patrimonio/"
MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()

def data_br(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month-1]} de {d.year}"

def ler_posts():
    posts = []
    for f in sorted(POSTS.glob("*.html")):
        txt = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--(\{.*?\})-->", txt, re.S)
        meta = json.loads(m.group(1))
        meta["slug"] = f.stem
        meta["corpo"] = txt[m.end():].strip().replace('<div class="tabela">', '<div class="tabela" tabindex="0" role="region" aria-label="Tabela comparativa">')
        palavras = len(re.sub(r"<[^>]+>", " ", meta["corpo"]).split())
        meta["leitura"] = max(1, round(palavras / 200))
        posts.append(meta)
    posts.sort(key=lambda p: p["data"], reverse=True)
    return posts

CSS = """
:root{--bordo:#4A0D18;--bordo-abs:#25070D;--bordo-mid:#6B1626;--ouro:#C6A04A;--ouro-hi:#E1C16A;--ouro-ink:#7A5A12;--off:#F5F1E8;--papel:#fff;--ink:#1A1214;--muted:#5E504B;--line:#E5DCCB;--creme:#FBF8F1;
--display:"Cormorant Garamond",Georgia,"Times New Roman",serif;--body:"Montserrat",system-ui,-apple-system,"Segoe UI",sans-serif;--gut:max(20px,env(safe-area-inset-left,0px));--gutr:max(20px,env(safe-area-inset-right,0px))}
*{box-sizing:border-box}html{background:var(--bordo-abs)}body{margin:0;background:var(--off);color:var(--ink);font:17px/1.75 var(--body)}
a{color:var(--bordo)}:focus-visible{outline:3px solid var(--ouro-hi);outline-offset:3px}
.wrap{max-width:1160px;margin:0 auto;padding-left:var(--gut);padding-right:var(--gutr)}
.topo{position:sticky;top:0;z-index:40;background:rgba(37,7,13,.95);border-bottom:1px solid rgba(198,160,74,.25);padding-top:env(safe-area-inset-top,0px)}
.topo .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px}
.marca{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--off)}
.losango{width:30px;height:30px;border:1px solid var(--ouro);display:grid;place-items:center;transform:rotate(45deg)}.losango span{transform:rotate(-45deg);font-family:var(--display);font-size:17px;color:var(--ouro-hi)}
.marca b{font-family:var(--display);font-size:21px;letter-spacing:.2em;display:block;line-height:1}.marca small{font-size:9px;letter-spacing:.34em;text-transform:uppercase;color:var(--ouro-hi)}
.menu{display:flex;gap:4px;align-items:center}.menu a{color:rgba(245,241,232,.86);text-decoration:none;font-size:13.5px;font-weight:500;padding:8px 12px}
.menu .btn{margin-left:6px}
.btn{display:inline-flex;align-items:center;justify-content:center;padding:12px 20px;border-radius:999px;font:600 14.5px/1 var(--body);text-decoration:none;background:linear-gradient(180deg,var(--ouro-hi),var(--ouro));color:var(--bordo-abs)!important}
@media (max-width:760px){.menu a:not(.btn){display:none}}
h1,h2,h3{font-family:var(--display);font-weight:600;line-height:1.12;text-wrap:balance;color:var(--bordo)}
.trilha{font-size:13px;color:var(--muted);padding-top:28px}.trilha a{color:var(--muted)}
.cab{max-width:760px;padding-block:14px 8px}
.cat{font-size:12px;letter-spacing:.22em;text-transform:uppercase;font-weight:600;color:var(--ouro-ink)}
.cab h1{font-size:clamp(34px,5vw,52px);margin:10px 0 14px}
.meta{font-size:13.5px;color:var(--muted);display:flex;gap:6px 14px;flex-wrap:wrap}
article.post{max-width:760px;padding-bottom:30px}
article.post .lead{font-size:19px;color:#3B2D2A}
article.post h2{font-size:clamp(26px,3.4vw,32px);margin:38px 0 8px}
article.post ul{padding-left:22px}article.post li{margin:6px 0}
.tabela{overflow-x:auto;margin:16px 0}.tabela:focus-visible{outline:3px solid var(--ouro-hi)}table{border-collapse:collapse;width:100%;min-width:520px;font-size:15px;background:var(--papel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
th,td{padding:11px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--creme);font-size:12.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.aviso{background:var(--creme);border:1px solid var(--line);border-left:4px solid var(--ouro);border-radius:10px;padding:12px 16px;font-size:14.5px;color:var(--muted);margin:16px 0}
.faq{margin-top:34px}.faq details{background:var(--papel);border:1px solid var(--line);border-radius:12px;padding:0 18px;margin-bottom:10px}
.faq summary{cursor:pointer;padding:14px 0;font-weight:600;color:var(--bordo)}.faq details p{margin:0 0 14px;color:var(--muted)}
.autor{max-width:760px;display:flex;gap:16px;align-items:center;background:var(--papel);border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:24px 0}
.autor .av{width:56px;height:56px;border-radius:50%;background:var(--bordo);display:grid;place-items:center;font-family:var(--display);font-size:24px;color:var(--ouro-hi);flex:none}
.autor p{margin:0;font-size:14.5px;color:var(--muted)}.autor b{color:var(--bordo);font-size:16px}
.cta{max-width:760px;background:var(--bordo-abs);color:var(--off);border-radius:18px;padding:28px;margin:10px 0 50px}
.cta h2{color:var(--off);font-size:30px;margin:0 0 8px}.cta p{color:rgba(245,241,232,.8);margin:0 0 18px}
.lista{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;padding-bottom:60px}
.card{background:var(--papel);border:1px solid var(--line);border-radius:16px;padding:22px;display:flex;flex-direction:column;gap:8px;text-decoration:none;color:inherit}
.card:hover{border-color:var(--ouro)}.card h2{font-size:25px;margin:0}.card p{margin:0;font-size:15px;color:var(--muted);flex:1}.card .mais{font-weight:600;color:var(--bordo);font-size:14px}
.rel{max-width:760px;margin-bottom:30px}.rel h2{font-size:26px}.rel ul{padding-left:20px}
footer{background:var(--bordo-abs);color:rgba(245,241,232,.78);font-size:12.5px;padding-block:30px calc(30px + env(safe-area-inset-bottom,0px))}
footer .wrap{display:grid;gap:12px}footer nav{display:flex;gap:6px 18px;flex-wrap:wrap}footer a{color:rgba(245,241,232,.9)}footer p{margin:0;max-width:110ch}
"""

def cabeca(titulo, descricao, url, extra_ld, tipo="article", fundo=""):
    return f"""<!DOCTYPE html>
<!-- © 2026 A&R Assessoria Estratégica Ltda. (ARVIA Capital). Todos os direitos reservados. Lei nº 9.609/1998 e Lei nº 9.610/1998. -->
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(descricao)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#25070D">
<link rel="icon" type="image/png" href="{fundo}icon.png">
<meta property="og:type" content="{tipo}"><meta property="og:title" content="{html.escape(titulo)}"><meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og.png"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="ARVIA Capital">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Montserrat:wght@400;500;600&display=swap">
<script type="application/ld+json">{json.dumps(extra_ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<header class="topo"><div class="wrap">
  <a class="marca" href="{BASE}" aria-label="ARVIA Capital, ir para o início"><span class="losango" aria-hidden="true"><span>A</span></span><span><b>ARVIA</b><small>Capital</small></span></a>
  <nav class="menu" aria-label="Navegação"><a href="{BASE}">Início</a><a href="{BASE}blog/">Blog</a><a href="{BASE}#simulador">Simulador</a><a class="btn" href="{BASE}#diagnostico">Diagnóstico gratuito</a></nav>
</div></header>
"""

RODAPE = f"""<footer><div class="wrap">
  <nav aria-label="Documentos legais"><a href="{LEGAL}privacidade.html">Política de Privacidade</a><a href="{LEGAL}termos.html">Termos de Uso</a><a href="{LEGAL}cookies.html">Política de Cookies</a><a href="{LEGAL}contato.html">Contato</a></nav>
  <p><strong>ARVIA Capital</strong> é a marca de A&amp;R Assessoria Estratégica Ltda. · CNPJ 63.972.524/0001-64 · Parceiro autorizado Ademicon · lucca.ribeiro@autorizadoademicon.com.br · WhatsApp (41) 98840-2942</p>
  <p>Conteúdo educativo. Simulações e exemplos são ilustrativos e não garantem contemplação, rentabilidade ou resultado. O consórcio é administrado pela Ademicon Administradora de Consórcios; as administradoras de consórcio são autorizadas e fiscalizadas pelo Banco Central do Brasil.</p>
  <p>© 2026 A&amp;R Assessoria Estratégica Ltda. (ARVIA Capital). Todos os direitos reservados. Proibida a cópia ou reprodução, total ou parcial, sem autorização.</p>
</div></footer>
</body></html>
"""

AUTOR_LD = {"@type": "Person", "@id": BASE + "#lucca", "name": "Lucca Antunes", "url": BASE + "#sobre",
            "jobTitle": "Consultor em arquitetura patrimonial com consórcio",
            "sameAs": ["https://www.instagram.com/luccaaribeiro/", "https://www.linkedin.com/in/lucca-antunes-ribeiro-79a055188"]}
EMPRESA_LD = {"@type": "Organization", "@id": BASE + "#empresa", "name": "ARVIA Capital", "logo": BASE + "icon.png", "url": BASE}

def pagina_post(p, posts):
    url = f"{BASE}blog/{p['slug']}/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": p["titulo"], "description": p["descricao"], "datePublished": p["data"], "dateModified": p.get("atualizado", p["data"]),
         "author": AUTOR_LD, "publisher": EMPRESA_LD, "mainEntityOfPage": url, "image": BASE + "og.png", "inLanguage": "pt-BR", "articleSection": p["categoria"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Início", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "blog/"},
            {"@type": "ListItem", "position": 3, "name": p["titulo"], "item": url}]}]}
    if p.get("faq"):
        ld["@graph"].append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
    faq = ""
    if p.get("faq"):
        faq = '<section class="faq" aria-labelledby="t-faq"><h2 id="t-faq">Perguntas frequentes</h2>' + "".join(
            f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in p["faq"]) + "</section>"
    outros = [o for o in posts if o["slug"] != p["slug"]][:3]
    rel = ""
    if outros:
        rel = '<section class="rel" aria-labelledby="t-rel"><h2 id="t-rel">Continue lendo</h2><ul>' + "".join(
            f'<li><a href="../{o["slug"]}/">{html.escape(o["titulo"])}</a></li>' for o in outros) + "</ul></section>"
    return cabeca(p["titulo_seo"], p["descricao"], url, ld, "article", "../../") + f"""
<main class="wrap" id="conteudo">
  <nav class="trilha" aria-label="Você está em"><a href="{BASE}">Início</a> › <a href="../">Blog</a> › {html.escape(p['categoria'])}</nav>
  <header class="cab">
    <div class="cat">{html.escape(p['categoria'])}</div>
    <h1>{html.escape(p['titulo'])}</h1>
    <div class="meta"><span>Por Lucca Antunes</span><span>{data_br(p['data'])}</span><span>{p['leitura']} min de leitura</span></div>
  </header>
  <article class="post">
    {p['corpo']}
    {faq}
  </article>
  <aside class="autor" aria-label="Sobre o autor"><div class="av" aria-hidden="true">L</div><div><b>Lucca Antunes</b><p>Consultor da ARVIA Capital, parceiro autorizado Ademicon. Planeja a compra de imóveis, veículos e a expansão de negócios usando o consórcio como estratégia, com acompanhamento em cada assembleia.</p></div></aside>
  <section class="cta" aria-labelledby="t-cta"><h2 id="t-cta">Quer saber qual estratégia faz sentido para você?</h2><p>Responda o diagnóstico gratuito em menos de 2 minutos. Eu chego na primeira conversa com um plano pensado para o seu objetivo.</p><a class="btn" href="{BASE}#diagnostico">Fazer meu diagnóstico</a></section>
  {rel}
</main>
""" + RODAPE

def pagina_lista(posts):
    url = BASE + "blog/"
    ld = {"@context": "https://schema.org", "@type": "Blog", "name": "Blog ARVIA Capital", "url": url, "inLanguage": "pt-BR", "publisher": EMPRESA_LD,
          "blogPost": [{"@type": "BlogPosting", "headline": p["titulo"], "url": f"{url}{p['slug']}/", "datePublished": p["data"]} for p in posts]}
    cards = "".join(f"""<a class="card" href="{p['slug']}/"><div class="cat">{html.escape(p['categoria'])}</div><h2>{html.escape(p['titulo'])}</h2><p>{html.escape(p['resumo'])}</p><span class="mais">Ler matéria · {p['leitura']} min</span></a>""" for p in posts)
    return cabeca("Blog ARVIA Capital · Consórcio, patrimônio e estratégia", "Matérias sobre consórcio, lance, contemplação e planejamento patrimonial, escritas por Lucca Antunes, consultor da ARVIA Capital.", url, ld, "website", "../") + f"""
<main class="wrap" id="conteudo">
  <header class="cab" style="padding-top:40px"><div class="cat">Blog</div><h1>Consórcio, patrimônio e estratégia</h1><p style="color:var(--muted);margin:0 0 26px;max-width:62ch">Conteúdo direto ao ponto para você decidir melhor: como funciona, quanto custa, como usar o lance e o que fazer depois da contemplação.</p></header>
  <div class="lista">{cards}</div>
</main>
""" + RODAPE

def sitemap(posts):
    hoje = max([p.get("atualizado", p["data"]) for p in posts] + ["2026-10-23"])
    urls = [(BASE, hoje, "1.0"), (BASE + "blog/", hoje, "0.8")] + [(f"{BASE}blog/{p['slug']}/", p.get("atualizado", p["data"]), "0.7") for p in posts]
    corpo = "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{corpo}</urlset>\n'

def main():
    posts = ler_posts()
    (RAIZ / "blog").mkdir(exist_ok=True)
    (RAIZ / "blog" / "index.html").write_text(pagina_lista(posts), encoding="utf-8")
    for p in posts:
        d = RAIZ / "blog" / p["slug"]; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(pagina_post(p, posts), encoding="utf-8")
    (RAIZ / "sitemap.xml").write_text(sitemap(posts), encoding="utf-8")
    print(f"{len(posts)} matéria(s) geradas.")

if __name__ == "__main__":
    main()
