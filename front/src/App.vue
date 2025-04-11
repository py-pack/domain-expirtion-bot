<script setup lang="ts">

</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <h1>Vue 3 + Vite + TypeScript</h1>
      <p>
        This template should help get you started developing with Vue 3 in Vite.
        It is recommended to use the official documentation as a starting point:
        <a href="https://vuejs.org/guide/introduction.html" target="_blank" rel="noopener">Vue 3 Guide</a>
      </p>
    </div>
  </header>

  <main>
    <h1>Hello</h1>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
