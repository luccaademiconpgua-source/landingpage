#!/usr/bin/env python3
"""
Gera o site da ARVIA Capital: topo e rodapé iguais em todas as páginas,
blog, simulador, contato, páginas legais, sitemap e a seção "Do blog" da página inicial.

Uso:  python3 ferramentas/gerar_site.py      (ou python3 ferramentas/blog.py, que faz o mesmo)

Onde fica cada coisa:
  ferramentas/posts/*.html     matérias do blog (comentário <!--{json}--> + corpo em HTML)
  ferramentas/paginas/*.html   privacidade, termos, cookies e contato (comentário <!--{json}--> + corpo)
  index.html                   página inicial; o topo, o rodapé e a seção do blog são trocados
                               entre os marcadores <!--site:...--> e <!--/site:...--> a cada geração
  assets/site.css, site.js     visual e comportamento comuns

Para trocar o domínio, altere BASE abaixo e rode de novo. Os links internos são relativos.
"""
import json, re, html, pathlib, datetime

BASE = "https://luccaademiconpgua-source.github.io/landingpage/"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
POSTS = RAIZ / "ferramentas" / "posts"
PAGINAS = RAIZ / "ferramentas" / "paginas"
MESES = "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split()
WHATS = "https://wa.me/5541988402942?text=Ol%C3%A1%20Lucca%2C%20vim%20pelo%20site%20da%20ARVIA%20Capital."
INSTA = "https://www.instagram.com/luccaaribeiro/"
LINKEDIN = "https://www.linkedin.com/in/lucca-antunes-ribeiro-79a055188"
VERSAO = datetime.date.today().strftime("%Y%m%d")
ESC = html.escape


def data_br(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} de {MESES[d.month-1]} de {d.year}"


def ler_fonte(f):
    txt = f.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(\{.*?\})-->", txt, re.S)
    meta = json.loads(m.group(1))
    meta["slug"] = f.stem
    meta["corpo"] = txt[m.end():].strip()
    return meta


def ler_posts():
    posts = []
    for f in sorted(POSTS.glob("*.html")):
        p = ler_fonte(f)
        p["corpo"] = p["corpo"].replace('<div class="tabela">', '<div class="tabela" tabindex="0" role="region" aria-label="Tabela comparativa">')
        palavras = len(re.sub(r"<[^>]+>", " ", p["corpo"]).split())
        p["leitura"] = max(1, round(palavras / 200))
        posts.append(p)
    posts.sort(key=lambda p: p["data"], reverse=True)
    return posts


# ---------- peças comuns ----------

def topo(P, atual, home=False):
    inicio = "#inicio" if home else (P or "./")
    sim = "#simulador" if home else P + "simulador/"
    itens = [("metodo", "Método", P + "#metodo" if not home else "#metodo"),
             ("solucoes", "Soluções", P + "#solucoes" if not home else "#solucoes"),
             ("simulador", "Simulador", sim),
             ("blog", "Blog", P + "blog/"),
             ("sobre", "Sobre", P + "#sobre" if not home else "#sobre"),
             ("contato", "Contato", P + "contato/")]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if k == atual else ""}>{t}</a>' for k, t, h in itens)
    diag = "#diagnostico" if home else P + "#diagnostico"
    return f"""<header class="topo">
  <div class="wrap">
    <a class="marca" href="{inicio}" aria-label="ARVIA Capital, ir para o início"><span class="losango" aria-hidden="true"><span>A</span></span><span><b>ARVIA</b><small>Capital</small></span></a>
    <button class="abre-menu" type="button" aria-expanded="false" aria-controls="menu-site"><i aria-hidden="true"></i>Menu</button>
    <nav class="menu" id="menu-site" aria-label="Menu principal">{links}<a class="btn btn-ouro" href="{diag}">Diagnóstico gratuito</a></nav>
  </div>
</header>"""


ZAP_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.47-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.69.63.71.23 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.8h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88a9.83 9.83 0 0 1 9.88 9.89c0 5.45-4.44 9.88-9.88 9.88zm8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89 0-3.18-1.24-6.16-3.48-8.41z"/></svg>'


def rodape(P, home=False):
    a = lambda ancora: ("#" if home else P + "#") + ancora
    return f"""<footer class="rodape">
  <div class="wrap">
    <div class="rod-grade">
      <div>
        <a class="marca" href="{'#inicio' if home else (P or './')}" aria-label="ARVIA Capital, ir para o início"><span class="losango" aria-hidden="true"><span>A</span></span><span><b>ARVIA</b><small>Capital</small></span></a>
        <p class="sobre-curto">Consultoria patrimonial com consórcio: diagnóstico, estratégia de lance e acompanhamento em cada assembleia. Atendimento online para todo o Brasil e para brasileiros no exterior.</p>
      </div>
      <nav aria-label="Site"><h2>Site</h2><ul>
        <li><a href="{'#inicio' if home else (P or './')}">Início</a></li>
        <li><a href="{a('metodo')}">Método</a></li>
        <li><a href="{a('solucoes')}">Soluções</a></li>
        <li><a href="{'#simulador' if home else P + 'simulador/'}">Simulador</a></li>
        <li><a href="{P}blog/">Blog</a></li>
        <li><a href="{a('sobre')}">Sobre</a></li>
        <li><a href="{a('diagnostico')}">Diagnóstico gratuito</a></li>
      </ul></nav>
      <nav aria-label="Atendimento"><h2>Atendimento</h2><ul>
        <li><a href="{WHATS}" target="_blank" rel="noopener">WhatsApp (41) 98840-2942</a></li>
        <li><a href="mailto:lucca.ribeiro@autorizadoademicon.com.br">E-mail</a></li>
        <li><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></li>
        <li><a href="{P}contato/">Página de contato</a></li>
      </ul></nav>
      <nav aria-label="Documentos legais"><h2>Legal</h2><ul>
        <li><a href="{P}privacidade/">Política de Privacidade</a></li>
        <li><a href="{P}termos/">Termos de Uso</a></li>
        <li><a href="{P}cookies/">Política de Cookies</a></li>
      </ul></nav>
    </div>
    <div class="rod-legal">
      <p><strong>ARVIA Capital</strong> é a marca de A&amp;R Assessoria Estratégica Ltda. · CNPJ 63.972.524/0001-64 · Rua Antônio Morais Pereira da Costa, 44, Correia Velho, Paranaguá/PR, CEP 83206-400 · Parceiro autorizado Ademicon</p>
      <p>O consórcio é administrado pela Ademicon Administradora de Consórcios. As administradoras de consórcio são autorizadas e fiscalizadas pelo Banco Central do Brasil. Conteúdo educativo: simulações e exemplos são ilustrativos e não garantem contemplação, rentabilidade ou resultado.</p>
      <p>© 2026 A&amp;R Assessoria Estratégica Ltda. (ARVIA Capital). Todos os direitos reservados. Proibida a cópia ou reprodução, total ou parcial, sem autorização.</p>
    </div>
  </div>
  <a class="zap" href="{WHATS}" target="_blank" rel="noopener" aria-label="Falar com o Lucca no WhatsApp">{ZAP_SVG}</a>
</footer>"""


def cabeca(titulo, descricao, url, ld, P, tipo="website", robots="index, follow, max-image-preview:large"):
    return f"""<!DOCTYPE html>
<!-- © 2026 A&R Assessoria Estratégica Ltda. (ARVIA Capital). Todos os direitos reservados. Lei nº 9.609/1998 e Lei nº 9.610/1998. -->
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{ESC(titulo)}</title>
<meta name="description" content="{ESC(descricao)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#25070D">
<link rel="icon" type="image/png" href="{P}icon.png"><link rel="apple-touch-icon" href="{P}icon.png">
<meta property="og:type" content="{tipo}"><meta property="og:title" content="{ESC(titulo)}"><meta property="og:description" content="{ESC(descricao)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og.png"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="ARVIA Capital">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">
<link rel="stylesheet" href="{P}assets/site.css?v={VERSAO}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
"""


def fim(P):
    return f'\n<script src="{P}assets/site.js?v={VERSAO}" defer></script>\n</body>\n</html>\n'


def pagina(titulo, descricao, caminho, ld, atual, conteudo, tipo="website", robots="index, follow, max-image-preview:large", P=None):
    if P is None:
        P = "../" * caminho.count("/")
    return cabeca(titulo, descricao, BASE + caminho, ld, P, tipo, robots) + topo(P, atual) + "\n" + conteudo + "\n" + rodape(P) + fim(P)


def migalhas(*itens):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + c} for i, (n, c) in enumerate(itens)]}


def faixa(P, trilha, eyebrow, h1, texto="", extra=""):
    tr = " › ".join([f'<a href="{P or "./"}">Início</a>'] + trilha)
    return f"""<section class="faixa" aria-labelledby="t-pagina"><div class="wrap">
  <nav class="trilha" aria-label="Você está em">{tr}</nav>
  <div class="eyebrow">{eyebrow}</div>
  <h1 id="t-pagina">{h1}</h1>
  {f'<p>{texto}</p>' if texto else ''}{extra}
</div></section>"""


AUTOR_LD = {"@type": "Person", "@id": BASE + "#lucca", "name": "Lucca Antunes", "url": BASE + "#sobre",
            "jobTitle": "Consultor em arquitetura patrimonial com consórcio", "sameAs": [INSTA, LINKEDIN]}
EMPRESA_LD = {"@type": "Organization", "@id": BASE + "#empresa", "name": "ARVIA Capital", "logo": BASE + "icon.png", "url": BASE}


def cartoes(posts, P, nivel="h2"):
    return "".join(f"""<a class="card" href="{P}blog/{p['slug']}/"><span class="cat">{ESC(p['categoria'])}</span><{nivel}>{ESC(p['titulo'])}</{nivel}><p>{ESC(p['resumo'])}</p><span class="mais">Ler matéria · {p['leitura']} min</span></a>""" for p in posts)


# ---------- páginas ----------

def pagina_post(p, posts):
    caminho = f"blog/{p['slug']}/"
    url = BASE + caminho
    P = "../../"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": p["titulo"], "description": p["descricao"], "datePublished": p["data"], "dateModified": p.get("atualizado", p["data"]),
         "author": AUTOR_LD, "publisher": EMPRESA_LD, "mainEntityOfPage": url, "image": BASE + "og.png", "inLanguage": "pt-BR", "articleSection": p["categoria"]},
        migalhas(("Início", ""), ("Blog", "blog/"), (p["titulo"], caminho))]}
    faq = ""
    if p.get("faq"):
        ld["@graph"].append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
        faq = '<section class="faq-post" aria-labelledby="t-faq"><h2 id="t-faq">Perguntas frequentes</h2>' + "".join(
            f"<details><summary>{ESC(q)}</summary><p>{ESC(a)}</p></details>" for q, a in p["faq"]) + "</section>"
    outros = [o for o in posts if o["slug"] != p["slug"]][:3]
    rel = f'<section class="rel" aria-labelledby="t-rel"><h2 id="t-rel">Continue lendo</h2><div class="lista">{cartoes(outros, P, "h3")}</div></section>' if outros else ""
    meta = f'<div class="post-meta"><span>Por Lucca Antunes</span><span>{data_br(p["data"])}</span><span>{p["leitura"]} min de leitura</span></div>'
    conteudo = f"""<main id="conteudo">
{faixa(P, [f'<a href="../">Blog</a>', ESC(p['categoria'])], ESC(p['categoria']), ESC(p['titulo']), extra=meta)}
<div class="wrap miolo">
  <div class="lado">
    <div>
      <article class="post">
        {p['corpo']}
        {faq}
      </article>
      <aside class="autor" aria-label="Sobre o autor"><div class="av" aria-hidden="true">L</div><div><b>Lucca Antunes</b><p>Consultor da ARVIA Capital, parceiro autorizado Ademicon. Planeja a compra de imóveis, veículos e a expansão de negócios usando o consórcio como estratégia, com acompanhamento em cada assembleia.</p></div></aside>
    </div>
    <aside class="cartao-lado" aria-labelledby="t-cta"><h2 id="t-cta">Qual estratégia faz sentido para você?</h2><p>Responda o diagnóstico gratuito em menos de 2 minutos. Eu chego na primeira conversa com um plano pensado para o seu objetivo.</p><a class="btn btn-ouro" href="{P}#diagnostico">Fazer meu diagnóstico</a></aside>
  </div>
  {rel}
</div>
</main>"""
    return pagina(p["titulo_seo"], p["descricao"], caminho, ld, "blog", conteudo, "article", P=P)


def pagina_lista(posts):
    P = "../"
    url = BASE + "blog/"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "name": "Blog ARVIA Capital", "url": url, "inLanguage": "pt-BR", "publisher": EMPRESA_LD,
         "blogPost": [{"@type": "BlogPosting", "headline": p["titulo"], "url": f"{url}{p['slug']}/", "datePublished": p["data"]} for p in posts]},
        migalhas(("Início", ""), ("Blog", "blog/"))]}
    conteudo = f"""<main id="conteudo">
{faixa(P, ['Blog'], 'Blog', 'Consórcio, patrimônio e estratégia', 'Conteúdo direto ao ponto para você decidir melhor: como funciona, quanto custa, como usar o lance e o que fazer depois da contemplação.')}
<div class="wrap miolo"><div class="lista">{cartoes(posts, P)}</div></div>
</main>"""
    return pagina("Blog ARVIA Capital · Consórcio, patrimônio e estratégia",
                  "Matérias sobre consórcio, lance, contemplação e planejamento patrimonial, escritas por Lucca Antunes, consultor da ARVIA Capital.",
                  "blog/", ld, "blog", conteudo)


def pagina_simulador():
    P = "../"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": "Calculadora Patrimonial ARVIA", "url": BASE + "simulador/", "applicationCategory": "FinanceApplication",
         "operatingSystem": "Navegador", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL"}, "provider": EMPRESA_LD, "inLanguage": "pt-BR"},
        migalhas(("Início", ""), ("Simulador", "simulador/"))]}
    conteudo = f"""<main id="conteudo">
{faixa(P, ['Simulador'], 'Calculadora patrimonial', 'Veja o consórcio como estratégia, com os seus números', 'Arraste os controles e compare três cenários: vender a carta contemplada, comprar um imóvel que se paga com o aluguel ou deixar o crédito aplicado. É uma simulação educativa, não uma oferta.')}
<div class="wrap miolo">
  <div class="calc-quadro"><iframe class="calc-frame" src="../calculadora/?embed=1" title="Calculadora patrimonial ARVIA"></iframe></div>
  <div class="calc-depois">
    <p>Gostou do que viu? Eu monto a simulação oficial com um grupo real, o lance e o prazo certos para o seu objetivo.</p>
    <a class="btn btn-bordo" href="../#diagnostico">Quero a simulação com um grupo real</a>
  </div>
</div>
</main>"""
    return pagina("Simulador de consórcio · Calculadora Patrimonial ARVIA",
                  "Simule a carta de crédito, o lance e três estratégias patrimoniais com consórcio: vender a carta, imóvel para renda ou crédito aplicado.",
                  "simulador/", ld, "simulador", conteudo)


def pagina_fixa(meta):
    slug = meta["slug"]
    P = "../"
    corpo = re.sub(r"^\s*<h1>.*?</h1>\s*", "", meta["corpo"], flags=re.S)
    corpo = corpo.replace('<div class="tabela">', '<div class="tabela" tabindex="0" role="region" aria-label="Tabela">')
    h1 = re.search(r"<h1>(.*?)</h1>", meta["corpo"], re.S).group(1)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "ContactPage" if slug == "contato" else "WebPage", "name": meta["titulo"], "url": BASE + slug + "/", "inLanguage": "pt-BR", "publisher": EMPRESA_LD},
        migalhas(("Início", ""), (h1, slug + "/"))]}
    lado = ""
    if slug == "contato":
        corpo = re.sub(r'^\s*<p class="meta">.*?</p>\s*', "", corpo, flags=re.S)
        lado = f"""<aside class="cartao-lado" aria-labelledby="t-lado"><h2 id="t-lado">Prefere começar pelo diagnóstico?</h2><p>Responda algumas perguntas rápidas e eu chego na primeira conversa com um plano pensado para o seu objetivo.</p><a class="btn btn-ouro" href="../#diagnostico">Fazer meu diagnóstico</a></aside>"""
    texto = {"contato": "Fale direto com o consultor responsável pelo seu plano.",
             "privacidade": "Como coletamos, usamos e protegemos os seus dados pessoais.",
             "termos": "As regras de uso do site, do simulador e dos formulários.",
             "cookies": "O que o site guarda no seu navegador e como você controla."}.get(slug, "")
    conteudo = f"""<main id="conteudo">
{faixa(P, [h1], 'ARVIA Capital', h1, texto)}
<div class="wrap miolo"><div class="{'lado' if lado else ''}"><div class="prosa">{corpo}</div>{lado}</div></div>
</main>"""
    return pagina(meta["titulo"], meta["descricao"], slug + "/", ld, slug if slug == "contato" else "", conteudo)


def pagina_404():
    P = BASE
    conteudo = f"""<main id="conteudo">
<section class="faixa" aria-labelledby="t-pagina"><div class="wrap">
  <div class="eyebrow">Erro 404</div>
  <h1 id="t-pagina">Página não encontrada</h1>
  <p>O endereço pode ter mudado. Volte para o início, veja o blog ou fale comigo direto.</p>
  <p style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-ouro" href="{BASE}">Ir para o início</a><a class="btn btn-linha" href="{BASE}blog/">Ver o blog</a></p>
</div></section>
</main>"""
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": "Página não encontrada"}
    return cabeca("Página não encontrada · ARVIA Capital", "Página não encontrada.", BASE, ld, P, robots="noindex") + topo(P, "") + "\n" + conteudo + "\n" + rodape(P) + fim(P)


# ---------- página inicial ----------

def trocar(txt, nome, novo):
    a, b = f"<!--site:{nome}-->", f"<!--/site:{nome}-->"
    i, j = txt.index(a), txt.index(b)
    return txt[:i + len(a)] + "\n" + novo + "\n" + txt[j:]


def secao_blog(posts):
    return f"""<section class="bloco" id="blog" aria-labelledby="t-blog">
  <div class="wrap">
    <div class="blog-topo">
      <div class="titulo"><div class="eyebrow">Do blog</div><h2 id="t-blog">Para decidir com informação</h2><p>Matérias curtas sobre consórcio, lance e planejamento patrimonial.</p></div>
      <a class="btn btn-bordo" href="blog/">Ver todas as matérias</a>
    </div>
    <div class="lista">{cartoes(posts[:3], "", "h3")}</div>
  </div>
</section>"""


def atualizar_home(posts):
    f = RAIZ / "index.html"
    txt = f.read_text(encoding="utf-8")
    txt = trocar(txt, "topo", topo("", "", home=True))
    txt = trocar(txt, "rodape", rodape("", home=True))
    txt = trocar(txt, "blog", secao_blog(posts))
    txt = re.sub(r'assets/site\.(css|js)\?v=\d+', lambda m: f"assets/site.{m.group(1)}?v={VERSAO}", txt)
    f.write_text(txt, encoding="utf-8")


# ---------- sitemap ----------

def sitemap(posts):
    hoje = datetime.date.today().isoformat()
    urls = [(BASE, hoje, "1.0"), (BASE + "simulador/", hoje, "0.8"), (BASE + "blog/", hoje, "0.8"),
            (BASE + "contato/", hoje, "0.6"), (BASE + "links/", hoje, "0.5"),
            (BASE + "privacidade/", hoje, "0.3"), (BASE + "termos/", hoje, "0.3"), (BASE + "cookies/", hoje, "0.3")]
    urls += [(f"{BASE}blog/{p['slug']}/", p.get("atualizado", p["data"]), "0.7") for p in posts]
    corpo = "".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{corpo}</urlset>\n'


def escrever(caminho, txt):
    f = RAIZ / caminho
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(txt, encoding="utf-8")


def main():
    posts = ler_posts()
    escrever("blog/index.html", pagina_lista(posts))
    for p in posts:
        escrever(f"blog/{p['slug']}/index.html", pagina_post(p, posts))
    escrever("simulador/index.html", pagina_simulador())
    for f in sorted(PAGINAS.glob("*.html")):
        meta = ler_fonte(f)
        escrever(f"{meta['slug']}/index.html", pagina_fixa(meta))
    escrever("404.html", pagina_404())
    atualizar_home(posts)
    escrever("sitemap.xml", sitemap(posts))
    print(f"Site gerado: {len(posts)} matéria(s), simulador, {len(list(PAGINAS.glob('*.html')))} página(s) fixas e página inicial.")


if __name__ == "__main__":
    main()
