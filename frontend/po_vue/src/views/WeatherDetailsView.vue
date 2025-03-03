<template>
  <div class="standard-container">
    <div class="standard-item">
      <h2 class="text-center font-bold">Weather at {{ itemCity }}</h2>
      <h2 class="text-center">{{ forecastDetails.date }}</h2>
    </div>
    <div v-if="success" class="weather-container">
      <div class="weather-item">
        <p class="font-medium">TEMPERATURES</p>
        <p>
          MIN: {{ forecastDetails.temperature.min_C }} °C /
          {{ forecastDetails.temperature.min_F }} °F
        </p>
        <p>
          MAX: {{ forecastDetails.temperature.max_C }} °C /
          {{ forecastDetails.temperature.max_F }} °F
        </p>
        <p>iso0</p>
        <p>
          {{ forecastDetails.iso0.meters }} m /
          {{ forecastDetails.iso0.feet }} ft
        </p>
        <img
          v-if="forecastDetails.weather_icon"
          :src="`${urlIcon}/${forecastDetails.weather_icon}.svg`"
          :alt="forecastDetails.weather"
          class="object-center"
        />
      </div>
      <div class="weather-item">
        <p>uv: {{ forecastDetails.uv }}</p>
        <p>Sunrise: {{ forecastDetails.sunrise }}</p>
        <p>Sunset: {{ forecastDetails.sunset }}</p>
        <p class="font-medium">WIND</p>
        <p>
          Speed: {{ forecastDetails.wind.speed_kmh }} km/h /
          {{ forecastDetails.wind.speed_mph }} mph
        </p>
        <p>Direction: {{ forecastDetails.wind.direction }}</p>
        <p class="font-medium">HUMIDITY</p>
        <p>
          MIN: {{ forecastDetails.humidity.min }} % / MAX:
          {{ forecastDetails.humidity.max }} %
        </p>
      </div>
    </div>
    <div v-else>
      <p>No data available for the selected date.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'WeatherDetailsView',
  components: {},
  props: {
    itemCity: {
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
    itemId: {
      type: [Number, String],
      required: true,
    },
  },
  data() {
    return {
      forecastDetails: {},
      success: false,
      //itemCity: '',
    };
  },
  computed: {
    getAccessToken() {
      return this.$store.getters.getAccessToken;
    },
  },
  mounted() {
    this.fetchWeatherDetailsData();
  },
  methods: {
    async fetchWeatherDetailsData() {
      try {
        this.success = false;
        const response = await axios.get(
          `http://localhost:8020/weather-details/${this.lat}/${this.lon}/${this.itemId}/`,
          {
            headers: {
              Authorization: `Bearer ${this.getAccessToken}`,
            },
          }
        );
        this.urlIcon = response.data.url_icon;
        this.forecastDetails = response.data.data;
        this.success = true;
      } catch (error) {
        console.error('Request error:', error);
        this.success = false;
      }
    },
  },
};
</script>

<style scoped lang="postcss"></style>
