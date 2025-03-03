<template>
  <img
    src="/assets/po_logo_color_640x480.svg"
    alt="planner outdoor logo"
    class="background-logo"
  />
  <div class="app-container">
    <PageHeader class="app-header" />
    <router-view class="app-router-view" />

    <PageFooter class="app-footer" />
  </div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue';
import PageFooter from '@/components/PageFooter.vue';

export default {
  name: 'App',
  components: {
    PageHeader,
    PageFooter,
  },
};
</script>

<style lang="postcss">
.background-logo {
  @apply fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 opacity-40 w-[50vw] h-[50vw] sm:w-[40vw] sm:h-[40vw];
}

.app-container {
  @apply flex flex-col min-h-screen min-w-full bg-gradient-to-b from-green-600 to-green-200;
}

.app-header,
.app-footer {
  @apply bg-transparent p-4;
}

.app-router-view {
  @apply flex-grow;
}

.header-footer {
  @apply flex-shrink-0;
}

.nav-header {
  @apply flex justify-between;
}

.nav-footer {
  @apply flex justify-center space-x-4 p-4;
}

.classic-button {
  @apply flex-1 mx-2 bg-blue-500 hover:bg-blue-700 disabled:bg-gray-300 text-white font-bold mt-2 py-2 px-4 rounded;
}

.footer-button {
  @apply w-12 h-12 rounded-full bg-blue-500 hover:bg-blue-700 flex items-center justify-center;
}

.svg-footer {
  @apply w-6 h-6;
}

.modal-background {
  @apply fixed inset-0 bg-gray-800 bg-opacity-80 flex items-center justify-center z-40;
}

.modal-container {
  @apply bg-white rounded-md p-8 max-w-sm md:max-w-lg z-50;
}

.form-container {
  @apply flex flex-col justify-start items-center gap-y-3;
}

.standard-container {
  @apply flex flex-col justify-start items-center gap-y-3;
}

.standard-item {
  @apply z-20 opacity-100 bg-zinc-200 border border-b-gray-400 rounded-md  hover:ring-2 hover:border-black hover:ring-black p-2 max-w-sm md:max-w-lg;
}

.error-message {
  @apply text-red-700 font-semibold max-w-full;
}

.success-message {
  @apply text-green-700 font-semibold max-w-full;
}

.weather-container {
  @apply flex flex-row flex-wrap justify-center items-center gap-5 max-w-fit p-2;
}

.weather-item {
  @apply flex flex-col justify-center items-center z-20 opacity-100 bg-zinc-200 border border-b-gray-400 rounded-md hover:ring-2 hover:border-black hover:ring-black p-2 max-w-sm md:max-w-lg;
}
</style>
