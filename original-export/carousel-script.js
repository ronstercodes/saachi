var items = document.querySelectorAll('#isl1');
  for (var i = 0, len = items.length; i < len; i++) {
    (function(){
      const slides = this.querySelectorAll('.slide');
      const navContainer = this.querySelector('.carousel-nav');
      if (slides.length === 0) return;
      let index = 0;
      // Initialize navigation bubbles
      if (!navContainer) {
        const nav = document.createElement('div');
        nav.className = 'carousel-nav';
        slides.forEach((_, i) => {
          const bubble = document.createElement('div');
          bubble.className = 'nav-bubble';
          bubble.dataset.index = i;
          nav.appendChild(bubble);
        }
                      );
        this.appendChild(nav);
      }
      const updateBubbles = () => {
        const bubbles = this.querySelectorAll('.nav-bubble');
        bubbles.forEach((b, i) => {
          b.classList.toggle('active', i === index);
        }
                       );
      };
      const showSlide = (newIndex) => {
        slides.forEach((s) => s.classList.remove('active'));
        slides[newIndex].classList.add('active');
        index = newIndex;
        updateBubbles();
      };
      // Initialize first slide
      showSlide(0);
      // Handle bubble clicks
      this.querySelectorAll('.nav-bubble').forEach((bubble) => {
        bubble.addEventListener('click', () => {
          const newIndex = parseInt(bubble.dataset.index);
          showSlide(newIndex);
        }
                               );
      }
                                                  );
    }
     .bind(items[i]))();
  }
