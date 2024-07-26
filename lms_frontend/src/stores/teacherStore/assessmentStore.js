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
	},
});
