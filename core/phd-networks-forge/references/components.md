# Components

> Premium UI component library for all themes

## Feature Cards

### Numbered Feature Card
```html
<!-- FORGE: Feature Card Numbered -->
<style>
.forge-feature-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  transition: var(--transition-base);
}

.forge-feature-card:hover {
  border-color: var(--accent-primary);
  transform: translateY(-4px);
}

.forge-feature-card__number {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  color: var(--accent-primary);
  opacity: 0.5;
  line-height: 1;
  margin-bottom: var(--space-sm);
}

.forge-feature-card__title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}

.forge-feature-card__description {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>

<div class="forge-feature-card">
  <span class="forge-feature-card__number">01</span>
  <h3 class="forge-feature-card__title">Feature Title</h3>
  <p class="forge-feature-card__description">
    Description of this amazing feature and how it benefits the user.
  </p>
</div>
```

### Icon Feature Card
```html
<!-- FORGE: Feature Card Icon -->
<style>
.forge-feature-icon {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  text-align: center;
  transition: var(--transition-base);
}

.forge-feature-icon:hover {
  background: var(--bg-tertiary);
}

.forge-feature-icon__icon {
  width: 64px;
  height: 64px;
  background: var(--accent-muted);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--space-md);
  color: var(--accent-primary);
}

.forge-feature-icon__title {
  font-family: var(--font-body);
  font-size: var(--text-xl);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-xs);
}

.forge-feature-icon__description {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--text-secondary);
}
</style>

<div class="forge-feature-icon">
  <div class="forge-feature-icon__icon">
    <svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
    </svg>
  </div>
  <h3 class="forge-feature-icon__title">Feature Name</h3>
  <p class="forge-feature-icon__description">Brief description of this feature.</p>
</div>
```

---

## Pricing Tables

### Three-Tier Pricing
```html
<!-- FORGE: Pricing Table -->
<style>
.forge-pricing {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-md);
  padding: var(--space-xl) 0;
}

.forge-pricing__card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  position: relative;
  transition: var(--transition-base);
}

.forge-pricing__card--featured {
  border-color: var(--accent-primary);
  transform: scale(1.05);
}

.forge-pricing__badge {
  position: absolute;
  top: calc(-1 * var(--space-xs));
  left: 50%;
  transform: translateX(-50%);
  background: var(--accent-primary);
  color: var(--text-inverse);
  padding: var(--space-xs) var(--space-sm);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  border-radius: var(--radius-full);
  text-transform: uppercase;
}

.forge-pricing__name {
  font-family: var(--font-body);
  font-size: var(--text-lg);
  color: var(--text-secondary);
  margin-bottom: var(--space-sm);
}

.forge-pricing__price {
  font-family: var(--font-display);
  font-size: var(--text-5xl);
  color: var(--text-primary);
  line-height: 1;
}

.forge-pricing__price span {
  font-size: var(--text-lg);
  color: var(--text-muted);
}

.forge-pricing__description {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin: var(--space-md) 0;
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--border-subtle);
}

.forge-pricing__features {
  list-style: none;
  padding: 0;
  margin: var(--space-md) 0;
}

.forge-pricing__feature {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  font-family: var(--font-body);
  color: var(--text-secondary);
  padding: var(--space-xs) 0;
}

.forge-pricing__feature svg {
  color: var(--accent-primary);
  flex-shrink: 0;
}

.forge-pricing__cta {
  display: block;
  width: 100%;
  padding: var(--space-sm);
  background: var(--accent-primary);
  color: var(--text-inverse);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  text-align: center;
  text-decoration: none;
  border-radius: var(--radius-sm);
  margin-top: var(--space-md);
  transition: var(--transition-base);
}

.forge-pricing__cta:hover {
  background: var(--accent-hover);
}

.forge-pricing__card:not(.forge-pricing__card--featured) .forge-pricing__cta {
  background: transparent;
  border: 1px solid var(--border-default);
  color: var(--text-primary);
}

.forge-pricing__card:not(.forge-pricing__card--featured) .forge-pricing__cta:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}
</style>

<div class="forge-pricing">
  <div class="forge-pricing__card">
    <h3 class="forge-pricing__name">Starter</h3>
    <div class="forge-pricing__price">£29<span>/mo</span></div>
    <p class="forge-pricing__description">Perfect for individuals getting started.</p>
    <ul class="forge-pricing__features">
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Up to 5 projects
      </li>
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Basic analytics
      </li>
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Email support
      </li>
    </ul>
    <a href="#" class="forge-pricing__cta magnetic-btn">Get Started</a>
  </div>

  <div class="forge-pricing__card forge-pricing__card--featured">
    <span class="forge-pricing__badge">Most Popular</span>
    <h3 class="forge-pricing__name">Professional</h3>
    <div class="forge-pricing__price">£79<span>/mo</span></div>
    <p class="forge-pricing__description">Best for growing businesses.</p>
    <ul class="forge-pricing__features">
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Unlimited projects
      </li>
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Advanced analytics
      </li>
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Priority support
      </li>
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Custom integrations
      </li>
    </ul>
    <a href="#" class="forge-pricing__cta magnetic-btn">Get Started</a>
  </div>

  <div class="forge-pricing__card">
    <h3 class="forge-pricing__name">Enterprise</h3>
    <div class="forge-pricing__price">£199<span>/mo</span></div>
    <p class="forge-pricing__description">For large teams and organizations.</p>
    <ul class="forge-pricing__features">
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Everything in Pro
      </li>
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Dedicated account manager
      </li>
      <li class="forge-pricing__feature">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
        Custom SLA
      </li>
    </ul>
    <a href="#" class="forge-pricing__cta magnetic-btn">Contact Sales</a>
  </div>
</div>
```

---

## Testimonials

### Quote Testimonial
```html
<!-- FORGE: Testimonial Quote -->
<style>
.forge-testimonial {
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  position: relative;
}

.forge-testimonial__quote-icon {
  position: absolute;
  top: var(--space-md);
  left: var(--space-md);
  font-family: var(--font-display);
  font-size: 6rem;
  color: var(--accent-primary);
  opacity: 0.2;
  line-height: 1;
}

.forge-testimonial__content {
  font-family: var(--font-body);
  font-size: var(--text-xl);
  color: var(--text-primary);
  line-height: 1.7;
  font-style: italic;
  margin-bottom: var(--space-lg);
  position: relative;
  z-index: 1;
}

.forge-testimonial__author {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.forge-testimonial__avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
}

.forge-testimonial__name {
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}

.forge-testimonial__role {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.forge-testimonial__rating {
  color: var(--accent-primary);
  margin-top: var(--space-xs);
}
</style>

<div class="forge-testimonial">
  <span class="forge-testimonial__quote-icon">"</span>
  <p class="forge-testimonial__content">
    Working with this team has been transformative for our business. The quality of work and attention to detail is exceptional.
  </p>
  <div class="forge-testimonial__author">
    <img src="avatar.jpg" alt="John Smith" class="forge-testimonial__avatar">
    <div>
      <div class="forge-testimonial__name">John Smith</div>
      <div class="forge-testimonial__role">CEO, Tech Company</div>
      <div class="forge-testimonial__rating">★★★★★</div>
    </div>
  </div>
</div>
```

---

## Social Proof

### Logo Marquee
```html
<!-- FORGE: Logo Marquee -->
<style>
.forge-logos {
  overflow: hidden;
  padding: var(--space-lg) 0;
  background: var(--bg-secondary);
}

.forge-logos__track {
  display: flex;
  animation: scroll 30s linear infinite;
}

.forge-logos__item {
  flex-shrink: 0;
  padding: 0 var(--space-xl);
  opacity: 0.5;
  transition: opacity 0.3s ease;
}

.forge-logos__item:hover {
  opacity: 1;
}

.forge-logos__item img {
  height: 40px;
  width: auto;
  filter: grayscale(100%);
  transition: filter 0.3s ease;
}

.forge-logos__item:hover img {
  filter: grayscale(0%);
}

@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>

<div class="forge-logos">
  <div class="forge-logos__track">
    <!-- Duplicate items for seamless loop -->
    <div class="forge-logos__item"><img src="logo1.svg" alt="Company 1"></div>
    <div class="forge-logos__item"><img src="logo2.svg" alt="Company 2"></div>
    <div class="forge-logos__item"><img src="logo3.svg" alt="Company 3"></div>
    <div class="forge-logos__item"><img src="logo4.svg" alt="Company 4"></div>
    <div class="forge-logos__item"><img src="logo5.svg" alt="Company 5"></div>
    <!-- Repeat for seamless loop -->
    <div class="forge-logos__item"><img src="logo1.svg" alt="Company 1"></div>
    <div class="forge-logos__item"><img src="logo2.svg" alt="Company 2"></div>
    <div class="forge-logos__item"><img src="logo3.svg" alt="Company 3"></div>
    <div class="forge-logos__item"><img src="logo4.svg" alt="Company 4"></div>
    <div class="forge-logos__item"><img src="logo5.svg" alt="Company 5"></div>
  </div>
</div>
```

### Stats Counter
```html
<!-- FORGE: Stats Counter -->
<style>
.forge-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-lg);
  padding: var(--space-xl) 0;
}

.forge-stat {
  text-align: center;
}

.forge-stat__number {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8vw, 5rem);
  color: var(--accent-primary);
  line-height: 1;
}

.forge-stat__label {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--text-secondary);
  margin-top: var(--space-xs);
}
</style>

<div class="forge-stats">
  <div class="forge-stat">
    <div class="forge-stat__number" data-target="500" data-suffix="+">0</div>
    <div class="forge-stat__label">Projects Completed</div>
  </div>
  <div class="forge-stat">
    <div class="forge-stat__number" data-target="98" data-suffix="%">0</div>
    <div class="forge-stat__label">Client Satisfaction</div>
  </div>
  <div class="forge-stat">
    <div class="forge-stat__number" data-target="12" data-suffix="">0</div>
    <div class="forge-stat__label">Years Experience</div>
  </div>
  <div class="forge-stat">
    <div class="forge-stat__number" data-target="24" data-suffix="/7">0</div>
    <div class="forge-stat__label">Support Available</div>
  </div>
</div>

<script>
// Counter animation (see animations.md for full implementation)
</script>
```

---

## Forms

### Waitlist Form
```html
<!-- FORGE: Waitlist Form -->
<style>
.forge-waitlist {
  max-width: 500px;
  margin: 0 auto;
  text-align: center;
}

.forge-waitlist__title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}

.forge-waitlist__description {
  font-family: var(--font-body);
  color: var(--text-secondary);
  margin-bottom: var(--space-lg);
}

.forge-waitlist__form {
  display: flex;
  gap: var(--space-xs);
}

.forge-waitlist__input {
  flex: 1;
  padding: var(--space-sm) var(--space-md);
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-family: var(--font-body);
  font-size: var(--text-base);
  transition: var(--transition-base);
}

.forge-waitlist__input:focus {
  outline: none;
  border-color: var(--accent-primary);
}

.forge-waitlist__input::placeholder {
  color: var(--text-muted);
}

.forge-waitlist__btn {
  padding: var(--space-sm) var(--space-lg);
  background: var(--accent-primary);
  color: var(--text-inverse);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition: var(--transition-base);
}

.forge-waitlist__btn:hover {
  background: var(--accent-hover);
}

.forge-waitlist__note {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin-top: var(--space-sm);
}

@media (max-width: 640px) {
  .forge-waitlist__form {
    flex-direction: column;
  }
}
</style>

<div class="forge-waitlist">
  <h2 class="forge-waitlist__title">Join the Waitlist</h2>
  <p class="forge-waitlist__description">Be the first to know when we launch.</p>
  <form class="forge-waitlist__form">
    <input type="email" class="forge-waitlist__input" placeholder="Enter your email" required>
    <button type="submit" class="forge-waitlist__btn magnetic-btn">Notify Me</button>
  </form>
  <p class="forge-waitlist__note">No spam, ever. Unsubscribe anytime.</p>
</div>
```

---

## Call to Action

### Full-Width CTA
```html
<!-- FORGE: CTA Section -->
<style>
.forge-cta {
  background: var(--bg-secondary);
  padding: var(--space-2xl) var(--space-xl);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.forge-cta__bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, var(--accent-muted) 0%, transparent 70%);
  opacity: 0.5;
}

.forge-cta__content {
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.forge-cta__title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 6vw, 4rem);
  color: var(--text-primary);
  margin-bottom: var(--space-md);
}

.forge-cta__description {
  font-family: var(--font-body);
  font-size: var(--text-xl);
  color: var(--text-secondary);
  margin-bottom: var(--space-lg);
}

.forge-cta__actions {
  display: flex;
  justify-content: center;
  gap: var(--space-sm);
  flex-wrap: wrap;
}

.forge-cta__btn {
  padding: var(--space-md) var(--space-xl);
  background: var(--accent-primary);
  color: var(--text-inverse);
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  font-size: var(--text-lg);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: var(--transition-base);
}

.forge-cta__btn:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
}

.forge-cta__btn--outline {
  background: transparent;
  border: 2px solid var(--border-default);
  color: var(--text-primary);
}

.forge-cta__btn--outline:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
  transform: translateY(-2px);
}
</style>

<section class="forge-cta">
  <div class="forge-cta__bg"></div>
  <div class="forge-cta__content">
    <h2 class="forge-cta__title">Ready to Get Started?</h2>
    <p class="forge-cta__description">
      Join thousands of satisfied customers who transformed their business with us.
    </p>
    <div class="forge-cta__actions">
      <a href="#contact" class="forge-cta__btn magnetic-btn">Start Your Project</a>
      <a href="#work" class="forge-cta__btn forge-cta__btn--outline">View Our Work</a>
    </div>
  </div>
</section>
```

---

## Footer

### Minimal Footer
```html
<!-- FORGE: Footer Minimal -->
<style>
.forge-footer {
  background: var(--bg-primary);
  border-top: 1px solid var(--border-subtle);
  padding: var(--space-xl) var(--space-md);
}

.forge-footer__inner {
  max-width: var(--container-xl);
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-md);
}

.forge-footer__brand {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  color: var(--text-primary);
}

.forge-footer__links {
  display: flex;
  gap: var(--space-md);
}

.forge-footer__link {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.3s ease;
}

.forge-footer__link:hover {
  color: var(--accent-primary);
}

.forge-footer__social {
  display: flex;
  gap: var(--space-sm);
}

.forge-footer__social-link {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-subtle);
  border-radius: 50%;
  color: var(--text-secondary);
  transition: var(--transition-base);
}

.forge-footer__social-link:hover {
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}

.forge-footer__copyright {
  width: 100%;
  text-align: center;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--text-muted);
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--border-subtle);
}
</style>

<footer class="forge-footer">
  <div class="forge-footer__inner">
    <div class="forge-footer__brand">BRAND</div>
    <nav class="forge-footer__links">
      <a href="#" class="forge-footer__link">About</a>
      <a href="#" class="forge-footer__link">Services</a>
      <a href="#" class="forge-footer__link">Work</a>
      <a href="#" class="forge-footer__link">Contact</a>
    </nav>
    <div class="forge-footer__social">
      <a href="#" class="forge-footer__social-link" aria-label="Twitter">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
      </a>
      <a href="#" class="forge-footer__social-link" aria-label="LinkedIn">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
      </a>
      <a href="#" class="forge-footer__social-link" aria-label="Instagram">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
      </a>
    </div>
    <p class="forge-footer__copyright">
      © 2024 Brand Name. All rights reserved. Built by PhD Networks.
    </p>
  </div>
</footer>
```
