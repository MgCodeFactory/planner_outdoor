<template>
  <div class="standard-container">
    <div class="standard-item">
      <form @submit.prevent="register" class="form-container">
        <h3>CREATE AN ACCOUNT</h3>
        <input
          type="text"
          v-model="username"
          placeholder="Username"
          required
          class="register-input"
          v-on:focus="usernameHelp"
          v-on:focusout="showHelpUsername = false"
        />
        <p v-show="showHelpUsername" class="text-center text-sm italic max-w-full">
          {{ usernameRules }}
        </p>
        <input
          type="email"
          v-model="email"
          placeholder="Email"
          required
          class="register-input"
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          required
          class="register-input"
          v-on:focus="passwordHelp"
          v-on:focusout="showHelpPassword = false"
        />
        <p v-show="showHelpPassword" class="text-center text-sm italic max-w-full">
          {{ passwordRules }}
        </p>
        <input
          type="text"
          :value="JSON.stringify(location)"
          placeholder="Location"
          class="register-input"
          readonly
          required
        />
        <p v-if="successMsg" class="success-message">{{ successMsg }}</p>
        <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
        <button
          v-show="!successMsg"
          type="button"
          @click="showLocateModal = true"
          class="classic-button"
        >
          GET LOCATION
        </button>
        <LocateModal
          v-if="showLocateModal"
          :show="showLocateModal"
          @location-selected="setLocationValue"
          @close="showLocateModal = false"
        />
        <button
          v-if="!successMsg"
          type="button"
          @click="register"
          class="classic-button"
        >
          REGISTER
        </button>
        <button v-else type="button" @click="goToHome" class="classic-button">
          OK
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import LocateModal from '@/components/LocateModal.vue';

export default {
  name: 'RegisterView',
  components: {
    LocateModal,
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      location: null,
      successMsg: '',
      errorMsg: '',
      showLocateModal: false,
      usernameRules: '',
      showHelpUsername: false,
      passwordRules: '',
      showHelpPassword: false,
    };
  },
  methods: {
    async usernameHelp() {
      try {
        const response = await axios.get(
          'http://localhost:8020/validators-rules/'
        );
        this.usernameRules = response.data.username_rules;
        this.showHelpUsername = true;
      } catch (error) {
        console.error('Failed to fetch validation rules:', error);
      }
    },
    async passwordHelp() {
      try {
        const response = await axios.get(
          'http://localhost:8020/validators-rules/'
        );
        this.passwordRules = response.data.password_rules;
        this.showHelpPassword = true;
      } catch (error) {
        console.error('Failed to fetch validation rules:', error);
      }
    },
    setLocationValue(selectedLocation) {
      this.location = null;
      this.location = selectedLocation;
      this.showLocateModal = false;
    },
    async register() {
      try {
        const response = await axios.post(
          'http://localhost:8020/auth/register/',
          {
            username: this.username,
            email: this.email,
            password: this.password,
            location: this.location,
          }
        );
        this.successMsg = `${this.username} account successfully created.`;
      } catch (error) {
        if (error.response) {
          if (error.response.data.username) {
            this.errorMsg = `Username: ${error.response.data.username[0]}`;
          } else if (error.response.data.email) {
            this.errorMsg = `Email: ${error.response.data.email[0]}`;
          } else if (error.response.data.password) {
            this.errorMsg = `Password: ${error.response.data.password[0]}`;
          } else if (error.response.data.location) {
            this.errorMsg = `Location: ${error.response.data.location[0]}`;
          }
        } else {
          this.errorMsg = 'An error occurred during registration.';
        }
      }
    },
    goToHome() {
      this.clearForm();
      this.$router.push('/');
    },
    clearForm() {
      this.username = '';
      this.email = '';
      this.password = '';
      this.location = null;
      this.successMsg = '';
      this.errorMsg = '';
      this.usernameRules = '';
      this.showHelpUsername = false;
      this.passwordRules = '';
      this.showHelpPassword = false;
    },
  },
};
</script>

<style scoped lang="postcss">
.register-input {
  @apply bg-zinc-100 border border-zinc-300 focus:ring-2 rounded-md font-bold p-2;
}
</style>
