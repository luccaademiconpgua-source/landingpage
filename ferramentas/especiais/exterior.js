(function(){
  var $ = function(id){ return document.getElementById(id); };
  var TAXA_ADM = 0.242;
  var SIMB = {USD:'US$', EUR:'€', GBP:'£', JPY:'¥', CAD:'C$', AUD:'A$', CHF:'CHF'};
  var NOME = {USD:'dólar', EUR:'euro', GBP:'libra', JPY:'iene', CAD:'dólar canadense', AUD:'dólar australiano', CHF:'franco suíço'};
  var cot = null, cotData = '';
  var brl = function(v){ return v.toLocaleString('pt-BR', {style:'currency', currency:'BRL', maximumFractionDigits:0}); };
  var brl2 = function(v){ return v.toLocaleString('pt-BR', {style:'currency', currency:'BRL', minimumFractionDigits:2, maximumFractionDigits:2}); };
  var em = function(v, m){ var d = m === 'JPY' ? 0 : 0; return SIMB[m] + ' ' + Math.round(v).toLocaleString('pt-BR', {maximumFractionDigits:d}); };
  var val = function(n){ var r = document.querySelector('input[name="'+n+'"]:checked'); return r ? r.value : ''; };

  function simular(){
    var carta = +$('s-carta').value, prazo = +$('s-prazo').value, pct = +val('pct'), moeda = val('moeda');
    $('o-carta').textContent = brl(carta);
    $('o-prazo').textContent = prazo + ' meses';
    var integral = carta * (1 + TAXA_ADM) / prazo;
    var parcela = integral * pct;
    $('r-rot').textContent = pct < 1 ? 'Parcela estimada até a contemplação (' + Math.round(pct*100) + '%)' : 'Parcela estimada';
    $('r-reais').textContent = 'Em reais: ' + brl2(parcela) + ' por mês';
    if(cot){
      $('r-moeda').innerHTML = em(parcela * cot[moeda], moeda) + ' <small>por mês</small>';
      $('r-moedas').innerHTML = Object.keys(SIMB).filter(function(m){ return m !== moeda; }).map(function(m){
        return '<div><b>' + em(parcela * cot[m], m) + '</b><span>' + NOME[m] + '</span></div>';
      }).join('');
    } else {
      $('r-moeda').innerHTML = brl2(parcela) + ' <small>por mês</small>';
      $('r-moedas').innerHTML = '<div style="grid-column:1/-1"><span>Não consegui carregar a cotação agora. Tente atualizar a página.</span></div>';
    }
    comparar(carta, prazo, integral);
  }

  function comparar(carta, prazoCons, integral){
    var aa = Math.max(0, parseFloat(String($('c-juros').value).replace(',', '.')) || 0) / 100;
    var n = Math.max(12, Math.round(+$('c-prazo').value || 360));
    var im = Math.pow(1 + aa, 1/12) - 1;
    var juros = im * carta * (n + 1) / 2;            // SAC: juros totais
    var p1 = carta / n + carta * im;                   // SAC: primeira parcela
    var totalF = carta + juros, totalC = carta * (1 + TAXA_ADM);
    $('f-valor').textContent = brl(carta);
    $('f-p1').textContent = brl2(p1);
    $('f-juros').textContent = brl(juros);
    $('f-total').textContent = brl(totalF);
    $('k-valor').textContent = brl(carta);
    $('k-p1').textContent = brl2(integral);
    $('k-total').textContent = brl(totalC);
    var dif = totalF - totalC;
    $('c-dif').innerHTML = dif > 0
      ? 'No financiamento você pagaria <b>' + brl(dif) + ' a mais</b> pelo mesmo crédito, o equivalente a ' + (totalF/totalC).toLocaleString('pt-BR', {maximumFractionDigits:1}) + ' vezes o total do consórcio.'
      : 'Com essa taxa e esse prazo, o total do financiamento fica abaixo do consórcio. Fale comigo para avaliar o seu caso.';
  }

  ['s-carta','s-prazo','c-juros','c-prazo'].forEach(function(id){ $(id).addEventListener('input', simular); });
  document.querySelectorAll('input[name="pct"],input[name="moeda"]').forEach(function(r){ r.addEventListener('change', simular); });
  simular();

  // Cotação do dia (ExchangeRate-API, acesso aberto)
  fetch('https://open.er-api.com/v6/latest/BRL').then(function(r){ return r.json(); }).then(function(d){
    if(d && d.result === 'success'){
      cot = d.rates;
      try{ cotData = new Date(d.time_last_update_unix * 1000).toLocaleDateString('pt-BR'); }catch(e){}
      var o = $('r-obs');
      o.innerHTML += ' Cotação de ' + cotData + ' por <a href="https://www.exchangerate-api.com" target="_blank" rel="noopener">ExchangeRate-API</a>.';
      simular();
    }
  }).catch(function(){});

  // Formulário: código do país acompanha o país escolhido
  $('x-pais').addEventListener('change', function(){
    var o = this.options[this.selectedIndex]; var ddi = o && o.getAttribute('data-ddi');
    if(ddi) $('x-ddi').value = ddi;
  });

  var CRM_URL = "https://maudmkjtzryqqytqgbki.supabase.co";
  var CRM_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hdWRta2p0enJ5cXF5dHFnYmtpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI3MjM5NzQsImV4cCI6MjEwODI5OTk3NH0.97yrWMLZkufXjuvkmjTYCBW0_eZoGEco1GrcYLyUxi4"; // chave pública (anon): só permite enviar leads, não ler
  var WHATS = "5541988402942";
  var form = $('ficha-ext');
  form.addEventListener('submit', function(e){
    e.preventDefault();
    if($('x-site').value) return;
    var d = { nome: $('x-nome').value.trim(), pais: $('x-pais').value, ddi: $('x-ddi').value.trim(), numero: $('x-whats').value.trim(),
      email: $('x-email').value.trim(), obj: $('x-obj').value, valor: $('x-valor').value, aceite: $('x-aceite').checked };
    var regras = { nome: d.nome.length > 1, pais: !!d.pais, whats: /^\+?\d{1,4}$/.test(d.ddi.replace(/\s/g,'')) && d.numero.replace(/\D/g,'').length >= 6,
      email: /^\S+@\S+\.\S+$/.test(d.email), obj: !!d.obj, valor: !!d.valor, aceite: d.aceite };
    var primeiro = null;
    Object.keys(regras).forEach(function(k){
      var el = form.querySelector('[data-c="'+k+'"]'); if(!el) return;
      el.classList.toggle('invalido', !regras[k]);
      if(!regras[k] && !primeiro) primeiro = el;
    });
    if(primeiro){ primeiro.scrollIntoView({behavior:'smooth', block:'center'}); var f = primeiro.querySelector('input,select'); if(f) f.focus({preventScroll:true}); return; }

    var whats = (d.ddi.charAt(0) === '+' ? d.ddi : '+' + d.ddi) + ' ' + d.numero;
    var trafego = ''; try{ trafego = sessionStorage.getItem('arviaTrafego') || ''; }catch(err){}
    var sim = { carta: +$('s-carta').value, prazo: +$('s-prazo').value, moeda: val('moeda') };
    try{
      fetch(CRM_URL + "/rest/v1/leads", {
        method:"POST", keepalive:true,
        headers:{ "apikey":CRM_KEY, "Authorization":"Bearer "+CRM_KEY, "Content-Type":"application/json", "Prefer":"return=minimal" },
        body: JSON.stringify({ origem:"exterior", nome:d.nome, whatsapp:whats, email:d.email, segmento:"Imóvel", objetivo:d.obj, valor_mensal:d.valor,
          qualificacao:{ pais:d.pais, moeda:sim.moeda, carta_simulada:sim.carta, prazo_simulado:sim.prazo, trafego: trafego || undefined },
          consentimento:true, consentimento_em:new Date().toISOString() })
      }).catch(function(){});
    }catch(err){}
    var msg = ["Olá Lucca! Moro fora do Brasil e quero uma estratégia de consórcio.", "",
      "Nome: " + d.nome, "País: " + d.pais, "WhatsApp: " + whats, "E-mail: " + d.email, "Objetivo: " + d.obj, "Quanto investir por mês: " + d.valor,
      "Simulei: carta de " + brl(sim.carta) + " em " + sim.prazo + " meses (" + sim.moeda + ")"].join("\n");
    var ok = $('x-ok');
    ok.textContent = "Recebi os seus dados. O WhatsApp vai abrir com a mensagem pronta; é só enviar.";
    ok.classList.add('show');
    window.open("https://wa.me/" + WHATS + "?text=" + encodeURIComponent(msg), "_blank");
  });
})();
