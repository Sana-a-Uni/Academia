import { defineStore } from "pinia";
import axios from "axios";

export const useQuizStore = defineStore("quiz", {
	state: () => ({
		quizzes: [],
		quizInstructions: [],
		loading: false,
		error: null,
	}),
	actions: {
		async fetchQuizzes(courseName, studentId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_quizzes_by_course",
					{
						params: {
							course_name: courseName,
							student_id: studentId,
						},
					}
				);
				this.quizzes = response.data.data;
			} catch (error) {
				this.error = error.message || "An error occurred while fetching quizzes.";
			} finally {
				this.loading = false;
			}
		},

		async fetchQuizInstructions(quizName, studentId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_quiz_instruction",
					{
						params: {
							quiz_name: quizName,
							student_id: studentId,
						},
					}
				);
				this.quizInstructions = response.data.data;
			} catch (error) {
				this.error = error.message || "An error occurred while fetching quiz instructions.";
			} finally {
				this.loading = false;
			}
		},
	},
});
