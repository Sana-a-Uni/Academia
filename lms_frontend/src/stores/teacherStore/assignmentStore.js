import { defineStore } from "pinia";
import axios from "axios";

export const useAssignmentStore = defineStore("assignment", {
	state: () => ({
		assignmentData: {
			assignment_title: "",
			course: "00",
			faculty_member: "ACAD-FM-00001",
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
		async fetchAssignments(courseName, facultyMember) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.assignment.get_assignments_by_course_and_faculty",
					{
						params: {
							course: courseName,
							faculty_member: facultyMember,
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
							Authorization: "token 0b88a69d4861506:a0640c80d24119a",
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
