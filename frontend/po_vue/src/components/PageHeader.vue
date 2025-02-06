<template>
  <header class="header-footer">
    <nav class="nav-header">
      <button class="classic-button" @click="goToHome">HOME</button>
      <button class="classic-button" @click="showLocateModal = true">
        LOCATE
        <LocateModal
          v-if="showLocateModal"
          :show="showLocateModal"
          @close="showLocateModal = false"
        />
      </button>
      <button class="classic-button" @click="showLoginModal = true">
        LOGIN
        <LoginModal
          v-if="showLoginModal"
          :show="showLoginModal"
          @close="showLoginModal = false"
        />
      </button>
    </nav>
  </header>
</template>

<script>
import LocateModal from '@/components/LocateModal.vue';
import LoginModal from '@/components/LoginModal.vue';

export default {
  name: 'PageHeader',
  components: {
    LocateModal,
    LoginModal,
  },
  data() {
    return {
      showLocateModal: false,
      showLoginModal: false,
    };
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
  },
};
</script>
