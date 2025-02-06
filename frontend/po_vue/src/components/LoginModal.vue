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
          <p v-if="successMsg" class="sucess-message">{{ successMsg }}</p>
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
    toggleLoginForm() {
      this.showLoginForm = true;
      this.showResetForm = false;
    },
    toggleResetForm() {
      this.showResetForm = true;
      this.showLoginForm = false;
    },
    async loginAccount() {
      try {
        const response = await axios.post('http://localhost:8020/auth/login/', {
          email: this.loginEmail,
          password: this.loginPassword,
        });
        const token = response.data.access;
        this.$store.dispatch('login', { email: this.loginEmail, token });
        const nextRoute = this.$route.query.next || '/account';
        this.$router.push(nextRoute);
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
    async resetPassword() {
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
            this.errorMsg = 'An error occurred during login.';
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

.error-message {
  @apply text-red-700 font-semibold max-w-full;
}

.sucess-message {
  @apply text-green-700 font-semibold max-w-full;
}
</style>
