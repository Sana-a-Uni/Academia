import { defineStore } from "pinia";
import axios from "axios";

export const useAssignmentStore = defineStore("assignment", {
	state: () => ({
		assignments: [],
		assignmentDetails: null,
		loading: false,
		error: null,
		previousSubmission: null,
		previousSubmissionFiles: [], 
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
		async fetchPreviousSubmission(assignmentName, studentId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					`http://localhost:8080/api/method/academia.lms_api.student.assignment.get_assignment_and_submission_details`,
					{
						params: {
							assignment: assignmentName,
							student: studentId,
						},
					}
				);
				this.previousSubmission = response.data.previous_submission;
				this.previousSubmissionFiles = response.data.files; 
			} catch (error) {
				console.error("Error fetching previous submission:", error);
				this.error = "Error fetching previous submission.";
			} finally {
				this.loading = false;
			}
		},
		async deleteAttachment(fileUrl) {
			try {
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.student.assignment.delete_attachment",
					{ file_url: fileUrl },
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: "token 209d178aa3fed8b:37cdbe81b02b42b",
						},
					}
				);
				return response.data;
			} catch (error) {
				console.error("Error deleting file:", error);
				throw error;
			}
		},
		async submitAssignment(data) {
			try {
				console.log("Submitting data:", data);
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
				console.error("Submission error:", error.response.data);
				let errorMessage =
					error.response.data.message ||
					"An error occurred while submitting the assignment.";

				if (error.response.data.exception.includes("UpdateAfterSubmitError")) {
					errorMessage =
						"Cannot update a submitted assignment. Please create a new submission.";
				}

				throw new Error(errorMessage);
			}
		},
	},
});
