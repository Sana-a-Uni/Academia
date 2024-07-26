import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";
import router from "../router";

export const useAuthStore = defineStore("auth", {
	state: () => ({
		user: null,
		userDetails: {},
		userRoles: [],
		error: null,
	}),
	actions: {
		async login(username, password) {
			try {
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.login.login",
					{ username, password }
				);

				if (response.data && response.data.message === true) {
					const { user_details, user_role, key_details } = response.data;

					if (user_details && user_role && key_details) {
						this.userDetails = user_details;
						this.userRoles = user_role;
						this.user = `${user_details[0].first_name} ${user_details[0].last_name}`;
						this.error = null;

						const token = `token ${key_details.api_key}:${key_details.api_secret}`;
						Cookies.set("authToken", token, { expires: 7 });
						Cookies.set("role", this.userRoles[0], { expires: 7 });
					} else {
						this.error = "Incomplete data received from server";
					}
				} else {
					this.error = "Login failed";
				}
			} catch (error) {
				this.error = error.response?.data?.message || "An error occurred during login";
			}
		},
		
	},
});
