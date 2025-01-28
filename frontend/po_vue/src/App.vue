<template>
  <div class="app-container">
    <PageHeader />
    <!--PageContent /-->
    <router-view />
    <PageFooter />
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader.vue";
//import PageContent from "@/components/PageContent.vue";
import PageFooter from "@/components/PageFooter.vue";

export default {
  name: 'App',
  components: {
    PageHeader,
    //PageContent,
    PageFooter,
  },
};
</script>

<style>
:root {
  /* set colors */
  --color-black: #090909;
  --color-white: #ffffff;
  --color-light-grey: #f3f3f3;
  --color-medium-grey: #726a6a;
  --color-dark-grey: #353535;
  --color-error-msg: #c63434;
  --color-success-msg: #1d01a8;
  --color-header-footer: rgba(32, 159, 232, 0.75);
  --color-button: rgba(32, 159, 232, 1);
  --color-background-modal: rgba(0, 0, 0, 0.5);
  --color-background-item: rgba(255, 255, 255, 0.7);
  /* set header & footer */
  --header-footer-height: 5vh;
  --header-footer-opacity: 0.7;
  --header-footer-shadow: 5px 5px 5px var(--color-medium-grey);
  --margin-header-footer: calc((var(--header-footer-height)) + 10px);
  --header-footer-width: 100%;
  /* set fonts */
  --font-family: 'Ubuntu', sans-serif;
  --font-size-small: 0.7rem;
  --font-size-medium: 1.2rem;
  --font-size-large: 1.5rem;
  --font-size-x-large: 2rem;
  --font-size-xx-large: 3rem;
  --font-weight-regular: 400;
  --font-weight-bold: 700;
  /* others */
  --modal-shadow: 30px 30px 30px var(--color-dark-grey);
  --default-radius: 0;
  --modal-header-footer-height: 3.5vh;
  --modal-content-height: 6vh;
}

@media screen and ((max-width: 800px) or (max-height: 800px)) {
  :root {
    --header-footer-height: 8vh;
  }
}

html,
body {
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  font-family: var(--font-family);
}

.app-container {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: start;
  align-items: stretch;
  align-content: center;
  min-height: 100vh;
  gap: 0;
}

.modal-background {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--color-background-modal);
}

.modal-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  width: 20vw;
  background: var(--color-light-grey);
  /*text-align: center;*/
}

.modal-item-header {
  display: flex;
  justify-content: center;
  align-items: center;
  height: var(--modal-header-footer-height);
  width: 100%;
  color: var(--color-white);
  background: var(--color-header-footer);
}

.modal-item-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: var(--modal-content-height);
  height:fit-content;
  width: 100%;
  color: var(--color-black);
  background: var(--color-light-grey);
}

.modal-item-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  height: var(--modal-header-footer-height);
  width: 100%;
  color: var(--color-white);
  background: var(--color-header-footer);
}
</style>
