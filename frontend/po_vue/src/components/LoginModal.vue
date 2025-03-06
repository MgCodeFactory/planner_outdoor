<template>
  <Teleport to="body">
    <div v-if="show" class="modal-background">
      <div class="modal-container">
        <form
          @submit.prevent="loginAccount || resetPassword"
          class="form-container"
        >
          <h4 v-if="!showLoginForm && !showResetForm" class="font-bold">
            NO ACCOUNT YET ?
          </h4>
          <button
            v-if="!showLoginForm && !showResetForm"
            @click="goToRegister"
            class="classic-button"
          >
            REGISTER
          </button>
          <h4 class="font-bold">ALREADY REGISTERED</h4>
          <button
            :disabled="showLoginForm"
            v-if="!showResetForm"
            @click="toggleLoginForm"
            class="classic-button"
          >
            LOGIN
          </button>
          <input
            class="login-input"
            v-if="showLoginForm"
            type="email"
            v-model="loginEmail"
            placeholder="Enter your email"
            required
          />
          <input
            v-if="showLoginForm"
            class="login-input"
            type="password"
            v-model="loginPassword"
            placeholder="Enter your password"
            required
          />
          <button
            :disabled="showResetForm"
            v-if="!showLoginForm"
            @click="toggleResetForm"
            class="classic-button"
          >
            RESET PASSWORD
          </button>
          <input
            v-if="showResetForm"
            class="login-input"
            type="email"
            v-model="resetEmail"
            placeholder="Enter your email"
            required
          />
          <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
          <p v-if="successMsg" class="success-message">{{ successMsg }}</p>
          <div
            v-if="showLoginForm || showResetForm"
            class="flex flex-row justify-center items-center gap-2"
          >
            <button v-if="errorMsg" @click="clearForm" class="classic-button">
              RETRY
            </button>
            <button
              v-else-if="showLoginForm"
              @click="loginAccount"
              class="classic-button"
            >
              SUBMIT
            </button>
            <button
              v-else-if="showResetForm && !successMsg"
              @click="resetPassword"
              class="classic-button"
            >
              SUBMIT
            </button>
            <button
              v-if="successMsg"
              @click="$emit('close')"
              class="classic-button"
            >
              OK
            </button>
            <button v-else @click="$emit('close')" class="classic-button">
              CLOSE
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginModal',
  emits: ['close'],
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showLoginForm: false,
      showResetForm: false,
      loginEmail: '',
      loginPassword: '',
      resetEmail: '',
      successMsg: '',
      errorMsg: '',
    };
  },
  methods: {
    // Toggle function to show login form
    toggleLoginForm() {
      this.showLoginForm = true;
      this.showResetForm = false;
    },
    toggleResetForm() {
      this.showResetForm = true;
      this.showLoginForm = false;
    },
    // email input validation xxxxxxx@xxx.xxxx
    validInputEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        return false;
      }
      return true;
    },
    // password input validation
    // At least 8 characters, one uppercase, one lowercase,
    // one number, one special character, and all different
    validInputPassword(password) {
      if (password.length < 8) {
        this.errorMsg = 'Password must be at least 8 characters long.';
        return false;
      }
      const charSet = new Set(password);
      if (charSet.size !== password.length) {
        this.errorMsg = 'In password, all characters must be different.';
        return false;
      }
      const upperCount = (password.match(/[A-Z]/g) || []).length;
      const lowerCount = (password.match(/[a-z]/g) || []).length;
      const digitCount = (password.match(/[0-9]/g) || []).length;
      if (upperCount === 0) {
        this.errorMsg = 'Password must contain at least one uppercase letter.';
        return false;
      }
      if (lowerCount === 0) {
        this.errorMsg = 'Password must contain at least one lowercase letter.';
        return false;
      }
      if (digitCount === 0) {
        this.errorMsg = 'Password must contain at least one digit.';
        return false;
      }
      const globalCount = upperCount + lowerCount + digitCount
      if (globalCount === password.length) {
        this.errorMsg = 'Password must contain at least one special character.'
        return false;
      }
      return true;
    },
    // async method to obtain user authentification with good credentials
    async loginAccount() {
      if (!this.validInputEmail(this.loginEmail)) {
        this.errorMsg = 'Invalid user email.';
        return;
      }
      if (!this.validInputPassword(this.loginPassword)) {
        this.errorMsg = 'Invalid user password.';
        return;
      }
      try {
        const response = await axios.post('http://localhost:8020/auth/login/', {
          email: this.loginEmail,
          password: this.loginPassword,
        });
        const token = response.data.access;
        const userId = response.data.user.user_id;
        this.$store.dispatch('login', {
          email: this.loginEmail,
          userId,
          token,
        });
        this.$router.push('/account');
        this.$emit('close');
      } catch (error) {
        if (error.response) {
          if (!error.response.data.detail) {
            if (error.response.data.password) {
              this.errorMsg = `Password: ${error.response.data.password[0]}`;
            } else if (error.response.data.email) {
              this.errorMsg = `Email: ${error.response.data.email[0]}`;
            }
          } else if (error.response.data.detail) {
            this.errorMsg = error.response.data.detail;
          } else {
            this.errorMsg = 'An error occurred during login.';
          }
        }
      }
    },
    // async method for resetting password (user lost his password !)
    async resetPassword() {
      if (!this.validInputEmail(this.resetEmail)) {
        this.errorMsg = 'Invalid user email.';
        return;
      }
      try {
        const response = await axios.post(
          'http://localhost:8020/auth/password-reset/',
          {
            email: this.resetEmail,
          }
        );
        this.successMsg = response.data.message;
      } catch (error) {
        if (error.response) {
          if (!error.response.data.detail) {
            if (error.response.data.email) {
              this.errorMsg = `Email: ${error.response.data.email}`;
            } else if (error.response.data.error) {
              this.errorMsg = `Email: ${error.response.data.error}`;
            }
          } else if (error.response.data.detail) {
            this.errorMsg = error.response.data.detail;
          } else {
            this.errorMsg = 'An error occurred during reset.';
          }
        }
      }
    },
    goToRegister() {
      this.$router.push('/register');
      this.$emit('close');
    },
    clearForm() {
      this.showLoginForm = false;
      this.showResetForm = false;
      this.loginEmail = '';
      this.loginPassword = '';
      this.resetEmail = '';
      this.$successMsg = '';
      this.errorMsg = '';
    },
  },
};
</script>

<style scoped lang="postcss">
.login-input {
  @apply bg-zinc-100 border border-zinc-300 focus:ring-2 rounded-md font-bold p-2;
}
</style>
