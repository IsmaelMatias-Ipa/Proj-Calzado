import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    shoeSize: "",
    accessToken: "",
    userEmail: "",
    subscriptionStatus: "",
  }),
  actions: {
    setSize(size) {
      this.shoeSize = size;
    },
    setToken(token) {
      this.accessToken = token;
    },
    setEmail(email) {
      this.userEmail = email;
    },
    setSubscriptionStatus(status) {
      this.subscriptionStatus = status;
    },
  },
});
