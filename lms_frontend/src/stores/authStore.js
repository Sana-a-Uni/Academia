// src/stores/authStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
	state: () => ({
		user: null,
		apiKey: "",
		apiSecret: "",
		userDetails: {},
		userRoles: [],
		error: null,
	}),
	actions: {
		async login(username, password) {
			try {
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.login.login",
					{
						username,
						password,
					}
				);
				if (response.data.message === true) {
					this.apiKey = response.data.key_details.api_key;
					this.apiSecret = response.data.key_details.api_secret;
					this.userDetails = response.data.user_details;
					this.userRoles = response.data.user_role;
					this.user =
						response.data.user_details[0].first_name +
						" " +
						response.data.user_details[0].last_name;
					this.error = null;
				} else {
					this.error = "Login failed";
				}
			} catch (error) {
				this.error = error.response.data.message || "An error occurred during login";
			}
		},
	},
});
