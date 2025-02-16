<template>
  <header class="header-footer">
    <nav class="nav-header">
      <button type="button" class="classic-button" @click="goToHome">
        HOME
      </button>
      <button
        type="button"
        class="classic-button"
        @click="showLocateModal = true"
      >
        LOCATE
        <LocateModal
          v-if="showLocateModal"
          :show="showLocateModal"
          @close="showLocateModal = false"
        />
      </button>
      <button
        v-if="!userIsLogged"
        type="button"
        class="classic-button"
        @click="showLoginModal = true"
      >
        LOGIN
        <LoginModal
          v-if="showLoginModal"
          :show="showLoginModal"
          @close="showLoginModal = false"
        />
      </button>
      <button
        v-else
        type="button"
        class="classic-button"
        @click="showLogoutModal = true"
      >
        LOGOUT
        <LogoutModal
          v-if="showLogoutModal"
          :show="showLogoutModal"
          @close="showLogoutModal = false"
        />
      </button>
      <button
        v-show="userIsLogged"
        type="button"
        class="classic-button"
        @click="goToAccount"
      >
        ACCOUNT
      </button>
    </nav>
  </header>
</template>

<script>
import LocateModal from '@/components/LocateModal.vue';
import LoginModal from '@/components/LoginModal.vue';
import LogoutModal from '@/components/LogoutModal.vue';

export default {
  name: 'PageHeader',
  emits: ['location-selected', 'close'],
  components: {
    LocateModal,
    LoginModal,
    LogoutModal,
  },
  data() {
    return {
      showLocateModal: false,
      showLoginModal: false,
      showLogoutModal: false,
    };
  },
  computed: {
    userIsLogged() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    goToAccount() {
      this.$router.push('/account');
    },
  },
};
</script>
