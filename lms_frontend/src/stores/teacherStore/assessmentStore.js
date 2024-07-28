import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useAssessmentStore = defineStore("assessmentStore", {
	state: () => ({
		assignments: [],
		assignmentDetails: null,
		loading: false,
		error: null,
	}),
	actions: {
		async fetchAssignments() {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.fetch_submitted_assignments_for_faculty_member",
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				this.assignments = response.data.submitted_assignments;
			} catch (error) {
				this.error = error.message || "An error occurred while fetching assignments.";
			} finally {
				this.loading = false;
			}
		},
		async fetchAssignmentDetails(assignmentSubmissionId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.fetch_assignment_details",
					{
						params: {
							assignment_submission_id: assignmentSubmissionId,
						},
					},
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				this.assignmentDetails = response.data.message;
			} catch (error) {
				this.error =
					error.message || "An error occurred while fetching assignment details.";
			} finally {
				this.loading = false;
			}
		},
		async saveAssessment(payload) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.save_assignment_assessment",
					payload,
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				console.log(response.data );
				if (response.data.message.status === "success") {
					alert("Assessment saved successfully!");
				} else {
					alert(`Error: ${response.data.message}`);
				}
			} catch (error) {
				this.error = error.message || "An error occurred while saving the assessment.";
				alert(this.error);
			} finally {
				this.loading = false;
			}
		},
	},
});
