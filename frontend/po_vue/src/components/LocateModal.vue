<template>
  <Teleport to="body">
    <div v-if="show" class="modal-background">
      <div class="modal-container">
        <form @submit.prevent="fetchSelections" class="form-container">
          <div>
            <input
              class="locate-input"
              type="text"
              v-model="city"
              placeholder="Enter a city name..."
              @input="fetchSelections"
            />
          </div>
          <div class="locate-ul">
            <ul v-if="selections.length">
              <li
                class="locate-li"
                v-for="(selection, index) in selections"
                :key="index"
                @click="selectCity(selection)"
              >
                {{ selection.name ? selection.name : 'Unknown' }},
                {{ selection.country ? selection.country : 'Unknown' }}
              </li>
            </ul>
          </div>
          <button class="classic-button" @click="$emit('close')">CLOSE</button>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';

export default {
  name: 'LocateModal',
  emits: ['location-selected', 'close'],
  setup() {
    const route = useRoute();
    return { route };
  },
  props: {
    show: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      city: '',
      selections: [],
    };
  },
  methods: {
    async fetchSelections() {
      if (this.city.length > 3) {
        try {
          const response = await axios.get(
            `http://localhost:8020/geocoding/${this.city}/`
          );
          this.selections = response.data.data || [];
        } catch (error) {
          console.error('Error fetching city selections:', error);
          this.selections = [];
        }
      } else {
        this.selections = [];
      }
    },
    selectCity(selection) {
      if (selection && selection.name && selection.country) {
        this.city = `${selection.name}, ${selection.country}`;
        this.selections = [];
        console.log(`route name: ${this.route.name}`)
        if (this.route.name === 'register') {
          this.$emit('location-selected', {
            name: selection.name,
            lat: selection.lat,
            lon: selection.lon,
            country: selection.country,
          });
        } else {
          this.$router.push({
            name: 'weather',
            query: {
              city: this.city,
              lat: selection.lat,
              lon: selection.lon,
            },
          });
        }
        this.city = '';
        this.$emit('close');
      } else {
        console.error('Invalid selection object:', selection);
      }
    },
  },
};
</script>

<style scoped lang="postcss">
.locate-input {
  @apply bg-zinc-100 border border-zinc-300 focus:ring-2 rounded-md font-bold p-2;
}

.locate-ul {
  @apply w-full max-h-60 overflow-y-auto;
}
.locate-li {
  @apply py-2 px-4 hover:bg-gray-200 font-bold cursor-pointer;
}
</style>
