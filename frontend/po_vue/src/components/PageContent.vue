<template>
    <main class="content-container">
      <HomeView />
    </main>
  </template>
  
  <script>
  import HomeView from '@/views/HomeView.vue';

  export default {
    components: {
      HomeView,
    },
  };
  
  </script>

  <style scoped>
  .content-container {
    order: 1; /* item of app-container*/
    display: flex;
    flex-direction:row;
    flex-grow: 1;
    align-items: center;
    justify-content: space-between;
    background-color: var(--color-light-grey);
    color: var(--color-white);
  }
  </style>