<template>
  <div class="multiselect-container">
    <div>
      <h3 class="font-bold">YOUR FAVORITE ACTIVITIES</h3>
    </div>
    <div>
      <vue-multiselect
        v-model="selectedActivities"
        :options="activitiesList"
        :multiple="true"
        :taggable="false"
        :close-on-select="false"
        :clear-on-select="false"
        :preserve-search="true"
        placeholder="Select activities"
        label="name"
        track-by="id"
        @update="saveUserActivities"
      >
        <template v-slot:option="{ option }">
          <div>
            <span>{{ option.name }}</span>
            <span class="activity-description">{{ option.description }}</span>
          </div>
        </template>
        Select activities
      </vue-multiselect>
    </div>
    <div>
      <p v-if="successMsg" class="success-message">{{ successMsg }}</p>
      <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
    </div>
    <div>
      <button
        type="button"
        v-if="!successMsg"
        @click="saveUserActivities"
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
  </div>
</template>

<script>
import axios from 'axios';
import VueMultiselect from 'vue-multiselect';

export default {
  name: 'FethcActivities',
  components: {
    VueMultiselect,
  },
  data() {
    return {
      activitiesList: [],
      selectedActivities: [],
      successMsg: '',
      errorMsg: '',
    };
  },
  mounted() {
    this.fetchActivitiesList();
  },
  methods: {
    // async method to retreive the list of activities
    async fetchActivitiesList() {
      try {
        const response = await axios.get(
          'http://localhost:8020/activities-list/',
          {
            headers: {
              Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
            },
          }
        );
        this.activitiesList = response.data;
        this.fetchSelectedActivities();
      } catch (error) {
        this.errorMsg = `Error fetching activities list: ${error}`;
      }
    },
    // async method to retreive activities of a user
    async fetchSelectedActivities() {
      try {
        const response = await axios.get(
          'http://localhost:8020/user-activities-list/',
          {
            headers: {
              Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
            },
          }
        );
        this.currentDbActivities = response.data;
        this.selectedActivities = this.activitiesList.filter((activity) =>
          response.data.some(
            (userActivity) => userActivity.activity === activity.id
          )
        );
      } catch (error) {
        this.errorMsg = `Error fetching selected activities: ${error}`;
      }
    },
    // method to save and apply chages to database
    async saveUserActivities() {
      const userId = this.$store.getters.getUserId;
      const activitiesToDelete = this.currentDbActivities.filter(
        (dbActivity) =>
          !this.selectedActivities.some(
            (selected) => selected.id === dbActivity.activity
          )
      );
      const activitiesToCreate = this.selectedActivities.filter(
        (selected) =>
          !this.currentDbActivities.some(
            (dbActivity) => dbActivity.activity === selected.id
          )
      );
      for (const activityToDelete of activitiesToDelete) {
        try {
          await axios.delete(
            `http://localhost:8020/user-activity-detail/${activityToDelete.id}/`,
            {
              headers: {
                Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
              },
            }
          );
        } catch (error) {
          this.errorMsg = `Error deleting user activity: ${error}`;
        }
      }
      for (const activityToCreate of activitiesToCreate) {
        try {
          await axios.post(
            'http://localhost:8020/user-activities-list/',
            {
              user: userId,
              activity: activityToCreate.id,
            },
            {
              headers: {
                Authorization: `Bearer ${this.$store.getters.getAccessToken}`,
              },
            }
          );
        } catch (error) {
          this.errorMsg = `Error creating user activity: ${error}`;
        }
      }
      this.successMsg = 'User activities updated successfully.';
    },
    clearMessages() {
      this.successMsg = '';
      this.errorMsg = '';
    },
  },
};
</script>

<style scoped lang="postcss">
.multiselect-container {
  @apply flex flex-col justify-start items-center gap-y-3;
}

.activity-description {
  @apply font-extralight italic text-wrap ml-3 p-2;
}
</style>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
