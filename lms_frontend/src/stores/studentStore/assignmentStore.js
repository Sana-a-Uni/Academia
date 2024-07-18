import { defineStore } from "pinia";
import axios from "axios";

export const useAssignmentStore = defineStore("assignment", {
	state: () => ({
		assignments: [],
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
	},
});
