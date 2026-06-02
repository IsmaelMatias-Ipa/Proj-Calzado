import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import ScannerView from "../views/ScannerView.vue";
import CatalogView from "../views/CatalogView.vue";
import CheckoutView from "../views/CheckoutView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/scanner", component: ScannerView },
  { path: "/catalog", component: CatalogView },
  { path: "/checkout", component: CheckoutView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
