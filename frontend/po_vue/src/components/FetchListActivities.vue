<template>
  <div class="multiselect-container">
    <div>
      <vue-multiselect
        v-model="selectedActivity"
        :options="activitiesList"
        :multiple="false"
        :taggable="false"
        :close-on-select="true"
        @select="() => {}"
        :clear-on-select="false"
        :preserve-search="true"
        placeholder="Select an activity"
        label="name"
        track-by="id"
      >
        <template v-slot:option="{ option }">
          <div>
            <span>{{ option.name }}</span>
            <span class="activity-description">{{ option.description }}</span>
          </div>
        </template>
        Select an activity
      </vue-multiselect>
    </div>
    <div>
      <p v-if="successMsg" class="success-message">{{ successMsg }}</p>
      <p v-if="errorMsg" class="error-message">{{ errorMsg }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import VueMultiselect from 'vue-multiselect';

export default {
  name: 'FetchListActivities',
  components: {
    VueMultiselect,
  },
  data() {
    return {
      activitiesList: [],
      selectedActivity: null,
      successMsg: '',
      errorMsg: '',
    };
  },
  mounted() {
    this.fetchListActivities();
  },
  methods: {
    async fetchListActivities() {
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
      } catch (error) {
        this.errorMsg = `Error fetching activities list: ${error}`;
      }
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
