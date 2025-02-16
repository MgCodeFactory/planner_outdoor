<template>
  <div class="standard-container">
    <div class="standard-item">
      <form @submit.prevent="updateUserAccountInfo" class="form-container">
        <h3 class="font-bold">YOUR ACCOUNT DATA</h3>
        <label class="account-label">Username:</label>
        <input
          v-model="username"
          @focus="clearMessages"
          class="account-input"
        />

        <label class="account-label">Email:</label>
        <input
          v-model="email"
          type="email"
          @focus="clearMessages"
          class="account-input"
        />

        <label class="account-label">Location:</label>
        <input
          @focus="clearMessages"
          :value="JSON.stringify(location)"
          readonly
          class="account-input"
        />
        <button
          v-show="!successAccountMsg"
          type="button"
          @click="showLocateModal = true"
          class="classic-button"
        >
          CHANGE LOCATION
        </button>
        <LocateModal
          v-if="showLocateModal"
          :show="showLocateModal"
          @location-selected="setLocationValue"
          @close="showLocateModal = false"
        />
        <label class="account-label">First name:</label>
        <input
          v-model="first_name"
          type="text"
          @focus="clearMessages"
          class="account-input"
        />
        <label class="account-label">Last name:</label>
        <input
          v-model="last_name"
          type="text"
          @focus="clearMessages"
          class="account-input"
        />
        <p v-if="successAccountMsg" class="success-message">
          {{ successAccountMsg }}
        </p>
        <p v-if="errorAccountMsg" class="error-message">
          {{ errorAccountMsg }}
        </p>
        <button v-if="!successAccountMsg" class="classic-button" type="submit">
          UPDATE DATA
        </button>
        <button
          v-else
          class="classic-button"
          type="button"
          @click="clearMessages"
        >
          OK
        </button>
        <button class="classic-button" @click="openDeleteAccountModal">
          DELETE ACCOUNT
        </button>
        <DeleteAccountPrompt
          v-if="showDeleteAccountModal"
          :show="showDeleteAccountModal"
          @close="showDeleteAccountModal = false"
        />
      </form>
    </div>
    <div class="standard-item">
      <FetchActivities />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import LocateModal from '@/components/LocateModal.vue';
import DeleteAccountPrompt from '@/components/DeleteAccountPrompt.vue';
import FetchActivities from '@/components/FetchActivities.vue';

export default {
  name: 'AccountManagerView',
  components: {
    LocateModal,
    DeleteAccountPrompt,
    FetchActivities,
  },
  data() {
    return {
      userId: Number,
      username: '',
      email: '',
      location: null,
      first_name: '',
      last_name: '',
      successAccountMsg: '',
      errorAccountMsg: '',
      showLocateModal: false,
      showDeleteAccountModal: false,
    };
  },
  created() {
    this.getUserAccountInfo();
  },
  methods: {
    setLocationValue(selectedLocation) {
      this.location = null;
      this.location = selectedLocation;
      this.showLocateModal = false;
    },
    openDeleteAccountModal() {
      this.errorAccountMsg = '';
      this.successAccountMsg = '';
      this.showDeleteAccountModal = true;
    },
    async getUserAccountInfo() {
      try {
        const response = await axios.get(
          `http://localhost:8020/user-detail/${this.$store.getters.getUserId}/`,
          {
            headers: {
              Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
            },
          }
        );
        this.userId = response.data.id;
        this.username = response.data.username;
        this.email = response.data.email;
        this.location = response.data.location;
        this.first_name = response.data.first_name;
        this.last_name = response.data.last_name;
        // data for update user
        this.currentUsername = this.username;
        this.currentEmail = this.email;
        this.currentLocation = this.location;
        this.currentFirstName = this.first_name;
        this.currentLastName = this.last_name;
        this.errorAccountMsg = '';
      } catch (error) {
        this.errorAccountMsg =
          error.response?.data?.error || 'An unexpected error occurred';
      }
    },
    async updateUserAccountInfo() {
      try {
        const dataToUpdate = {};
        if (this.username !== this.currentUsername) {
          dataToUpdate.username = this.username;
        }
        if (this.email !== this.currentEmail) {
          dataToUpdate.email = this.email;
        }
        if (this.location !== this.currentLocation) {
          dataToUpdate.location = this.location;
        }
        if (this.first_name !== this.currentFirstName) {
          dataToUpdate.first_name = this.first_name;
        }
        if (this.last_name !== this.currentLastName) {
          dataToUpdate.last_name = this.last_name;
        }
        const response = await axios.patch(
          `http://localhost:8020/user-detail/${this.$store.getters.getUserId}/`,
          dataToUpdate,
          {
            headers: {
              Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
            },
          }
        );
        this.errorAccountMsg = '';
        this.successAccountMsg = 'Data updated successfully';
        await this.getUserAccountInfo();
        // Update store informations
        this.$store.commit('setUsername', response.data.username);
        this.$store.commit('setEmail', response.data.email);
      } catch (error) {
        this.successAccountMsg = '';
        if (error.response) {
          if (error.response.data.username) {
            this.errorAccountMsg = `Username: ${error.response.data.username[0]}`;
          }
          if (error.response.data.email) {
            this.errorAccountMsg = `Email: ${error.response.data.email[0]}`;
          }
          if (error.response.data.location) {
            this.errorAccountMsg = `Location: ${error.response.data.location[0]}`;
          }
          if (error.response.data.first_name) {
            this.errorAccountMsg = `First name: ${error.response.data.first_name[0]}`;
          }
          if (error.response.data.last_name) {
            this.errorAccountMsg = `Last name: ${error.response.data.last_name[0]}`;
          }
        } else {
          this.errorAccountMsg = 'An unexpected error occurred';
        }
      }
    },
    clearMessages() {
      this.successAccountMsg = '';
      this.errorAccountMsg = '';
    },
  },
};
</script>

<style scoped lang="postcss">
.account-input {
  @apply bg-zinc-100 border border-zinc-300 focus:ring-2 rounded-md font-bold p-2;
}

.account-label {
  @apply font-bold text-left;
}
</style>
