import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useAssignmentStore = defineStore("assignment", {
	state: () => ({
		assignmentData: {
			assignment_title: "",
			course: "00",
			instruction: "",
			make_the_assignment_availability: false,
			from_date: "",
			to_date: "",
			question: "",
			assessment_criteria: [],
			attachments: [],
		},
		assignments: [],
		loading: false,
		error: null,
		errors: {}, // For holding validation errors
	}),
	actions: {
		async fetchAssignments(courseName) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assignment.fetch_assignments_for_course",
					{
						params: { course: courseName },
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				this.assignments = response.data.data;
			} catch (error) {
				this.error = error.message || "An error occurred while fetching assignments.";
			} finally {
				this.loading = false;
			}
		},

		async createAssignment() {
			this.errors = {};
			try {
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assignment.create_assignment",
					this.assignmentData,
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				if (response.data.status_code === 200) {
					return { success: true };
				} else {
					if (response.data.status_code === 400) {
						this.errors = response.data.errors;
					}
					return { success: false };
				}
			} catch (error) {
				if (error.response && error.response.data && error.response.data.errors) {
					this.errors = error.response.data.errors;
				} else {
					this.error = error.message || "An error occurred while creating assignment.";
				}
				return { success: false };
			}
		},

		updateAssignmentData(partialData) {
			this.assignmentData = { ...this.assignmentData, ...partialData };
		},
	},
});
