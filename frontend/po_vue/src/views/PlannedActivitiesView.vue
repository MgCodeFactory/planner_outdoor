<template>
  <div class="standard-container">
    <div class="standard-item">
      <form class="form-container">
        <h3 class="font-bold">ADD A LOCATION</h3>
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
          SELECT LOCATION
        </button>
        <LocateModal
          v-if="showLocateModal"
          :show="showLocateModal"
          @location-selected="setLocationValue"
          @close="showLocateModal = false"
        />
        <p v-if="successAccountMsg" class="success-message">
          {{ successAccountMsg }}
        </p>
        <p v-if="errorAccountMsg" class="error-message">
          {{ errorAccountMsg }}
        </p>
        <!--button v-if="!successAccountMsg" class="classic-button" type="submit">
          PLANIFY
        </button>
        <button
          v-else
          class="classic-button"
          type="button"
          @click="clearMessages"
        >
          OK
        </button-->
        <h3 class="font-bold">ADD AN ACTIVITY</h3>
        <FetchListActivities />
        <h3 class="font-bold">CHOOSE START DATETIME</h3>
        <h3 class="font-bold">CHOOSE END DATEIME</h3>
        <div>
          <button
            type="button"
            v-if="!successMsg"
            @click=""
            class="classic-button"
          >
            SAVE CHANGES
          </button>
          <button
            type="button"
            v-else
            @click="clearMessages"
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
import LocateModal from '@/components/LocateModal.vue';
import FetchListActivities from '@/components/FetchListActivities.vue';

export default {
  name: 'PlannedActivitiesView',
  setup() {
    return {};
  },
  components: {
    LocateModal,
    FetchListActivities,
  },
  data() {
    return {
      //userId: Number,
      location: null,
      successAccountMsg: '',
      errorAccountMsg: '',
      showLocateModal: false,
    };
  },
  /*mounted() {
    this.planifyUserActivity();
  },*/
  methods: {
    setLocationValue(selectedLocation) {
      this.location = null;
      this.location = selectedLocation;
      this.showLocateModal = false;
    },
    async planifyUserActivity() {
      try {
        const response = await axios.post(
          `http://localhost:8020/planned-activities-list/`,
          {
            //user: userId,
            //activity: activityId,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
            },
          }
        );
        this.errorAccountMsg = '';
      } catch (error) {
        this.errorAccountMsg =
          error.response?.data?.error || 'An unexpected error occurred';
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
