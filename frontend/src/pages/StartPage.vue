<script setup lang="ts"></script>

<template>
  <div class="start">
    <div class="hero">
      <p class="eyebrow">Vocabulary practice</p>
      <h1 class="brand">LexLoop</h1>
      <p class="tagline">Build word knowledge in loops — terms, tags, and connections.</p>
      <router-link class="cta ll-btn ll-btn-primary" to="/login">Sign in</router-link>
    </div>
  </div>
</template>

<style scoped>
.start {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: var(--ll-space-page);
}

.hero {
  width: min(100%, 28rem);
  text-align: center;
  animation: rise 0.55s ease-out both;
}

.eyebrow {
  margin: 0 0 0.75rem;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ll-accent);
}

.brand {
  font-size: clamp(3rem, 10vw, 4.5rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  margin: 0 0 0.85rem;
  background: linear-gradient(135deg, var(--ll-ink) 40%, var(--ll-accent));
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.tagline {
  margin: 0 0 1.75rem;
  color: var(--ll-ink-muted);
  font-size: 1.05rem;
  line-height: 1.45;
}

.cta {
  min-width: 10rem;
  text-decoration: none;
}

@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}
</style>
