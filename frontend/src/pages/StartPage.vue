<script setup lang="ts"></script>

<template>
  <div class="start">
    <h1>LexLoop</h1>
    <router-link to="/login">
      <button>Sign In</button>
    </router-link>
  </div>
</template>

<style scoped>
.start {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-top: 3rem;
}
</style>
