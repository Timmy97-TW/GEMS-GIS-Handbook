(function(){
  var KEY='gems-gis-lang';
  function apply(l){
    document.body.setAttribute('data-lang',l);
    document.documentElement.lang = (l==='zh') ? 'zh-Hant' : 'en';
    var b=document.getElementById('langbtn');
    if(b) b.textContent = (l==='zh') ? 'English' : '繁體中文';
    try{localStorage.setItem(KEY,l)}catch(e){}
  }
  var saved='zh';
  try{ saved = localStorage.getItem(KEY) || 'zh' }catch(e){}
  document.addEventListener('DOMContentLoaded',function(){
    apply(saved);
    // the language switch changes the layout, so land on the anchor again
    if(location.hash){
      var tgt=document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if(tgt) setTimeout(function(){ tgt.scrollIntoView({block:'start',behavior:'instant'}); },0);
    }
    var b=document.getElementById('langbtn');
    if(b) b.addEventListener('click',function(){
      apply(document.body.getAttribute('data-lang')==='zh'?'en':'zh');
    });
    document.querySelectorAll('table.t').forEach(function(t){
      if(t.parentNode && t.parentNode.classList.contains('tscroll')) return;
      var d=document.createElement('div'); d.className='tscroll';
      t.parentNode.insertBefore(d,t); d.appendChild(t);
    });
    var lb=document.getElementById('lb');
    if(lb){
      var img=lb.querySelector('img');
      document.addEventListener('click',function(e){
        var t=e.target;
        var a=t.closest && t.closest('a[data-lb]');
        if(a){ e.preventDefault(); img.src=a.getAttribute('href'); img.alt=(t.alt||''); lb.classList.add('on'); return; }
        if(t.tagName==='IMG' && t.closest('figure.wide')){ img.src=t.getAttribute('data-full')||t.src; img.alt=t.alt||''; lb.classList.add('on'); return; }
        if(lb.classList.contains('on')) lb.classList.remove('on');
      });
      document.addEventListener('keydown',function(e){ if(e.key==='Escape') lb.classList.remove('on'); });
    }
  });
})();
