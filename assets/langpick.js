/* Claimball: language of every page without a language prefix ("/", /about/, /journal/..., never /xx/ and never 404.html).
   Inlined by build_site, which fills in S (all site languages) and A (the languages that really have THIS page).
   Order: ?lang=xx in the URL > the language the visitor picked on the site (localStorage "ipe_lang") > first match in
   navigator.languages (same rules as the kit's languages.resolve: zh-TW/HK/MO/Hant -> zh-Hant, zh-CN/Hans -> none,
   pt* -> pt-BR, in -> id, en* -> en, other tags by their first part) > stay on the English root.
   Redirect only when the language is not English and A has it; otherwise the page stays (no fallback to the next browser language).
   ?lang=xx (the company-wide hand-off from play.ipe.rest): a supported language is saved and the page moves to "/xx/<same path>"
   (en stays on the page, the query is cleaned); an unsupported one is ignored and the later steps decide. Other query params and #hash are kept.
   Bots (bot/crawl/spider/slurp/lighthouse user agents) are never redirected.
   No server redirect: crawlers see "/" as English. */
(function(){
  var S=/*SUPPORTED*/[],A=/*AVAILABLE*/[];
  /* browser/device tag -> a supported language, or '' (zh-CN, ru, ... -> '' so the next browser language is tried) */
  function pick(c){
    var p=String(c||'').toLowerCase().replace(/_/g,'-').split('-').filter(Boolean);
    if(!p.length)return '';
    var code=p[0]==='in'?'id':p[0];
    if(code==='zh'){
      var sub=p.slice(1);
      var script=sub.filter(function(x){return x.length===4&&/^[a-z]+$/.test(x)})[0];
      var region=sub.filter(function(x){return x.length===2&&/^[a-z]+$/.test(x)})[0];
      var hant=script?script==='hant':(!!region&&['tw','hk','mo'].indexOf(region)>=0);
      return hant&&S.indexOf('zh-Hant')>=0?'zh-Hant':'';
    }
    if(code==='pt')return S.indexOf('pt-BR')>=0?'pt-BR':'';
    for(var i=0;i<S.length;i++)if(S[i].toLowerCase()===code)return S[i];
    return '';
  }
  if(/bot|crawl|spider|slurp|lighthouse/i.test(navigator.userAgent||''))return;
  try{
    var seg=location.pathname.split('/')[1];
    for(var k=0;seg&&k<S.length;k++)if(S[k].toLowerCase()===seg.toLowerCase())return;
    var to='',saved='',q=location.search||'',keep='',hasLang=false;
    var parts=q.replace(/^\?/,'').split('&').filter(Boolean),rest=[],want='';
    for(var j=0;j<parts.length;j++){
      var kv=parts[j].split('=');
      if(kv[0]==='lang'){hasLang=true;if(!want){try{want=pick(decodeURIComponent((kv.slice(1).join('=')||'').replace(/\+/g,' ')))}catch(e){}}}
      else rest.push(parts[j]);
    }
    keep=rest.length?'?'+rest.join('&'):'';
    if(want){
      try{localStorage.setItem('ipe_lang',want)}catch(e){}
      if(want==='en'){
        if(hasLang&&history.replaceState)history.replaceState(null,'',location.pathname+keep+location.hash);
        return;
      }
      to=want;
    }else{
      try{saved=localStorage.getItem('ipe_lang')||''}catch(e){}
      if(S.indexOf(saved)>=0)to=saved;
      else{
        var L=(navigator.languages&&navigator.languages.length)?navigator.languages:[navigator.language||''];
        for(var i=0;i<L.length&&!to;i++)to=pick(L[i]);
      }
    }
    if(to&&to!=='en'&&A.indexOf(to)>=0)location.replace('/'+to+location.pathname+keep+location.hash);
    else if(want&&history.replaceState)history.replaceState(null,'',location.pathname+keep+location.hash);
  }catch(e){}
})();

