import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useAssessmentStore = defineStore("assessmentStore", {
	state: () => ({
		quizzes: [],
		assignments: [],
		assignmentDetails: null,
		loading: false,
		error: null,
		fieldErrors: {},
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
		async fetchAssignmentAssessment(assignmentSubmissionId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.get_assignment_assessment",
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
				return response.data.message.data;
			} catch (error) {
				this.error =
					error.message || "An error occurred while fetching assignment assessment.";
				return { status: "error", message: this.error };
			} finally {
				this.loading = false;
			}
		},
		async saveAssessment(payload) {
			this.loading = true;
			this.error = null;
			this.fieldErrors = {};
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
				if (response.data.message.status === "success") {
					return { status: "success" };
				} else if (response.data.message.status === "error") {
					throw new Error(response.data.message.message);
				}
			} catch (error) {
				if (error.response && error.response.status === 400) {
					this.error = error.response.data.message;
					this.fieldErrors.general = error.response.data.message;
				} else {
					this.error = error.message || "An error occurred while saving the assessment.";
					this.fieldErrors.general = this.error;
				}
				return { status: "error", message: this.error };
			} finally {
				this.loading = false;
			}
		},
		async fetchQuizAndAssignmentGrades(facultyMember, course) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assessment.get_quiz_and_assignment_grades",
					{
						params: {
							faculty_member: facultyMember,
							course: course,
						},
					},
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				console.log(response);
				this.quizzes = response.data.message.quizzes;
				this.assignments = response.data.message.assignments;
			} catch (error) {
				this.error = error.message || "An error occurred while fetching grades.";
			} finally {
				this.loading = false;
			}
		},
	},
});
