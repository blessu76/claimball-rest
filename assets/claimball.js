(function(){
  /* an explicit language choice wins over the browser language the root page follows (see langpick.js) */
  function remember(l){try{localStorage.setItem('ipe_lang',l)}catch(x){}}
  document.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('.langs a[hreflang]');
    if(a)remember(a.getAttribute('hreflang'));
  });
})();
