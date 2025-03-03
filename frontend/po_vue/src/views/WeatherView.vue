<template>
  <div class="standard-container">
    <div class="standard-item">
      <h2 class="text-center font-bold" v-if="success">
        Weather at {{ city }}
      </h2>
      <h3 class="text-center" v-else>No weather data or bad city name</h3>
      <p class="text-center text-sm italic" v-if="!userLoggedIn">
        You must be logged in to see details
      </p>
    </div>
    <div v-show="success" class="weather-container">
      <div v-for="(item, index) in forecast" :key="index" class="weather-item">
        <p>
          {{ item.date }}
        </p>
        <p>
          MIN: {{ item.temperature.min_C }} °C / {{ item.temperature.min_F }} °F
        </p>
        <p>
          MAX: {{ item.temperature.max_C }} °C / {{ item.temperature.max_F }} °F
        </p>
        <img
          v-if="item.weather_icon"
          :src="`${urlIcon}/${item.weather_icon}.svg`"
          :alt="item.weather"
          class="object-center"
        />
        <button
          :disabled="!userLoggedIn"
          type="button"
          class="classic-button"
          @click="goToDetails(item)"
        >
          Details
        </button>
      </div>
    </div>
    <LoginModal v-if="showModal" :show="showModal" @close="showModal = false" />
  </div>
</template>

<script>
import axios from 'axios';
import LoginModal from '@/components/LoginModal.vue';

export default {
  name: 'WeatherView',
  components: {
    LoginModal,
  },
  props: {
    city: {
      type: String,
      required: true,
    },
    lat: {
      type: [Number, String],
      required: true,
    },
    lon: {
      type: [Number, String],
      required: true,
    },
  },
  data() {
    return {
      //city: '',
      forecast: {},
      success: false,
      showModal: false,
    };
  },
  mounted() {
    this.fetchWeatherData();
  },
  computed: {
    userLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    async fetchWeatherData() {
      try {
        this.success = false;
        const response = await axios.get(
          `http://localhost:8020/weather/${this.lat}/${this.lon}/`
        );
        this.forecast = response.data.data;
        this.urlIcon = response.data.url_icon;
        this.success = true;
      } catch (error) {
        console.error('Request error:', error);
        this.success = false;
      }
    },
    goToDetails(item) {
      this.$router.push({
        name: 'weather-details',
        params: {
          itemCity: this.city,
          lat: this.lat,
          lon: this.lon,
          itemId: item.day_id,
        },
      });
    },
  },
};
</script>

<style scoped lang="postcss"></style>
