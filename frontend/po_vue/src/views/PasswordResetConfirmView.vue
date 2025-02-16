<template>
  <div class="standard-container">
    <div class="standard-item">
      <form @submit.prevent="recoveryPassword" class="form-container">
        <article class="prose text-center">
          <h4>Password Reset</h4>
          <p>You are on the reset password form for your account.</p>
        </article>
        <input
          v-model="newPassword"
          type="password"
          placeholder="Enter new password"
          class="reset-input"
          v-on:focus="passwordHelp"
          v-on:focusout="showHelp = false"
        />
        <p v-show="showHelp" class="text-center text-sm italic">
          {{ passwordRules }}
        </p>
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm new password"
          class="reset-input"
        />
        <p v-if="recoveryMsg" class="recovery-message">{{ recoveryMsg }}</p>
        <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        <div v-show="!recoveryMsg">
          <button v-if="!errorMsg" type="submit" class="classic-button">
            SUBMIT
          </button>
          <button
            v-else
            @click="clearForm"
            type="button"
            class="classic-button"
          >
            RETRY
          </button>
        </div>
        <div v-show="recoveryMsg">
          <button
            @click="this.$router.push('/')"
            type="button"
            class="classic-button"
          >
            OK
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';

export default {
  name: 'PasswordResetConfirmView',
  setup() {
    const route = useRoute();
    return {
      route,
    };
  },
  data() {
    return {
      newPassword: '',
      confirmPassword: '',
      recoveryMsg: '',
      errorMsg: '',
      passwordRules: '',
      showHelp: false,
    };
  },
  methods: {
    async passwordHelp() {
      try {
        const response = await axios.get(
          'http://localhost:8020/validators-rules/'
        );
        this.passwordRules = response.data.password_rules;
        this.showHelp = true;
      } catch (error) {
        console.error('Failed to fetch validation rules:', error);
      }
    },
    async recoveryPassword() {
      try {
        const response = await axios.patch(
          `http://localhost:8020/auth/password-reset-confirm/${this.route.params.uid}/${this.route.params.token}/`,
          {
            new_password: this.newPassword,
            confirm_password: this.confirmPassword,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
        this.recoveryMsg = response.data.message;
      } catch (error) {
        if (error.response) {
          if (error.response.data.new_password) {
            this.errorMsg = `New password: ${error.response.data.new_password}`;
          } else if (error.response.data.confirm_password) {
            this.errorMsg = `Confirm password: ${error.response.data.confirm_password}`;
          } else if (error.response.data.non_field_errors) {
            this.errorMsg = `Error: ${error.response.data.non_field_errors[0]}`;
          } else {
            this.errorMsg = 'An error occurred during reset process.';
          }
        }
      }
    },
    clearForm() {
      this.newPassword = '';
      this.confirmPassword = '';
      this.recoveryMsg = '';
      this.errorMsg = '';
      this.showHelp = false;
    },
  },
};
</script>

<style scoped lang="postcss">
.reset-input {
  @apply bg-zinc-100 border border-zinc-300 focus:ring-2 rounded-md font-bold p-2;
}
</style>
