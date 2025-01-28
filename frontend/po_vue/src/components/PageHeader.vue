<template>
  <header class="header-container">
    <div class="home" @click="goToHome">
      <h3>HOME</h3>
    </div>
    <div class="locate" @click="showLocateModal = true">
      <h3>LOCATE</h3>
      <LocateModal
        v-if="showLocateModal"
        :show="showLocateModal"
        @close="showLocateModal = false"
      />
    </div>
    <div class="login" @click="goToLogin">
      <h3>LOGIN</h3>
      <LoginView />
    </div>
  </header>
</template>

<script>
import LoginView from '@/components/LoginView.vue';
import LocateModal from '@/components/LocateModal.vue';

export default {
  name: 'PageHeader',
  components: {
    LoginView,
    LocateModal,
  },
  data() {
    return {
      showLocateModal: false,
    };
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    goToLogin() {
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
@media screen and ((max-width: 800px) or (max-height: 800px)) {
  h3 {
    font-size: 0.7rem;
  }
}

.header-container {
  order: 0; /* item of app-container*/
  display: flex;
  flex-direction: row;
  align-items: center;
  flex-grow: 0;
  flex-wrap: nowrap;
  gap: 0;
  height: var(--header-footer-height);
  background-color: var(--color-header-footer);
  color: var(--color-white);
}

.home {
  order: 0; /* item of header-container*/
  width: 20vw;
  flex-grow: 0;
}

.locate {
  order: 1; /* item of header-container*/
  flex-grow: 1;
}

.login {
  order: 2; /* item of header-container*/
  flex-grow: 0;
  width: 20vw;
}

.header-container > div:hover {
  background-color: var(--color-white);
  color: var(--color-black);
  background-size: 100%;
  cursor: pointer;
}

h3 {
  text-align: center;
}
</style>
