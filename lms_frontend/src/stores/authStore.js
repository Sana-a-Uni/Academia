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
        roleError: false,
    }),
    actions: {
        async login(username, password) {
            try {
                const response = await axios.post(
                    "http://localhost:8080/api/method/academia.lms_api.auth.login",
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

                        const validRoles = ["teacher", "Student"];
                        const roleToSet = validRoles.find((validRole) =>
                            user_role.includes(validRole)
                        );

                        if (roleToSet) {
                            Cookies.set("role", roleToSet, { expires: 7 });
                        } else {
                            this.roleError = true;
                        }
                    } else {
                        this.error = "Incomplete data received from server";
                    }
                } else {
                    this.error = "Invalid login, try again";
                }
            } catch (error) {
                this.error = "Invalid login, try again";
            }
        },
        async logout() {
            try {
                const response = await axios.post(
                    "http://localhost:8080/api/method/academia.lms_api.auth.logout"
                );

                if (response.data.message === true) {
                    this.user = null;
                    this.userDetails = {};
                    this.userRoles = [];
                    this.error = null;

                    Cookies.remove("authToken");
                    Cookies.remove("role");

                    router.push({ name: "login" });
                } else {
                    this.error = "Logout failed";
                }
            } catch (error) {
                this.error = error.response?.data?.message || "An error occurred during logout";
            }
        }
    }
});
