import { defineStore } from "pinia";
import axios from "axios";

export const useAssignmentStore = defineStore("assignment", {
	state: () => ({
		assignments: [],
		assignmentDetails: null,
		loading: false,
		error: null,
	}),
	actions: {
		async fetchAssignments(courseName, studentId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.assignment.get_assignments_by_course",
					{
						params: {
							course_name: courseName,
							student_id: studentId,
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
		async fetchAssignmentDetails(assignmentName) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.assignment.get_assignment",
					{
						params: {
							assignment_name: assignmentName,
						},
					}
				);
				this.assignmentDetails = response.data.data;
			} catch (error) {
				this.error =
					error.message || "An error occurred while fetching the assignment details.";
			} finally {
				this.loading = false;
			}
		},
		async submitAssignment(data) {
			try {
				console.log("Submitting data:", data); // Debugging line
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.student.assignment.create_assignment_submission",
					data,
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: "token 209d178aa3fed8b:37cdbe81b02b42b",
						},
					}
				);
				return response.data;
			} catch (error) {
				console.error("Submission error:", error.response.data); // Debugging line
				throw new Error(
					error.response.data.message ||
						"An error occurred while submitting the assignment."
				);
			}
		},
	},
});
