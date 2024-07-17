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

	
	},
});
