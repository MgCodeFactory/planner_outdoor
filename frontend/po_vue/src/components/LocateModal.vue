<template>
  <Teleport to="body">
    <div v-if="show" class="modal-background">
      <form @submit.prevent="fetchSelections" class="modal-container">
        <div class="modal-item-header">
          <input
            type="text"
            v-model="city"
            placeholder="Enter a city name..."
            @input="fetchSelections"
          />
        </div>
        <div class="modal-item-content">
          <ul v-if="selections.length">
            <li
              v-for="(selection, index) in selections"
              :key="index"
              @click="selectCity(selection)"
            >
              {{ selection.name ? selection.name : 'Unknown' }},
              {{ selection.country ? selection.country : 'Unknown' }}
            </li>
          </ul>
        </div>
        <div class="modal-item-footer" @click="$emit('close')">
          <h4>CLOSE</h4>
        </div>
      </form>
    </div>
  </Teleport>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LocateView',
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
        this.$router.push({
          name: 'weather',
          query: {
            city: this.city,
            lat: selection.lat,
            lon: selection.lon,
          },
        });
        this.city = '';
        this.$emit('close');
      } else {
        console.error('Invalid selection object:', selection);
      }
    },
  },
};
</script>

<style scoped>
input {
  height: 100%;
  height: 100%;
  border: none;
  outline: none;
  background-color: transparent;
  color: var(--color-white);
  text-align: center;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  color: var(--color-black);
  text-align: center;
}

li {
  color: var(--color-black);
  font-size: var(--font-size-small);
  padding: 8px;
  cursor: pointer;
}

li:hover {
  background-color: var(--color-white);
}

.modal-item-footer:hover {
  cursor: pointer;
  background: var(--color-white);
  color: var(--color-black);
}
</style>
