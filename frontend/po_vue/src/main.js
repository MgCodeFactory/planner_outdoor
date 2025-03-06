import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import './tailwindcss/index.css';
import VCalendar from 'v-calendar';
import 'v-calendar/style.css';

const app = createApp(App);

app.use(VCalendar, {})
app.use(store).use(router).mount("#app");
