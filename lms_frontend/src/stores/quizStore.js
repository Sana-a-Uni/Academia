import { defineStore } from "pinia";
import axios from "axios";

export const useQuizStore = defineStore("quiz", {
	state: () => ({
		quizzes: [],
		quiz: {},
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

		async fetchQuiz(quizName) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					`http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_quiz`,
					{
						params: {
							quiz_name: quizName,
						},
						headers: {
							Authorization: "Bearer 0b88a69d4861506:536f9ea01265e49",
						},
					}
				);

				this.quiz = response.data.data;
				console.log(response.data.data);
			} catch (error) {
				this.error = error.message || "An error occurred while fetching the quiz.";
				console.log("errrrrrrrrrrror");
			} finally {
				this.loading = false;
			}
		},
	},
});
