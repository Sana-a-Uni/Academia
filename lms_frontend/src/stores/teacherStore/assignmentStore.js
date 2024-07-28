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
	}),
	actions: {
		async fetchAssignments(courseName) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assignment.fetch_assignments_for_course",
					{
						params: {
							course: courseName,
						},
					},
					{
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
				if (response.status === 200) {
					console.log("Assignment created successfully");
					console.log(this.assignmentData);
				} else {
					console.error("Error creating assignment");
				}
			} catch (error) {
				console.error(
					"Error creating assignment:",
					error.response ? error.response.data : error
				);
			}
		},
		updateAssignmentData(partialData) {
			this.assignmentData = { ...this.assignmentData, ...partialData };
		},
	},
});
