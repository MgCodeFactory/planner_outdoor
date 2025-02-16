<template>
  <div class="standard-container">
    <div class="standard-item">
      <h2 v-if="success">Weather at {{ city }}</h2>
      <h3 v-else>No weather data or bad city name</h3>
    </div>
    <div v-show="success" class="weather-container">
      <div class="weather-item">
        <div
          v-for="(item, index) in forecast"
          :key="index"
          @click="goToDetails(item)"
        >
          <p>
            {{ item.date.year }} - {{ item.date.month }} - {{ item.date.day }}
          </p>
          <p>
            MIN: {{ item.temperature.min_C }} °C /
            {{ item.temperature.min_F }} °F
          </p>
          <p>
            MAX: {{ item.temperature.max_C }} °C /
            {{ item.temperature.max_F }} °F
          </p>
          <img
            v-if="item.weather_icon"
            :src="`${urlIcon}/${item.weather_icon}.svg`"
            :alt="item.weather"
            class="object-center"
          />
          <button
            type="button"
            class="classic-button"
            @click="goToDetails(item)"
          >
            Details
          </button>
        </div>
      </div>
      <LoginModal
        v-if="showModal"
        :show="showModal"
        @close="showModal = false"
      />
    </div>
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
  data() {
    return {
      city: {},
      forecast: {},
      success: false,
      showModal: false,
    };
  },
  created() {
    this.fetchWeatherData();
  },
  watch: {
    '$route.query.city': 'fetchWeatherData',
    '$route.query.lat': 'fetchWeatherData',
    '$route.query.lon': 'fetchWeatherData',
  },
  computed: {
    userLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    async fetchWeatherData() {
      try {
        const city = this.$route.query.city;
        const lat = this.$route.query.lat;
        const lon = this.$route.query.lon;
        this.success = false;
        const response = await axios.get(
          `http://localhost:8020/weather/${lat}/${lon}/`
        );
        this.city = city;
        this.forecast = response.data.data;
        this.urlIcon = response.data.url_icon;
        this.success = true;
      } catch (error) {
        console.error('Request error:', error);
        this.success = false;
      }
    },
    goToDetails(item) {
      if (this.userLoggedIn) {
        this.$router.push({
          name: 'weather-details',
          params: {
            itemCity: this.city,
            itemDt: item.dt,
          },
          query: {
            lat: this.$route.query.lat,
            lon: this.$route.query.lon,
          },
        });
      } else {
        this.showModal = true;
      }
    },
  },
};
</script>

<style scoped lang="postcss"></style>
