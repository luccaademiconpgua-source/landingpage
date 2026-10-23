/* © 2026 A&R Assessoria Estratégica Ltda. (ARVIA Capital). Todos os direitos reservados. */
(function(){
  // Menu do celular
  var botao = document.querySelector('.abre-menu'), menu = document.getElementById('menu-site');
  if(botao && menu){
    var fechar = function(){ menu.classList.remove('aberto'); botao.setAttribute('aria-expanded','false'); };
    botao.addEventListener('click', function(){
      var abrir = botao.getAttribute('aria-expanded') !== 'true';
      menu.classList.toggle('aberto', abrir); botao.setAttribute('aria-expanded', String(abrir));
    });
    menu.addEventListener('click', function(e){ if(e.target.closest('a')) fechar(); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && menu.classList.contains('aberto')){ fechar(); botao.focus(); } });
  }

  // Guarda de onde o visitante chegou (ex.: link da bio do Instagram) para enviar junto com o diagnóstico
  try{
    var u = new URLSearchParams(location.search);
    var origem = [u.get('utm_source'), u.get('utm_medium')].filter(Boolean).join(' / ');
    if(origem) sessionStorage.setItem('arviaTrafego', origem);
  }catch(e){}

  // Simulador incorporado: o quadro acompanha a altura do conteúdo
  window.addEventListener('message', function(ev){
    var d = ev.data; if(!d || typeof d.arviaCalcAltura !== 'number') return;
    document.querySelectorAll('iframe.calc-frame').forEach(function(f){
      if(ev.source === f.contentWindow) f.style.height = Math.max(600, d.arviaCalcAltura) + 'px';
    });
  });
})();
