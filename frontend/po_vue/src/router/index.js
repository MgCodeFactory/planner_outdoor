import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import WeatherView from "../views/WeatherView.vue";
import WeatherDetailsView from "../views/WeatherDetailsView.vue";
import CreateAccountView from "../views/CreateAccountView.vue";
import AccountManagerView from "../views/AccountManagerView.vue";


const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/weather",
    name: "weather",
    component: WeatherView,
  },
  {
    path: "/login",
    name: "login",
    component: CreateAccountView,
  },
  {
    path: "/account",
    name: "account",
    component: AccountManagerView,
  },
  {
    path: "/weather-details/:itemCity/:itemDt",
    name: "WeatherDetails",
    component: WeatherDetailsView,
  },
  {
    //path: "/about",
    //name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    //component: () =>
    //  import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
