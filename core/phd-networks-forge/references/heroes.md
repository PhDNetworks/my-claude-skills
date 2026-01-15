# Hero Sections

> Five premium hero variants for maximum impact

## Hero 1: Stacked Typography

Massive overlapping text creating bold visual impact. Best for creative agencies, portfolios, and bold brand statements.

```html
<!-- FORGE: Stacked Typography Hero | Theme: [THEME] | Mode: [MODE] -->
<style>
.forge-hero-stacked {
  min-height: 100vh;
  background: var(--bg-primary);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: var(--space-xl) var(--space-md);
  position: relative;
  overflow: hidden;
}

.forge-hero-stacked__words {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.forge-hero-stacked__word {
  font-family: var(--font-display);
  font-size: clamp(4rem, 18vw, 16rem);
  line-height: 0.85;
  color: var(--accent-secondary);
  text-transform: uppercase;
  letter-spacing: -0.02em;
  opacity: 0;
  transform: translateY(100px);
}

.forge-hero-stacked__word:nth-child(2) {
  color: var(--accent-primary);
  margin-left: 5%;
}

.forge-hero-stacked__word:nth-child(3) {
  color: var(--text-primary);
  margin-left: 10%;
}

.forge-hero-stacked__tagline {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  color: var(--text-secondary);
  margin-top: var(--space-lg);
  max-width: 500px;
  opacity: 0;
}

.forge-hero-stacked__cta {
  margin-top: var(--space-md);
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: var(--accent-primary);
  color: var(--text-inverse);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  text-decoration: none;
  border-radius: var(--radius-sm);
  opacity: 0;
  transition: var(--transition-base);
}

.forge-hero-stacked__cta:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}

.forge-hero-stacked__scroll {
  position: absolute;
  bottom: var(--space-md);
  left: 50%;
  transform: translateX(-50%);
  color: var(--text-muted);
  font-size: var(--text-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-xs);
  opacity: 0;
}

.forge-hero-stacked__scroll-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(to bottom, var(--text-muted), transparent);
}

@media (max-width: 768px) {
  .forge-hero-stacked__word:nth-child(2),
  .forge-hero-stacked__word:nth-child(3) {
    margin-left: 0;
  }
}
</style>

<section class="forge-hero-stacked">
  <div class="forge-hero-stacked__words">
    <div class="forge-hero-stacked__word"><span>INNOVATE</span></div>
    <div class="forge-hero-stacked__word"><span>CREATE</span></div>
    <div class="forge-hero-stacked__word"><span>DELIVER</span></div>
  </div>
  <p class="forge-hero-stacked__tagline">
    Premium digital experiences that transform businesses and captivate audiences.
  </p>
  <a href="#contact" class="forge-hero-stacked__cta magnetic-btn">
    Start Your Project
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M5 12h14M12 5l7 7-7 7"/>
    </svg>
  </a>
  <div class="forge-hero-stacked__scroll">
    <span>Scroll</span>
    <div class="forge-hero-stacked__scroll-line"></div>
  </div>
</section>

<script>
(function() {
  gsap.registerPlugin(ScrollTrigger);

  const words = document.querySelectorAll('.forge-hero-stacked__word');
  const tagline = document.querySelector('.forge-hero-stacked__tagline');
  const cta = document.querySelector('.forge-hero-stacked__cta');
  const scroll = document.querySelector('.forge-hero-stacked__scroll');

  const tl = gsap.timeline({ delay: 0.5 });

  tl.to(words, {
    opacity: 1,
    y: 0,
    duration: 1,
    stagger: 0.15,
    ease: 'power4.out'
  })
  .to(tagline, {
    opacity: 1,
    duration: 0.8,
    ease: 'power3.out'
  }, '-=0.3')
  .to(cta, {
    opacity: 1,
    duration: 0.6,
    ease: 'power3.out'
  }, '-=0.4')
  .to(scroll, {
    opacity: 1,
    duration: 0.6,
    ease: 'power3.out'
  }, '-=0.2');
})();
</script>
<!-- END FORGE COMPONENT -->
```

---

## Hero 2: Split Hero

50/50 layout with text and visual element. Best for product launches, services, and balanced messaging.

```html
<!-- FORGE: Split Hero | Theme: [THEME] | Mode: [MODE] -->
<style>
.forge-hero-split {
  min-height: 100vh;
  background: var(--bg-primary);
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: var(--space-xl);
  padding: var(--space-xl);
}

.forge-hero-split__content {
  max-width: 600px;
}

.forge-hero-split__badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--space-sm);
  background: var(--accent-muted);
  color: var(--accent-primary);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  border-radius: var(--radius-full);
  margin-bottom: var(--space-md);
  opacity: 0;
  transform: translateY(20px);
}

.forge-hero-split__title {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  line-height: 1.1;
  color: var(--text-primary);
  margin-bottom: var(--space-md);
  opacity: 0;
  transform: translateY(40px);
}

.forge-hero-split__title span {
  color: var(--accent-primary);
}

.forge-hero-split__description {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: var(--space-lg);
  opacity: 0;
  transform: translateY(30px);
}

.forge-hero-split__actions {
  display: flex;
  gap: var(--space-sm);
  flex-wrap: wrap;
  opacity: 0;
  transform: translateY(20px);
}

.forge-hero-split__btn-primary {
  padding: var(--space-sm) var(--space-lg);
  background: var(--accent-primary);
  color: var(--text-inverse);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: var(--transition-base);
}

.forge-hero-split__btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}

.forge-hero-split__btn-secondary {
  padding: var(--space-sm) var(--space-lg);
  background: transparent;
  color: var(--text-primary);
  font-family: var(--font-body);
  font-weight: var(--weight-medium);
  text-decoration: none;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  transition: var(--transition-base);
}

.forge-hero-split__btn-secondary:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.forge-hero-split__visual {
  position: relative;
  height: 100%;
  min-height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.forge-hero-split__image {
  width: 100%;
  height: 80%;
  object-fit: cover;
  border-radius: var(--radius-lg);
  opacity: 0;
  transform: scale(0.95);
}

.forge-hero-split__float {
  position: absolute;
  background: var(--bg-elevated);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  opacity: 0;
}

.forge-hero-split__float--stats {
  bottom: 10%;
  left: -10%;
}

.forge-hero-split__float--rating {
  top: 10%;
  right: -5%;
}

@media (max-width: 1024px) {
  .forge-hero-split {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .forge-hero-split__content {
    max-width: 100%;
  }

  .forge-hero-split__actions {
    justify-content: center;
  }

  .forge-hero-split__visual {
    min-height: 400px;
  }

  .forge-hero-split__float {
    display: none;
  }
}
</style>

<section class="forge-hero-split">
  <div class="forge-hero-split__content">
    <div class="forge-hero-split__badge">
      <span>New Release</span>
    </div>
    <h1 class="forge-hero-split__title">
      Transform Your <span>Digital Presence</span>
    </h1>
    <p class="forge-hero-split__description">
      We create stunning websites and digital experiences that convert visitors into customers. Premium quality, exceptional results.
    </p>
    <div class="forge-hero-split__actions">
      <a href="#contact" class="forge-hero-split__btn-primary magnetic-btn">Get Started</a>
      <a href="#work" class="forge-hero-split__btn-secondary">View Our Work</a>
    </div>
  </div>
  <div class="forge-hero-split__visual">
    <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800" alt="Digital Experience" class="forge-hero-split__image">
    <div class="forge-hero-split__float forge-hero-split__float--stats">
      <div style="font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--accent-primary);">500+</div>
      <div style="font-size: var(--text-sm); color: var(--text-secondary);">Projects Delivered</div>
    </div>
    <div class="forge-hero-split__float forge-hero-split__float--rating">
      <div style="color: var(--accent-primary);">★★★★★</div>
      <div style="font-size: var(--text-sm); color: var(--text-secondary);">5.0 Rating</div>
    </div>
  </div>
</section>

<script>
(function() {
  gsap.registerPlugin(ScrollTrigger);

  const tl = gsap.timeline({ delay: 0.3 });

  tl.to('.forge-hero-split__badge', { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' })
    .to('.forge-hero-split__title', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '-=0.3')
    .to('.forge-hero-split__description', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, '-=0.4')
    .to('.forge-hero-split__actions', { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }, '-=0.3')
    .to('.forge-hero-split__image', { opacity: 1, scale: 1, duration: 1, ease: 'power3.out' }, '-=0.8')
    .to('.forge-hero-split__float', { opacity: 1, duration: 0.6, stagger: 0.2, ease: 'power3.out' }, '-=0.4');
})();
</script>
<!-- END FORGE COMPONENT -->
```

---

## Hero 3: Video Background

Full-bleed video with overlay for lifestyle brands and immersive experiences.

```html
<!-- FORGE: Video Background Hero | Theme: [THEME] | Mode: [MODE] -->
<style>
.forge-hero-video {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.forge-hero-video__bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

.forge-hero-video__overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(10, 10, 10, 0.7) 0%,
    rgba(10, 10, 10, 0.5) 50%,
    rgba(10, 10, 10, 0.8) 100%
  );
  z-index: 2;
}

.forge-hero-video__content {
  position: relative;
  z-index: 3;
  text-align: center;
  max-width: 900px;
  padding: var(--space-xl);
}

.forge-hero-video__subtitle {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--accent-primary);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  margin-bottom: var(--space-sm);
  opacity: 0;
  transform: translateY(20px);
}

.forge-hero-video__title {
  font-family: var(--font-display);
  font-size: clamp(3rem, 10vw, 7rem);
  line-height: 1;
  color: var(--text-primary);
  margin-bottom: var(--space-md);
  opacity: 0;
  transform: translateY(40px);
}

.forge-hero-video__description {
  font-family: var(--font-body);
  font-size: var(--text-xl);
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto var(--space-lg);
  opacity: 0;
  transform: translateY(30px);
}

.forge-hero-video__cta {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-xl);
  background: var(--accent-primary);
  color: var(--text-inverse);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  font-size: var(--text-lg);
  text-decoration: none;
  border-radius: var(--radius-sm);
  opacity: 0;
  transform: translateY(20px);
  transition: var(--transition-base);
}

.forge-hero-video__cta:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}

.forge-hero-video__play {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 2px solid var(--accent-primary);
  border-radius: 50%;
  color: var(--accent-primary);
  margin-top: var(--space-xl);
  cursor: pointer;
  opacity: 0;
  transition: var(--transition-base);
}

.forge-hero-video__play:hover {
  background: var(--accent-primary);
  color: var(--text-inverse);
  transform: scale(1.1);
}

.forge-hero-video__scroll {
  position: absolute;
  bottom: var(--space-lg);
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  color: var(--text-muted);
  font-size: var(--text-sm);
  opacity: 0;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(10px); }
}

@media (max-width: 768px) {
  .forge-hero-video__content {
    padding: var(--space-md);
  }
}
</style>

<section class="forge-hero-video">
  <video class="forge-hero-video__bg" autoplay muted loop playsinline>
    <source src="YOUR_VIDEO_URL.mp4" type="video/mp4">
  </video>
  <div class="forge-hero-video__overlay"></div>
  <div class="forge-hero-video__content">
    <p class="forge-hero-video__subtitle">Welcome to the Future</p>
    <h1 class="forge-hero-video__title">EXPERIENCE EXCELLENCE</h1>
    <p class="forge-hero-video__description">
      Immerse yourself in a world of premium quality and exceptional craftsmanship.
    </p>
    <a href="#discover" class="forge-hero-video__cta magnetic-btn">
      Discover More
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M5 12h14M12 5l7 7-7 7"/>
      </svg>
    </a>
    <div class="forge-hero-video__play">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
        <polygon points="5 3 19 12 5 21 5 3"/>
      </svg>
    </div>
  </div>
  <div class="forge-hero-video__scroll">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 5v14M5 12l7 7 7-7"/>
    </svg>
  </div>
</section>

<script>
(function() {
  gsap.registerPlugin(ScrollTrigger);

  const tl = gsap.timeline({ delay: 0.5 });

  tl.to('.forge-hero-video__subtitle', { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' })
    .to('.forge-hero-video__title', { opacity: 1, y: 0, duration: 1, ease: 'power4.out' }, '-=0.3')
    .to('.forge-hero-video__description', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '-=0.5')
    .to('.forge-hero-video__cta', { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }, '-=0.4')
    .to('.forge-hero-video__play', { opacity: 1, duration: 0.6, ease: 'power3.out' }, '-=0.3')
    .to('.forge-hero-video__scroll', { opacity: 1, duration: 0.6, ease: 'power3.out' }, '-=0.2');
})();
</script>
<!-- END FORGE COMPONENT -->
```

---

## Hero 4: Particle/3D Hero

Three.js interactive particle field for tech companies and innovation-focused brands.

```html
<!-- FORGE: Particle Hero | Theme: [THEME] | Mode: [MODE] -->
<style>
.forge-hero-particle {
  position: relative;
  min-height: 100vh;
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.forge-hero-particle__canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.forge-hero-particle__content {
  position: relative;
  z-index: 2;
  text-align: center;
  max-width: 800px;
  padding: var(--space-xl);
}

.forge-hero-particle__tag {
  display: inline-block;
  padding: var(--space-xs) var(--space-md);
  background: var(--accent-muted);
  color: var(--accent-primary);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  border-radius: var(--radius-full);
  margin-bottom: var(--space-md);
  opacity: 0;
}

.forge-hero-particle__title {
  font-family: var(--font-display);
  font-size: clamp(2.5rem, 8vw, 5rem);
  line-height: 1.1;
  color: var(--text-primary);
  margin-bottom: var(--space-md);
  opacity: 0;
  transform: translateY(30px);
}

.forge-hero-particle__title span {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.forge-hero-particle__description {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto var(--space-lg);
  line-height: 1.7;
  opacity: 0;
  transform: translateY(20px);
}

.forge-hero-particle__actions {
  display: flex;
  justify-content: center;
  gap: var(--space-sm);
  opacity: 0;
  transform: translateY(20px);
}

.forge-hero-particle__btn {
  padding: var(--space-sm) var(--space-lg);
  background: var(--accent-primary);
  color: var(--bg-primary);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: var(--transition-base);
}

.forge-hero-particle__btn:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(88, 166, 255, 0.3);
}

.forge-hero-particle__btn--outline {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-default);
}

.forge-hero-particle__btn--outline:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  box-shadow: none;
}
</style>

<section class="forge-hero-particle">
  <canvas class="forge-hero-particle__canvas" id="particle-canvas"></canvas>
  <div class="forge-hero-particle__content">
    <span class="forge-hero-particle__tag">Next Generation Platform</span>
    <h1 class="forge-hero-particle__title">
      Build the <span>Future</span> Today
    </h1>
    <p class="forge-hero-particle__description">
      Harness the power of cutting-edge technology to transform your business.
      Fast, secure, and infinitely scalable.
    </p>
    <div class="forge-hero-particle__actions">
      <a href="#start" class="forge-hero-particle__btn magnetic-btn">Get Started Free</a>
      <a href="#demo" class="forge-hero-particle__btn forge-hero-particle__btn--outline">Watch Demo</a>
    </div>
  </div>
</section>

<script>
(function() {
  // Three.js Particle System
  const canvas = document.getElementById('particle-canvas');
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });

  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // Particles
  const particleCount = 1500;
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);

  const accentColor = new THREE.Color(0x58A6FF);
  const secondaryColor = new THREE.Color(0xF78166);

  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 20;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 20;

    const color = Math.random() > 0.5 ? accentColor : secondaryColor;
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const material = new THREE.PointsMaterial({
    size: 0.05,
    vertexColors: true,
    transparent: true,
    opacity: 0.8
  });

  const particles = new THREE.Points(geometry, material);
  scene.add(particles);

  camera.position.z = 5;

  // Mouse interaction
  let mouseX = 0, mouseY = 0;
  document.addEventListener('mousemove', (e) => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  // Animation
  function animate() {
    requestAnimationFrame(animate);
    particles.rotation.x += 0.001;
    particles.rotation.y += 0.002;
    particles.rotation.x += mouseY * 0.01;
    particles.rotation.y += mouseX * 0.01;
    renderer.render(scene, camera);
  }
  animate();

  // Resize
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // GSAP animations
  gsap.registerPlugin(ScrollTrigger);
  const tl = gsap.timeline({ delay: 0.5 });

  tl.to('.forge-hero-particle__tag', { opacity: 1, duration: 0.6, ease: 'power3.out' })
    .to('.forge-hero-particle__title', { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }, '-=0.3')
    .to('.forge-hero-particle__description', { opacity: 1, y: 0, duration: 0.7, ease: 'power3.out' }, '-=0.4')
    .to('.forge-hero-particle__actions', { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out' }, '-=0.3');
})();
</script>
<!-- END FORGE COMPONENT -->
```

---

## Hero 5: Minimal Statement

Elegant single headline for luxury and editorial brands.

```html
<!-- FORGE: Minimal Statement Hero | Theme: [THEME] | Mode: [MODE] -->
<style>
.forge-hero-minimal {
  min-height: 100vh;
  background: var(--bg-primary);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: var(--space-xl);
  position: relative;
}

.forge-hero-minimal__logo {
  width: 60px;
  height: 60px;
  margin-bottom: var(--space-xl);
  opacity: 0;
}

.forge-hero-minimal__title {
  font-family: var(--font-display);
  font-size: clamp(3rem, 12vw, 10rem);
  line-height: 0.9;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  margin-bottom: var(--space-md);
}

.forge-hero-minimal__title .char {
  display: inline-block;
  opacity: 0;
  transform: translateY(100%);
}

.forge-hero-minimal__line {
  width: 60px;
  height: 2px;
  background: var(--accent-primary);
  margin: var(--space-md) auto;
  transform: scaleX(0);
}

.forge-hero-minimal__tagline {
  font-family: var(--font-body);
  font-size: var(--text-xl);
  color: var(--text-secondary);
  font-weight: var(--weight-light);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  opacity: 0;
  transform: translateY(20px);
}

.forge-hero-minimal__cta {
  margin-top: var(--space-xl);
  padding: var(--space-sm) var(--space-xl);
  background: transparent;
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.15em;
  text-decoration: none;
  border: 1px solid var(--border-default);
  opacity: 0;
  transition: var(--transition-base);
}

.forge-hero-minimal__cta:hover {
  background: var(--text-primary);
  color: var(--bg-primary);
  border-color: var(--text-primary);
}

.forge-hero-minimal__scroll {
  position: absolute;
  bottom: var(--space-lg);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  color: var(--text-muted);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.2em;
  opacity: 0;
}

.forge-hero-minimal__scroll-line {
  width: 1px;
  height: 50px;
  background: linear-gradient(to bottom, var(--accent-primary), transparent);
}
</style>

<section class="forge-hero-minimal">
  <img src="logo.svg" alt="Logo" class="forge-hero-minimal__logo">
  <h1 class="forge-hero-minimal__title">EXCELLENCE</h1>
  <div class="forge-hero-minimal__line"></div>
  <p class="forge-hero-minimal__tagline">Crafted with precision</p>
  <a href="#discover" class="forge-hero-minimal__cta magnetic-btn">Explore Collection</a>
  <div class="forge-hero-minimal__scroll">
    <span>Scroll</span>
    <div class="forge-hero-minimal__scroll-line"></div>
  </div>
</section>

<script>
(function() {
  gsap.registerPlugin(ScrollTrigger);

  // Split title into characters
  const title = document.querySelector('.forge-hero-minimal__title');
  const text = title.textContent;
  title.innerHTML = text.split('').map(char =>
    `<span class="char">${char}</span>`
  ).join('');

  const tl = gsap.timeline({ delay: 0.8 });

  tl.to('.forge-hero-minimal__logo', { opacity: 1, duration: 0.8, ease: 'power3.out' })
    .to('.forge-hero-minimal__title .char', {
      opacity: 1,
      y: 0,
      duration: 0.8,
      stagger: 0.05,
      ease: 'power4.out'
    }, '-=0.4')
    .to('.forge-hero-minimal__line', {
      scaleX: 1,
      duration: 0.8,
      ease: 'power3.inOut'
    }, '-=0.3')
    .to('.forge-hero-minimal__tagline', {
      opacity: 1,
      y: 0,
      duration: 0.6,
      ease: 'power3.out'
    }, '-=0.4')
    .to('.forge-hero-minimal__cta', { opacity: 1, duration: 0.6, ease: 'power3.out' }, '-=0.2')
    .to('.forge-hero-minimal__scroll', { opacity: 1, duration: 0.6, ease: 'power3.out' }, '-=0.2');
})();
</script>
<!-- END FORGE COMPONENT -->
```

---

## Hero Selection Guide

| Hero Type | Best For | Complexity | Impact |
|-----------|----------|------------|--------|
| Stacked Typography | Creative agencies, Bold statements | Medium | High |
| Split Hero | Products, Services, Balanced messaging | Low | Medium-High |
| Video Background | Lifestyle, Events, Immersive brands | Medium | High |
| Particle/3D | Tech, SaaS, Innovation | High | Very High |
| Minimal Statement | Luxury, Editorial, Minimalist | Low | Medium |
