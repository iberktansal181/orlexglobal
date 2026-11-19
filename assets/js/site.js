/* ORLEX Global — interactions. Vanilla JS, no dependencies. */
(function(){
  'use strict';
  var d=document, w=window, root=d.documentElement;
  var reduce=w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $=function(s,c){return (c||d).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
  var esc=function(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})};
  var GROUPS=w.ORLEX_GROUPS||[];
  var thumb=function(k,cls,lazy){return k?'<img class="'+cls+'" '+(lazy?'data-src':'src')+'="assets/img/p/'+encodeURIComponent(k)+'.webp" alt="" width="56" height="56" loading="lazy" decoding="async">':'<span class="'+cls+' none" aria-hidden="true"></span>'};
  var REGIONS={
    neck:{label:'Neck',title:'Neck & cervical'},
    shoulder:{label:'Shoulder',title:'Shoulder & arm'},
    elbow:{label:'Elbow',title:'Elbow'},
    hand:{label:'Wrist & hand',title:'Wrist, hand & fingers'},
    spine:{label:'Back',title:'Spine, back & abdomen'},
    hip:{label:'Hip',title:'Hip'},
    knee:{label:'Knee',title:'Knee'},
    leg:{label:'Leg',title:'Calf, thigh & compression'},
    foot:{label:'Ankle & foot',title:'Ankle & foot'}
  };
  var CATS={all:'All groups',upper:'Upper limb',spine:'Spine & corsets',lower:'Lower limb',paed:'Pediatric',comp:'Compression & women’s health',rehab:'Rehab & mobility',std:'Standard sizes'};

  /* ---------- enquiry store ---------- */
  var KEY='orlex-enquiry', mem=[];
  function load(){try{var v=JSON.parse(w.localStorage.getItem(KEY)||'[]');return Array.isArray(v)?v:[]}catch(e){return mem.slice()}}
  function save(a){mem=a.slice();try{w.localStorage.setItem(KEY,JSON.stringify(a))}catch(e){}}
  var picked=load();
  function has(code){return picked.indexOf(code)>-1}
  function toggle(code){var i=picked.indexOf(code);if(i>-1)picked.splice(i,1);else picked.push(code);save(picked);updateTray(true);return i===-1}
  function updateTray(bump){
    $$('.tray-btn .count').forEach(function(el){el.textContent=picked.length;el.setAttribute('data-n',picked.length);if(bump&&!reduce){el.classList.add('bump');setTimeout(function(){el.classList.remove('bump')},300)}});
    $$('[data-code]').forEach(function(b){var on=has(b.getAttribute('data-code'));b.classList.toggle('on',on);b.setAttribute('aria-pressed',on)});
    renderPicked();
  }
  var toastEl,toastT;
  function toast(html){
    if(!toastEl){toastEl=d.createElement('div');toastEl.className='toast';toastEl.setAttribute('role','status');d.body.appendChild(toastEl)}
    toastEl.innerHTML=html;toastEl.classList.add('show');clearTimeout(toastT);toastT=setTimeout(function(){toastEl.classList.remove('show')},2600);
  }
  d.addEventListener('click',function(e){
    var b=e.target.closest('[data-code]');if(!b)return;
    e.preventDefault();e.stopPropagation();
    var code=b.getAttribute('data-code'),added=toggle(code);
    toast(added?(esc(code)+' added to your enquiry · <a href="contact.html">Review</a>'):(esc(code)+' removed'));
  });

  /* ---------- header, progress, menu ---------- */
  var hdr=$('.hdr'),bar=$('.progress');
  function onScroll(){
    var y=w.scrollY||0,h=root.scrollHeight-w.innerHeight;
    if(hdr)hdr.classList.toggle('scrolled',y>8);
    if(bar)bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')';
    timelines.forEach(tlUpdate);
  }
  var burger=$('.burger');
  if(burger)burger.addEventListener('click',function(){var o=d.body.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o)});
  $$('.nav a').forEach(function(a){a.addEventListener('click',function(){d.body.classList.remove('menu-open')})});

  /* ---------- reveal + draw ---------- */
  $$('.draw path,.draw circle').forEach(function(p){try{var L=Math.ceil(p.getTotalLength());p.style.setProperty('--len',L)}catch(e){}});
  if('IntersectionObserver' in w&&!reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);if(en.target.hasAttribute('data-count'))count(en.target)}})},{threshold:.15,rootMargin:'0px 0px -6% 0px'});
    $$('[data-reveal],.draw,[data-count]').forEach(function(el){io.observe(el)});
  }else{$$('[data-reveal],.draw').forEach(function(el){el.classList.add('in')});$$('[data-count]').forEach(function(el){el.textContent=el.getAttribute('data-count')})}
  function count(el){
    var to=+el.getAttribute('data-count'),from=+(el.getAttribute('data-from')||0),t0=null,dur=1600;
    function f(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-p,4);el.textContent=Math.round(from+(to-from)*e);if(p<1)requestAnimationFrame(f)}
    requestAnimationFrame(f);
  }

  /* ---------- pointer spotlight + magnetic ---------- */
  var pmE=null;
  d.addEventListener('pointermove',function(e){
    if(pmE){pmE=e;return}pmE=e;
    requestAnimationFrame(function(){var ev=pmE;pmE=null;var c=ev.target.closest&&ev.target.closest('.card,.cert');
      if(c){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(ev.clientX-r.left)+'px');c.style.setProperty('--my',(ev.clientY-r.top)+'px')}});
  },{passive:true});
  if(!reduce&&w.matchMedia('(pointer:fine)').matches){
    $$('[data-magnetic]').forEach(function(b){
      b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;b.style.transform='translate('+x*.18+'px,'+y*.3+'px)'});
      b.addEventListener('pointerleave',function(){b.style.transform=''});
    });
  }

  /* ---------- hero words ---------- */
  var h1=$('.hero h1[data-split]');
  if(h1){
    var i=0;
    h1.innerHTML=h1.innerHTML.replace(/(<[^>]+>)|([^\s<]+)/g,function(m,tag,word){if(tag)return tag;i++;return '<span class="w"><span style="transition-delay:'+(0.08*i).toFixed(2)+'s">'+word+'</span></span>'});
  }
  requestAnimationFrame(function(){d.body.classList.add('ready')});

  /* ---------- orbit ---------- */
  var orbit=$('.orbit-wrap');
  if(orbit){
    var sats=$$('.sat',orbit),core=$('.core',orbit),ang=0,running=!reduce,hover=false;
    function place(){
      var R=orbit.clientWidth*0.44;
      sats.forEach(function(s,k){var a=ang+k*(2*Math.PI/sats.length)-Math.PI/2;s.style.transform='translate(-50%,-50%) translate('+(Math.cos(a)*R).toFixed(1)+'px,'+(Math.sin(a)*R*0.92).toFixed(1)+'px)'});
    }
    var vis=true,raf=0;
    function tick(){raf=0;if(!hover)ang+=0.0016;place();if(running&&vis&&!d.hidden)raf=requestAnimationFrame(tick)}
    function kick(){if(running&&vis&&!d.hidden&&!raf)raf=requestAnimationFrame(tick)}
    if('IntersectionObserver' in w)new IntersectionObserver(function(es){vis=es[0].isIntersecting;kick()}).observe(orbit);
    d.addEventListener('visibilitychange',kick);
    orbit.addEventListener('pointerenter',function(){hover=true});
    orbit.addEventListener('pointerleave',function(){hover=false;if(core)core.style.transform=''});
    orbit.addEventListener('pointermove',function(e){if(!core||reduce)return;var r=orbit.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;core.style.transform='rotate('+(x*40)+'deg) translate('+(x*14)+'px,'+(y*14)+'px)'});
    w.addEventListener('resize',place);place();kick();
  }

  /* ---------- body map (male front/back, from the ORLEX order app) ---------- */
  var BODY=w.ORLEX_BODY, byCode={};
  GROUPS.forEach(function(g){g.refs.forEach(function(r){byCode[r[0]]={g:g,n:r[1],t:r[2]}})});
  $$('[data-bodymap]').forEach(function(map){
    if(!BODY)return;
    var NS='http://www.w3.org/2000/svg',svg=$('.figure svg',map),panel=$('.panel',map),pills=$('.region-pills',map),kidsBox=$('.kids input',map),
        linkBase=map.getAttribute('data-link')||'products.html',view='front',sel=map.getAttribute('data-start')||'knee',kids=false;
    function list(r){return ((kids?BODY.kids:BODY.adult)[r])||[]}
    function draw(){
      var F=BODY.fig[view],html='<image href="assets/img/body-'+view+'.webp" x="0" y="0" width="600" height="1000"/><g class="zones">';
      Object.keys(F.r).forEach(function(r){var n=list(r).length;html+='<g class="z'+(r===sel?' on':'')+(n?'':' empty')+'" data-r="'+r+'" style="--c:'+BODY.colors[r]+'">'+F.r[r].map(function(d){return '<path d="'+d+'"/>'}).join('')+'</g>'});
      html+='</g><g class="dots">';
      var MID={chest:1,abdomen:1,back:1,neck:1};
      Object.keys(F.p).forEach(function(r){var n=list(r).length;F.p[r].forEach(function(pt){var x=(MID[r]&&F.p[r].length===1)?300:pt[0],y=pt[1];
        html+='<g class="d'+(r===sel?' on':'')+(n?'':' empty')+'" data-r="'+r+'" style="--c:'+BODY.colors[r]+'" tabindex="'+(n?0:-1)+'" role="button" aria-label="'+BODY.names[r]+' · '+n+' references"><title>'+BODY.names[r]+' ('+n+')</title><circle class="hit" cx="'+x+'" cy="'+y+'" r="28"/><circle class="ring" cx="'+x+'" cy="'+y+'" r="12"/><circle class="dot" cx="'+x+'" cy="'+y+'" r="10"/><circle class="in" cx="'+x+'" cy="'+y+'" r="4"/></g>'})});
      svg.innerHTML=html+'</g>';
      pills.innerHTML=Object.keys(BODY.names).filter(function(r){return F.p[r]}).map(function(r){var n=list(r).length;return '<button type="button" data-r="'+r+'" class="'+(r===sel?'on':'')+'"'+(n?'':' disabled')+'><i style="background:'+BODY.colors[r]+'"></i>'+BODY.names[r]+'<span class="n">'+n+'</span></button>'}).join('');
    }
    function show(){
      var codes=list(sel),gs={},order=[];
      codes.forEach(function(c){var x=byCode[c];if(!x)return;if(!gs[x.g.id]){gs[x.g.id]={g:x.g,n:0};order.push(x.g.id)}gs[x.g.id].n++});
      var chips=codes.slice(0,12).map(function(c){var x=byCode[c]||{};return '<button type="button" class="tile pick" data-code="'+esc(c)+'" title="'+esc(x.n||'')+'">'+thumb(x.t,'ti',false)+'<b>'+esc(c.replace('ORX-',''))+'</b></button>'}).join('');
      panel.innerHTML='<div class="panel-enter"><div class="region" style="--c:'+BODY.colors[sel]+'"><i></i>'+(kids?'Children · ':'')+'Body region</div><h3>'+BODY.names[sel]+'</h3><div class="meta">'+
        (codes.length?(order.length+' product group'+(order.length>1?'s':'')+' · '+codes.length+' reference'+(codes.length>1?'s':'')):'No '+(kids?'children’s ':'')+'products for this region')+'</div><ul>'+
        order.map(function(id){var o=gs[id];return '<li><a href="'+linkBase+'#'+id+'"><span>'+esc(o.g.name)+'</span><small>'+o.n+' ref'+(o.n>1?'s':'')+' →</small></a></li>'}).join('')+'</ul>'+
        (codes.length?'<p class="hint-s">Tap a code to add it to your enquiry</p><div class="codes">'+chips+(codes.length>12?'<span class="tile more">+'+(codes.length-12)+'<small>more</small></span>':'')+'</div>':'')+'</div>';
      updateTray(false);
    }
    function pick(r){if(!list(r).length)return;sel=r;$$('.z,.d',svg).forEach(function(el){el.classList.toggle('on',el.getAttribute('data-r')===r)});$$('button',pills).forEach(function(b){b.classList.toggle('on',b.getAttribute('data-r')===r)});show()}
    svg.addEventListener('click',function(e){var t=e.target.closest('[data-r]');if(t)pick(t.getAttribute('data-r'))});
    svg.addEventListener('keydown',function(e){var t=e.target.closest('[data-r]');if(t&&(e.key==='Enter'||e.key===' ')){e.preventDefault();pick(t.getAttribute('data-r'))}});
    svg.addEventListener('pointerover',function(e){var t=e.target.closest('[data-r]');$$('.z',svg).forEach(function(z){z.classList.toggle('hov',!!t&&z.getAttribute('data-r')===t.getAttribute('data-r'))})});
    svg.addEventListener('pointerleave',function(){$$('.z.hov',svg).forEach(function(z){z.classList.remove('hov')})});
    pills.addEventListener('click',function(e){var b=e.target.closest('button[data-r]');if(b)pick(b.getAttribute('data-r'))});
    $$('.seg button',map).forEach(function(b){b.addEventListener('click',function(){view=b.getAttribute('data-view');$$('.seg button',map).forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',x===b)});
      if(!BODY.fig[view].p[sel]){sel=view==='back'?'back':'chest'}draw();show()})});
    if(kidsBox)kidsBox.addEventListener('change',function(){kids=kidsBox.checked;if(!list(sel).length){var f=Object.keys(BODY.fig[view].p).filter(function(r){return list(r).length});sel=f.indexOf('hip')>-1?'hip':f[0]}draw();show()});
    if(!BODY.names[sel]||!list(sel).length||!BODY.fig[view].p[sel])sel=Object.keys(BODY.fig[view].p).filter(function(r){return list(r).length})[0];
    draw();show();
  });

  /* ---------- explorer ---------- */
  var ex=$('#explorer');
  if(ex){
    var list=$('.groups',ex),q=$('#q'),filt=$('.filters'),line=$('.result-line',ex),cat='all';
    var totals={all:0};GROUPS.forEach(function(g){totals.all+=g.refs.length;totals[g.cat]=(totals[g.cat]||0)+g.refs.length});
    filt.innerHTML=Object.keys(CATS).filter(function(k){return totals[k]}).map(function(k){return '<button type="button" data-cat="'+k+'" class="'+(k==='all'?'on':'')+'">'+CATS[k]+'<span class="n">'+totals[k]+'</span></button>'}).join('');
    list.innerHTML=GROUPS.map(function(g){
      return '<article class="group" id="'+g.id+'" data-cat="'+g.cat+'"><button type="button" class="group-h" aria-expanded="false"><span class="gi">'+(g.refs[0][2]?'<img src="assets/img/p/'+encodeURIComponent(g.refs[0][2])+'.webp" alt="" width="48" height="48" loading="lazy" decoding="async">':esc(g.prefix))+'</span><span><h3>'+esc(g.name)+'</h3><p>'+esc(g.desc)+'</p></span><span class="cnt"><span class="k">'+g.refs.length+'</span> ref'+(g.refs.length===1?'':'s')+'</span><span class="tog" aria-hidden="true"></span></button>'+
      '<div class="group-b"><div><div class="refs">'+g.refs.map(function(r){return '<div class="ref" data-t="'+esc((r[0]+' '+r[0].replace(/\s/g,'')+' '+r[1]).toLowerCase())+'">'+thumb(r[2],'rt',true)+'<span class="rx"><span class="c">'+esc(r[0])+'</span><span class="nm">'+esc(r[1])+'</span></span><button type="button" class="add" data-code="'+esc(r[0])+'" aria-label="Add '+esc(r[0])+' to enquiry" aria-pressed="false"></button></div>'}).join('')+'</div>'+
      '<div class="group-f"><a class="link" href="'+esc(g.url)+'" target="_blank" rel="noopener">Photos & size charts on orlex.com.tr ↗</a><button type="button" class="btn sm ghost add-all">Add all '+esc(g.prefix)+' codes to enquiry</button></div></div></div></article>';
    }).join('');
    function setOpen(art,o){art.classList.toggle('open',o);$('.group-h',art).setAttribute('aria-expanded',o);if(o)$$('img[data-src]',art).forEach(function(im){im.src=im.getAttribute('data-src');im.removeAttribute('data-src')})}
    list.addEventListener('click',function(e){
      var h=e.target.closest('.group-h');if(h){var a=h.parentNode;setOpen(a,!a.classList.contains('open'));return}
      var all=e.target.closest('.add-all');if(all){var art=all.closest('.group'),n=0;$$('.ref:not([hidden]) .add',art).forEach(function(b){var c=b.getAttribute('data-code');if(!has(c)){picked.push(c);n++}});save(picked);updateTray(true);toast(n+' codes added · <a href="contact.html">Review enquiry</a>')}
    });
    function apply(){
      var term=(q.value||'').trim().toLowerCase(),tn=term.replace(/\s/g,''),shown=0,gshown=0;
      $$('.group',list).forEach(function(art){
        var okCat=cat==='all'||art.getAttribute('data-cat')===cat,k=0;
        $$('.ref',art).forEach(function(r){
          var t=r.getAttribute('data-t'),hit=!term||t.indexOf(term)>-1||t.indexOf(tn)>-1;
          r.hidden=!hit;if(hit)k++;
          var nm=$('.nm',r),c=$('.c',r);
          [nm,c].forEach(function(el){var raw=el.textContent;if(term&&raw.toLowerCase().indexOf(term)>-1){var i=raw.toLowerCase().indexOf(term);el.innerHTML=esc(raw.slice(0,i))+'<mark>'+esc(raw.slice(i,i+term.length))+'</mark>'+esc(raw.slice(i+term.length))}else el.textContent=raw});
        });
        var vis=okCat&&k>0;art.hidden=!vis;if(vis){gshown++;shown+=k}
        $('.cnt .k',art).textContent=k;
        if(term)setOpen(art,vis);
      });
      line.innerHTML=shown?('Showing <b>'+gshown+'</b> group'+(gshown>1?'s':'')+' · <b>'+shown+'</b> reference'+(shown===1?'':'s')+(term?' matching “'+esc(q.value.trim())+'”':'')):'';
      var em=$('.empty',ex);em.hidden=shown>0;
    }
    var qT;q.addEventListener('input',function(){clearTimeout(qT);qT=setTimeout(apply,90)});
    filt.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;cat=b.getAttribute('data-cat');$$('button',filt).forEach(function(x){x.classList.toggle('on',x===b)});apply()});
    function fromHash(){var id=decodeURIComponent((location.hash||'').slice(1)),el=id&&d.getElementById(id);if(el&&el.classList.contains('group')){setOpen(el,true);setTimeout(function(){el.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'})},60)}
      var p=new URLSearchParams(location.search);if(p.get('q')){q.value=p.get('q')}}
    fromHash();apply();w.addEventListener('hashchange',fromHash);
  }

  /* ---------- incoterms ---------- */
  var route=$('#route');
  if(route){
    var T={
      EXW:{to:0,txt:'<strong>Ex Works Istanbul.</strong> Our export price list is quoted EXW. Goods are made available at our facility in Istanbul; you or your forwarder arrange pick-up, export clearance and onward transport.'},
      FOB:{to:1,txt:'<strong>Free On Board, Istanbul port.</strong> We deliver the goods on board the vessel nominated by you and clear them for export. Freight, insurance and import formalities are on your side.'},
      CIF:{to:2,txt:'<strong>Cost, Insurance & Freight to your port.</strong> We book and pay sea freight and insurance to the named destination port. Risk passes once the goods are on board in Istanbul; import clearance is yours.'},
      DAP:{to:3,txt:'<strong>Delivered At Place.</strong> We deliver to a named place in your country, ready for unloading. Import duties, taxes and customs clearance remain with you as importer of record.'},
      DDP:{to:-1,txt:'<strong>DDP is not offered.</strong> Duty-paid delivery would make us importer of record in your country. A local importer clears goods faster and recovers import VAT — so DAP or CIF almost always costs you less.'}
    };
    var tabs=$$('.terms-tabs button',route),seller=$('.seller',route),nodes=$$('.node',route),copy=$('.term-copy p',route),big=$('.term-copy b',route),ship=$('.ship',route);
    var L=0;try{L=seller.getTotalLength()}catch(e){L=900}
    seller.style.strokeDasharray=L;
    var stops=[0,.33,.67,1];
    function set(k){
      var t=T[k];tabs.forEach(function(b){b.classList.toggle('on',b.getAttribute('data-t')===k)});
      var frac=t.to<0?0:stops[t.to];seller.style.strokeDashoffset=L*(1-frac);
      nodes.forEach(function(n,i){n.classList.toggle('s',t.to>=0&&i<=t.to)});
      if(ship){try{var pt=seller.getPointAtLength(L*Math.max(frac,0));ship.setAttribute('transform','translate('+pt.x+','+pt.y+')')}catch(e){}}
      copy.innerHTML=t.txt;big.textContent=k;
    }
    tabs.forEach(function(b){b.addEventListener('click',function(){set(b.getAttribute('data-t'))})});
    set('FOB');
  }

  /* ---------- timeline ---------- */
  var timelines=$$('.timeline');
  function tlUpdate(tl){
    var r=tl.getBoundingClientRect(),vh=w.innerHeight,p=Math.min(1,Math.max(0,(vh*0.75-r.top)/(r.height+vh*0.25)));
    tl.style.setProperty('--p',p.toFixed(3));
    var steps=$$('.step',tl);steps.forEach(function(s,i){s.classList.toggle('lit',p>=(i+0.2)/steps.length||reduce)});
  }

  /* ---------- private label demo ---------- */
  var lab=$('.label-demo');
  if(lab){
    var nameIn=$('input',lab),brand=$('.lb-brand',lab);
    nameIn.addEventListener('input',function(){brand.textContent=(nameIn.value.trim()||'YOUR BRAND').toUpperCase().slice(0,22)});
    $$('.lb-sw button',lab).forEach(function(b){b.addEventListener('click',function(){$$('.lb-sw button',lab).forEach(function(x){x.classList.toggle('on',x===b)});var c=b.getAttribute('data-c');brand.style.color=c;$('.lb-top',lab).style.borderColor=c})});
  }

  /* ---------- contact form ---------- */
  function renderPicked(){
    var box=$('#picked');if(!box)return;
    box.innerHTML=picked.length?picked.map(function(c){return '<span class="chip">'+esc(c)+' <button type="button" data-code="'+esc(c)+'" aria-label="Remove '+esc(c)+'"></button></span>'}).join(''):'<span class="hint">No codes picked yet — add them from the <a class="link" href="products.html">product range</a>, or describe what you need below.</span>';
  }
  var form=$('#enquiry');
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var v=function(n){var el=form.elements[n];return el?el.value.trim():''};
      if(!v('company')||!v('country')){toast('Please add your company and country');return}
      var body='Company: '+v('company')+'\nName: '+v('name')+'\nCountry / market: '+v('country')+'\nBusiness type: '+v('type')+'\nEmail: '+v('email')+'\n\nProducts of interest: '+(picked.length?picked.join(', '):'-')+'\n\n'+v('message')+'\n';
      var subj='Distributor enquiry - '+v('company')+' ('+v('country')+')';
      w.location.href='mailto:export@orlexglobal.com?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(body);
      toast('Opening your email app…');
    });
  }

  /* ---------- year ---------- */
  $$('[data-year]').forEach(function(el){el.textContent=new Date().getFullYear()});

  var ticking=false;function reqScroll(){if(!ticking){ticking=true;requestAnimationFrame(function(){ticking=false;onScroll()})}}
  w.addEventListener('scroll',reqScroll,{passive:true});w.addEventListener('resize',reqScroll);
  updateTray(false);onScroll();
})();
