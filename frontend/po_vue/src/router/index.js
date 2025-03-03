import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import WeatherView from "../views/WeatherView.vue";
import WeatherDetailsView from "../views/WeatherDetailsView.vue";
import RegisterView from "../views/RegisterView.vue";
import PasswordResetConfirmView from "../views/PasswordResetConfirmView.vue";
import AccountManagerView from "../views/AccountManagerView.vue";


const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/weather/:city/:lat/:lon",
    name: "weather",
    component: WeatherView,
    props: true
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/auth/password-reset-confirm/:uid/:token",
    name: "password-reset-confirm",
    component: PasswordResetConfirmView,
  },
  {
    path: "/account",
    name: "account",
    component: AccountManagerView,
  },
  {
    path: "/weather-details/:itemCity/:lat/:lon/:itemId",
    name: "weather-details",
    component: WeatherDetailsView,
    props: true
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
