<template>
  <div class="router-container">
    <div class="main-item">
      <h2 v-if="success">Weather at {{ city }}</h2>
      <h3 v-else>No weather data or bad city name</h3>
    </div>
    <div v-show="success" class="weather-container">
      <div
        v-for="(item, index) in forecast"
        :key="index"
        class="weather-item"
        @click="goToDetails(item)"
      >
        <p>
          {{ item.date.year }} - {{ item.date.month }} - {{ item.date.day }}
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
        />
        <!--p><button @click="goToDetails(item)">Details</button></p-->
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

<style scoped>
.main-item {
  background-color: var(--color-background-item);
  border: 2px solid var(--color-light-grey);
  margin: 10px;
  padding: 20px;
  align-self: center;
  text-align: center;
  flex-grow: 1;
}

.weather-container {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  gap: 20px;
  flex-grow: 19;
  margin-bottom: var(--margin-header-footer);
  padding-bottom: 20px;
}

.weather-item {
  background-color: var(--color-background-item);
  border: 1px solid var(--color-light-grey);
  margin: 10px;
  padding: 20px;
  min-width: 200px;
  max-height: 330px;
  text-align: center;
  font-size: var(--font-size-medium);
}

.weather-item:hover {
  border: solid 1px var(--color-black);
  cursor: pointer;
}



button {
  height: 30px;
  width: 80px;
  background-color: var(--color-button);
  border: 0;
  font-family: var(--font-family);
  color: var(--color-white);
  cursor: pointer;
}
</style>
