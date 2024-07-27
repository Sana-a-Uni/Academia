import { defineStore } from "pinia";
import axios from "axios";

export const useAssessmentStore = defineStore("assessmentStore", {
	state: () => ({
		assignments: [],
		assignmentDetails: null,
		loading: false,
		error: null,
	}),
	actions: {
		async fetchAssignments(facultyMemberId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.get_submitted_assignments_by_faculty_member",
					{
						params: {
							faculty_member_id: facultyMemberId,
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
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.get_assignment_details",
					{
						params: {
							assignment_submission_id: assignmentSubmissionId,
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
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.save_assessment",
					payload,
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: "token 0b88a69d4861506:a0640c80d24119a",
						},
					}
				);
				if (response.data.message.status=== "success") {
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
