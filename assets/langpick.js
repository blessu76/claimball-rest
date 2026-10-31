/* Claimball: language of "/" (inlined into the root home page only; build_site fills in the list).
   Order: ?lang=xx in the URL > the language the visitor picked on the site (localStorage "cb-lang") > first match in
   navigator.languages (exact tag, then its first part: ko-KR -> ko, zh-TW -> zh) > stay on the English root.
   ?lang=xx (the company-wide hand-off from play.ipe.rest): a supported language is saved and "/" moves to "/xx/"
   (en stays on the root, the query is cleaned); an unsupported one is ignored and the later steps decide.
   No server redirect: crawlers see "/" as English. */
(function(){
  var S=/*SUPPORTED*/[];
  /* "ko-KR" -> "ko", "zh_TW" -> "zh" ... first supported match for a language tag, or '' */
  function pick(c){
    c=String(c||'').toLowerCase().replace(/_/g,'-');
    /* legacy codes: Android/old browsers say "in" for Indonesian. Traditional Chinese (zh-Hant) has no pages yet, so it goes to zh. */
    if(c.split('-')[0]==='in')c='id'+c.slice(2);
    if(S.indexOf(c)>=0)return c;
    var b=c.split('-')[0];
    return S.indexOf(b)>=0?b:'';
  }
  try{
    if(location.pathname!=='/')return;
    var to='',saved='',q=location.search||'',keep='',hasLang=false;
    var parts=q.replace(/^\?/,'').split('&').filter(Boolean),rest=[],want='';
    for(var j=0;j<parts.length;j++){
      var kv=parts[j].split('=');
      if(kv[0]==='lang'){hasLang=true;if(!want){try{want=pick(decodeURIComponent((kv.slice(1).join('=')||'').replace(/\+/g,' ')))}catch(e){}}}
      else rest.push(parts[j]);
    }
    keep=rest.length?'?'+rest.join('&'):'';
    if(want){
      try{localStorage.setItem('cb-lang',want)}catch(e){}
      if(want==='en'){
        if(hasLang&&history.replaceState)history.replaceState(null,'','/'+keep+location.hash);
        return;
      }
      to=want;
    }else{
      try{saved=localStorage.getItem('cb-lang')||''}catch(e){}
      if(S.indexOf(saved)>=0)to=saved;
      else{
        var L=(navigator.languages&&navigator.languages.length)?navigator.languages:[navigator.language||''];
        for(var i=0;i<L.length&&!to;i++)to=pick(L[i]);
      }
    }
    if(to&&to!=='en')location.replace('/'+to+'/'+keep+location.hash);
  }catch(e){}
})();

