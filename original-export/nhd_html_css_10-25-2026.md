**HTML**  
\<body\>  
  \<div class="auto-nav"\>\[\*\*\*smart-nav\*\*\*\]  
  \</div\>  
  \<div class="container c1363"\>  
	\<div\>  
	\</div\>  
	\<h1 id="itsa"\>  
	  \<strong\>A Fatal Mix-Up:\</strong\>  
	\</h1\>  
	\<h2 id="i2k2s"\>The 1901 Diphtheria Tragedy and America’s First Leap into Drug Regulation  
	\</h2\>  
  \</div\>  
  \<div id="isl1" class="carousel"\>  
	\<img src="../90886777/uploaded/Screenshot\_2026-10-17\_at\_1\_49\_31\_PM\_1.png" alt="Slide 1" class="slide"/\>  
	\<img src="../90886777/uploaded/Screenshot\_2026-10-17\_at\_1\_49\_37\_PM.png" alt="Slide 2" class="slide"/\>  
	\<img src="../90886777/uploaded/Screenshot\_2026-10-17\_at\_1\_49\_43\_PM.png" alt="Slide 1" class="slide"/\>  
	\<img src="../90886777/uploaded/Screenshot\_2026-10-18\_at\_2\_22\_49\_PM.png" alt="Slide 1" class="slide"/\>  
  \</div\>  
  \<div id="ihq6k"\>  
	\<p\>In 1901, medicine intended to save children became deadly. The tragedy shocked the nation and changed\&nbsp;how America regulates medical products.  
	\</p\>​​​​​​​  
  \</div\>  
  \<div id="ipwhb"\>  
	\<p\>  
	  \<strong\>13 Children died.\<br\>\<br\>America changed forever.\</strong\>  
	\</p\>  
  \</div\>  
  \<a href="thesis\_4" id="irtjk"\>Click here to see Thesis\</a\>  
\</body\>  
\<script\>var items \= document.querySelectorAll('\#isl1');  
  for (var i \= 0, len \= items.length; i \< len; i++) {  
	(function(){  
	  const slides \= this.querySelectorAll('.slide');  
	  const navContainer \= this.querySelector('.carousel-nav');  
	  if (slides.length \=== 0\) return;  
	  let index \= 0;  
	  // Initialize navigation bubbles  
	  if (\!navContainer) {  
		const nav \= document.createElement('div');  
		nav.className \= 'carousel-nav';  
		slides.forEach((\_, i) \=\> {  
		  const bubble \= document.createElement('div');  
		  bubble.className \= 'nav-bubble';  
		  bubble.dataset.index \= i;  
		  nav.appendChild(bubble);  
		}  
					  );  
		this.appendChild(nav);  
	  }  
	  const updateBubbles \= () \=\> {  
		const bubbles \= this.querySelectorAll('.nav-bubble');  
		bubbles.forEach((b, i) \=\> {  
		  b.classList.toggle('active', i \=== index);  
		}  
					   );  
	  };  
	  const showSlide \= (newIndex) \=\> {  
		slides.forEach((s) \=\> s.classList.remove('active'));  
		slides\[newIndex\].classList.add('active');  
		index \= newIndex;  
		updateBubbles();  
	  };  
	  // Initialize first slide  
	  showSlide(0);  
	  // Handle bubble clicks  
	  this.querySelectorAll('.nav-bubble').forEach((bubble) \=\> {  
		bubble.addEventListener('click', () \=\> {  
		  const newIndex \= parseInt(bubble.dataset.index);  
		  showSlide(newIndex);  
		}  
							   );  
	  }  
												  );  
	}  
	 .bind(items\[i\]))();  
  }  
\</script\>  
**CSS**  
body{  
  background-color:\#c8d5dc;  
}  
.c1363{  
  min-height:12px;  
}  
\#itsa{  
  font-family:Georgia, serif;  
  text-align:center;  
  border:\#243e50;  
  background-color:\#243e50;  
  color:\#faf6ed;  
  font-size:50px;  
}  
.slide{  
  background-color:\#faf6ed;  
}  
.container.c1363{  
  background-color:\#faf6ed;  
}  
.auto-nav{  
  background-color:\#c8d5dc;  
  font-family:Georgia, serif;  
}  
\#ihq6k{  
  padding:10px;  
  font-family:Georgia, serif;  
  text-align:center;  
  background-color:\#faf6ed;  
  font-size:18px;  
}  
\#ipwhb{  
  padding:10px;  
  text-align:center;  
  font-family:Georgia, serif;  
  font-size:25px;  
  background-color:\#faf6ed;  
  color:\#783b40;  
}  
\#i2k2s{  
  font-family:Georgia, serif;  
  text-align:center;  
  color:\#faf6ed;  
  background-color:\#243e50;  
  font-size:25px;  
}  
\#irtjk{  
  display:inline-block;  
  padding:.5em 1em;  
  min-height:50px;  
  min-width:50px;  
  background-color:\#243e50;  
  color:\#faf6ed;  
  width:1110px;  
  text-align:center;  
  font-size:28px;  
  font-family:Georgia, serif;  
}

