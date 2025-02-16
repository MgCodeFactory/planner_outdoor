<template>
  <Teleport to="body">
    <div v-if="show" class="modal-background">
      <div class="modal-container">
        <div>
          <h3 class="font-bold p-2">Are you sure you want to logout ?</h3>
          <p class="font-light italic p-2">You will be redirected to homepage.</p>
        </div>
        <div>
          <p v-show="ErrorMsg" class="error-message">{{ ErrorMsg }}</p>
        </div>
        <div class="flex items-center">
          <button
            v-show="!ErrorMsg"
            type="button"
            class="classic-button"
            @click="logoutAccount"
          >
            LOGOUT
          </button>
          <button type="button" class="classic-button" @click="$emit('close')">
            CANCEL
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
export default {
  name: 'LogoutModal',
  emits: ['close'],
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      ErrorMsg: '',
    };
  },
  methods: {
    async logoutAccount() {
      try {
        this.$store.dispatch('logout');
        this.$router.push('/');
      } catch (error) {
        this.ErrorMsg = 'Unable to logout. Restart your browser.';
      }
    },
  },
};
</script>

<style scoped lang="postcss"></style>
