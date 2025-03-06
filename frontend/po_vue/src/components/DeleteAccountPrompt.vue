<template>
  <Teleport to="body">
    <div v-if="show" class="modal-background">
      <div class="modal-container">
        <p class="text-center">{{ defaultMsg || errorMsg }}</p>
        <div class="flex flex-row items-center justify-center">
          <button
            type="button"
            class="delete-account-button"
            v-if="showDeleteButton"
            @click="handleActionClick"
          >
            {{ buttonMsg }}
          </button>
          <button
            type="button"
            class="classic-button"
            v-if="showCloseButton"
            @click="closeModal"
          >
            CLOSE
          </button>
          <button
            type="button"
            class="classic-button"
            v-if="showCancelButton"
            @click="cancelModal"
          >
            CANCEL
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DeleteAccountPrompt',
  props: {
    show: Boolean,
  },
  data() {
    return {
      defaultMsg: 'Confirm to delete your account',
      buttonMsg: 'ERASE ACCOUNT !',
      errorMsg: '',
      showDeleteButton: true,
      showCloseButton: false,
      showCancelButton: true,
      confirmDelete: false,
    };
  },
  methods: {
    cancelModal() {
      this.$emit('close');
    },
    closeModal() {
      this.$emit('close');
      this.resetModal();
    },
    handleActionClick() {
      if (!this.confirmDelete) {
        this.defaultMsg = 'Are you sure? This action cannot be undone!';
        this.buttonMsg = 'OK';
        this.confirmDelete = true;
      } else {
        this.deleteUserAccount();
      }
    },
    async deleteUserAccount() {
      try {
        await axios.delete(
          `http://localhost:8020/user-detail/${this.$store.getters.getUserId}/`,
          {
            headers: {
              Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
            },
          }
        );
        this.defaultMsg = 'Account deleted successfully.';
        this.showDeleteButton = false;
        this.showCancelButton = false;
        this.showCloseButton = true;
        this.$store.commit('clearUserData');
        this.$router.push('/').then(() => window.location.reload());
      } catch (error) {
        this.errorMsg = 'Error appeared while deleting your account';
        this.defaultMsg = '';
        this.showDeleteButton = false;
        this.showCancelButton = false;
        this.showCloseButton = true;
      }
    },
    resetModal() {
      this.defaultMsg = 'Confirm to delete your account';
      this.errorMsg = '';
      this.buttonMsg = 'Erase account!';
      this.showDeleteButton = true;
      this.showCloseButton = false;
      this.showCancelButton = true;
      this.confirmDelete = false;
    },
  },
  /*
  watch: {
    show(newValue) {
      if (newValue) this.resetModal();
    },
  },*/
};
</script>

<style scoped></style>
