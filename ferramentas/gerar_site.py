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
LOGO = '<svg class="logo-arvia" viewBox="6 2 316 120" aria-hidden="true"><path d="M14 92 L44 22 L74 92" fill="none" stroke="#7A1F2E" stroke-width="12"/><circle cx="44" cy="12" r="7" fill="#B08A3A"/><path d="M89.72506933021545 92.0V42.513964704513555H124.44225543022156Q129.9060518875122 42.513964704513555 133.50952405643463 44.65561153697968Q137.11299622535705 46.79725836944581 138.92057016563416 50.37696714496613Q140.72814410591124 53.956675920486454 140.72814410591124 58.30567090034485Q140.72814410591124 63.052220428466796 138.51473953056336 66.82933761596681Q136.30133495521545 70.6064548034668 132.08207295799255 72.75599037742614L142.1140616569519 92.0H126.7026361541748L118.47112429618835 75.0373663520813H103.48121330451966V92.0ZM103.48121330451966 64.86141727256775H120.85557964897156Q123.5067156715393 64.86141727256775 125.09367040157318 63.18602253246308Q126.68062513160706 61.510627792358406 126.68062513160706 58.686382394790655Q126.68062513160706 56.84303920173645 125.97013712882996 55.53710372447968Q125.25964912605286 54.231168247222904 123.96219620990753 53.52621895885468Q122.6647432937622 52.82126967048645 120.85557964897156 52.82126967048645H103.48121330451966Z M175.9920435256958 92.0 155.28709221076966 42.513964704513555H170.3275675201416L180.23745605659485 68.60215235900878Q180.70801925277712 69.71376354408264 181.3147502784729 71.42959529304504Q181.9214813041687 73.14542704200744 182.5617376508713 74.9135613861084Q183.20199399757385 76.68169573020936 183.6548339805603 78.07584109687805H184.16077203750612Q184.594830909729 76.8116057472229 185.1896967010498 75.10842641162873Q185.7845624923706 73.40524707603456 186.41874671268465 71.67839767932892Q187.05293093299866 69.95154828262329 187.56105635070801 68.63502345275879L197.5275387763977 42.513964704513555H211.91338490104675L191.22878138160706 92.0Z M228.59706933021548 92.0V42.513964704513555H242.35321330451967V92.0Z M258.8898544864655 92.0 280.2427092590332 42.513964704513555H296.09763406562803L317.4675824489593 92.0H302.6841651763916L299.35836857986453 83.72311034965514H276.33648618507385L273.0294706993103 92.0ZM280.3285551052094 73.55705231285096H295.3695538444519L291.3549254951477 63.31015721702576Q291.0699291229248 62.571246364593506 290.630383644104 61.36762199497223Q290.1908381652832 60.16399762535096 289.7239647703171 58.78688546180726Q289.25709137535097 57.40977329826355 288.8311635017395 56.128953125Q288.405235628128 54.84813295173645 288.1286933555603 54.02814661979676H287.6227552986145Q287.184118440628 55.37110769653321 286.57487213802335 57.10693986701966Q285.9656258354187 58.84277203750611 285.3799204788208 60.507508992195135Q284.7942151222229 62.17224594688416 284.34318345451356 63.32593470001221Z" fill="#7A1F2E"/><path d="M96.0475732421875 118.252Q93.78778662109374 118.252 92.20045886230469 117.46130334472656Q90.61313110351563 116.67060668945312 89.77906555175781 115.0175411376953Q88.945 113.3644755859375 88.945 110.79243444824219Q88.945 107.01426220703125 90.80441387939453 105.1735655517578Q92.66382775878907 103.33286889648437 96.0475732421875 103.33286889648437Q97.90105651855468 103.33286889648437 99.36694982910157 103.96241387939453Q100.83284313964845 104.5919588623047 101.68562591552734 105.85470050048829Q102.53840869140625 107.11744213867188 102.53840869140625 109.03483544921875H99.38929565429687Q99.38929565429687 108.03049096679688 98.97203729248048 107.33110150146484Q98.55477893066407 106.63171203613281 97.80928277587891 106.26284313964844Q97.06378662109375 105.89397424316407 96.07587658691406 105.89397424316407Q94.74375317382813 105.89397424316407 93.87408477783202 106.42079815673829Q93.00441638183594 106.9476220703125 92.59172357177735 107.96657324218751Q92.17903076171875 108.9855244140625 92.17903076171875 110.46555786132812V111.11931103515624Q92.17903076171875 112.61577893066406 92.59400634765625 113.63473010253907Q93.00898193359374 114.65368127441407 93.86815032958984 115.17228796386719Q94.72731872558595 115.69089465332031 96.06674548339844 115.69089465332031Q97.12222106933594 115.69089465332031 97.8932827758789 115.33480853271485Q98.66434448242188 114.97872241210938 99.0838856201172 114.28161572265626Q99.5034267578125 113.58450903320312 99.5034267578125 112.58473010253905H102.53840869140625Q102.53840869140625 114.49299230957031 101.70297424316406 115.7511683959961Q100.86753979492188 117.00934448242188 99.4039292602539 117.63067224121093Q97.94031872558594 118.252 96.0475732421875 118.252Z M126.13832775878906 118.0 131.67227893066405 103.58486889648438H135.5408752441406L141.0912608642578 118.0H137.70566455078125L136.66936889648437 115.1577120361328H130.40865417480467L129.37235852050782 118.0ZM131.29248193359373 112.64682775878906H135.77367224121093L134.4890321044922 109.08780969238282Q134.4050321044922 108.86867858886718 134.29181488037108 108.53633026123046Q134.17859765625 108.20398193359375 134.0571632080078 107.81319915771485Q133.93572875976562 107.42241638183594 133.81429431152344 107.02569915771485Q133.69285986328126 106.62898193359375 133.59242541503906 106.31854748535156H133.4737287597656Q133.35685986328124 106.72941638183593 133.18749096679687 107.26171972656249Q133.0181220703125 107.79402307128906 132.85468762207032 108.28387139892578Q132.69125317382813 108.7737197265625 132.5771220703125 109.08780969238282Z M165.41886889648435 118.0V103.58486889648438H172.92593310546874Q174.4717120361328 103.58486889648438 175.5112120361328 104.16328277587891Q176.5507120361328 104.74169665527344 177.08940869140625 105.78439331054688Q177.6281053466797 106.8270899658203 177.6281053466797 108.25965551757812Q177.6281053466797 109.68491772460938 177.07069146728514 110.7463316040039Q176.51327758789063 111.80774548339843 175.44090869140626 112.39209381103515Q174.36853979492187 112.97644213867187 172.81089196777344 112.97644213867187H168.5643341064453V118.0ZM168.5643341064453 110.41716455078125H172.40730334472656Q173.38882006835937 110.41716455078125 173.92066455078123 109.85016839599609Q174.4525090332031 109.28317224121093 174.4525090332031 108.26878662109375Q174.4525090332031 107.58400769042969 174.22105401611327 107.11881488037109Q173.98959899902343 106.6536220703125 173.54084063720703 106.40344982910156Q173.09208227539062 106.15327758789063 172.40730334472656 106.15327758789063H168.5643341064453Z M202.33736889648435 118.0V103.58486889648438H205.4828341064453V118.0Z M234.83582775878907 118.0V106.22906420898437H230.20486889648436V103.58486889648438H242.62412072753907V106.22906420898437H237.98129296874998V118.0Z M265.89532775878905 118.0 271.42927893066405 103.58486889648438H275.2978752441406L280.8482608642578 118.0H277.46266455078126L276.42636889648435 115.1577120361328H270.1656541748047L269.1293585205078 118.0ZM271.0494819335937 112.64682775878906H275.53067224121094L274.2460321044922 109.08780969238282Q274.1620321044922 108.86867858886718 274.0488148803711 108.53633026123046Q273.93559765624997 108.20398193359375 273.8141632080078 107.81319915771485Q273.6927287597656 107.42241638183594 273.5712943115234 107.02569915771485Q273.44985986328123 106.62898193359375 273.34942541503904 106.31854748535156H273.2307287597656Q273.1138598632812 106.72941638183593 272.9444909667968 107.26171972656249Q272.7751220703125 107.79402307128906 272.6116876220703 108.28387139892578Q272.4482531738281 108.7737197265625 272.3341220703125 109.08780969238282Z M305.17586889648436 118.0V103.58486889648438H308.3213341064453V115.33937023925782H315.58642407226563V118.0Z" fill="#B08A3A"/></svg>'


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
        p["capa"] = (RAIZ / "img" / "blog" / f"{p['slug']}.webp").exists()
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
    <a class="marca" href="{inicio}" aria-label="ARVIA Capital, ir para o início">{LOGO}</a>
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
        <a class="marca" href="{'#inicio' if home else (P or './')}" aria-label="ARVIA Capital, ir para o início">{LOGO}</a>
        <p class="sobre-curto">Consultoria patrimonial com consórcio: diagnóstico, estratégia de lance e acompanhamento em cada assembleia. Atendimento online para todo o Brasil e para brasileiros no exterior.</p>
      </div>
      <nav aria-label="Site"><h2>Site</h2><ul>
        <li><a href="{'#inicio' if home else (P or './')}">Início</a></li>
        <li><a href="{a('metodo')}">Método</a></li>
        <li><a href="{a('solucoes')}">Soluções</a></li>
        <li><a href="{'#simulador' if home else P + 'simulador/'}">Simulador</a></li>
        <li><a href="{P}brasileiros-no-exterior/">Brasileiros no exterior</a></li>
        <li><a href="{P}blog/">Blog</a></li>
        <li><a href="{a('arvia')}">Missão e valores</a></li>
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


def alt_imagem(titulo):
    return f"{titulo.split(' | ')[0].split(' · ')[0]} · ARVIA Capital"


def titulo_seo(titulo, limite=60):
    """O Google corta títulos muito longos: sem espaço, mantém só o título da página, sem a marca."""
    if len(titulo) <= limite:
        return titulo
    curto = re.split(r" \| | · ", titulo)[0]
    return curto if len(curto) <= limite + 4 else curto[:limite].rsplit(" ", 1)[0]


def cabeca(titulo, descricao, url, ld, P, tipo="website", robots="index, follow, max-image-preview:large", imagem=None, extra_head=""):
    return f"""<!DOCTYPE html>
<!-- © 2026 A&R Assessoria Estratégica Ltda. (ARVIA Capital). Todos os direitos reservados. Lei nº 9.609/1998 e Lei nº 9.610/1998. -->
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{ESC(titulo_seo(titulo))}</title>
<meta name="description" content="{ESC(descricao)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="{P}assets/favicon.ico?v=2" sizes="any"><link rel="icon" type="image/svg+xml" href="{P}assets/favicon.svg?v=2"><link rel="icon" type="image/png" sizes="32x32" href="{P}assets/favicon-32.png?v=2"><link rel="apple-touch-icon" href="{P}assets/favicon-180.png?v=2">
<meta property="og:type" content="{tipo}"><meta property="og:title" content="{ESC(titulo)}"><meta property="og:description" content="{ESC(descricao)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{imagem or BASE + 'og.jpg'}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{ESC(alt_imagem(titulo))}"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="ARVIA Capital">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{ESC(titulo)}"><meta name="twitter:description" content="{ESC(descricao)}"><meta name="twitter:image" content="{imagem or BASE + 'og.jpg'}">
<link rel="preload" href="{P}assets/fonts/montserrat-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{P}assets/fonts/cormorant-garamond-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{P}assets/site.css?v={VERSAO}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{extra_head}</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
"""


def fim(P):
    return f'\n<script src="{P}assets/site.js?v={VERSAO}" defer></script>\n</body>\n</html>\n'


def pagina(titulo, descricao, caminho, ld, atual, conteudo, tipo="website", robots="index, follow, max-image-preview:large", P=None, imagem=None, extra_head="", extra_fim=""):
    if P is None:
        P = "../" * caminho.count("/")
    return cabeca(titulo, descricao, BASE + caminho, ld, P, tipo, robots, imagem, extra_head) + topo(P, atual) + "\n" + conteudo + "\n" + rodape(P) + extra_fim + fim(P)


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
    capa = lambda p: f'<img class="capa" src="{P}img/blog/{p["slug"]}.webp" alt="" width="1200" height="630" loading="lazy" decoding="async">' if p.get("capa") else ""
    return "".join(f"""<a class="card" href="{P}blog/{p['slug']}/">{capa(p)}<span class="cat">{ESC(p['categoria'])}</span><{nivel}>{ESC(p['titulo'])}</{nivel}><p>{ESC(p['resumo'])}</p><span class="mais">Ler matéria · {p['leitura']} min</span></a>""" for p in posts)


# ---------- páginas ----------

def pagina_post(p, posts):
    caminho = f"blog/{p['slug']}/"
    url = BASE + caminho
    imagem = f"{BASE}img/blog/{p['slug']}.jpg" if p.get("capa") else BASE + "og.jpg"
    P = "../../"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": p["titulo"], "description": p["descricao"], "datePublished": p["data"], "dateModified": p.get("atualizado", p["data"]),
         "author": AUTOR_LD, "publisher": EMPRESA_LD, "mainEntityOfPage": url, "image": imagem, "inLanguage": "pt-BR", "articleSection": p["categoria"]},
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
        {f'<figure class="capa-post"><img src="{P}img/blog/{p["slug"]}.webp" alt="" width="1200" height="630" decoding="async"></figure>' if p.get("capa") else ""}
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
    return pagina(p["titulo_seo"], p["descricao"], caminho, ld, "blog", conteudo, "article", P=P, imagem=imagem)


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


def pagina_exterior():
    E = RAIZ / "ferramentas" / "especiais"
    css = (E / "exterior.css").read_text(encoding="utf-8")
    js = (E / "exterior.js").read_text(encoding="utf-8")
    conteudo = (E / "exterior.html").read_text(encoding="utf-8")
    perguntas = re.findall(r"<summary>(.*?)</summary><p>(.*?)</p>", conteudo)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "name": "Consórcio para brasileiros no exterior", "url": BASE + "brasileiros-no-exterior/", "inLanguage": "pt-BR", "publisher": EMPRESA_LD},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in perguntas]},
        migalhas(("Início", ""), ("Brasileiros no exterior", "brasileiros-no-exterior/"))]}
    return pagina("Consórcio para brasileiros no exterior | ARVIA Capital",
                  "Mora fora? Simule a parcela do consórcio em dólar, euro ou libra e compare com o financiamento. Imóvel no Brasil sem juros, com atendimento 100% online.",
                  "brasileiros-no-exterior/", ld, "exterior", conteudo,
                  extra_head=f"<style>{css}</style>\n", extra_fim=f"\n<script>{js}</script>")


def pagina_fixa(meta):
    slug = meta["slug"]
    P = "../"
    corpo = re.sub(r"^\s*<h1>.*?</h1>\s*", "", meta["corpo"], flags=re.S)
    _n = iter(range(1, 50))
    corpo = re.sub(r'<div class="tabela">', lambda m: f'<div class="tabela" tabindex="0" role="region" aria-label="Tabela {next(_n)}">', corpo)
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
      <div class="titulo"><h2 id="t-blog">Para decidir com informação</h2><p>Matérias curtas sobre consórcio, lance e planejamento patrimonial.</p></div>
      <a class="btn btn-bordo" href="blog/">Ver todas as matérias</a>
    </div>
    <div class="lista">{cartoes(posts[:3], "", "h3").replace("Ler matéria · ", "Leitura de ")}</div>
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
    urls = [(BASE, hoje, "1.0"), (BASE + "simulador/", hoje, "0.8"), (BASE + "brasileiros-no-exterior/", hoje, "0.9"), (BASE + "blog/", hoje, "0.8"),
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
    escrever("brasileiros-no-exterior/index.html", pagina_exterior())
    for f in sorted(PAGINAS.glob("*.html")):
        meta = ler_fonte(f)
        escrever(f"{meta['slug']}/index.html", pagina_fixa(meta))
    escrever("404.html", pagina_404())
    atualizar_home(posts)
    escrever("sitemap.xml", sitemap(posts))
    print(f"Site gerado: {len(posts)} matéria(s), simulador, {len(list(PAGINAS.glob('*.html')))} página(s) fixas e página inicial.")


if __name__ == "__main__":
    main()
