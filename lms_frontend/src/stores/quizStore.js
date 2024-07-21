import { defineStore } from "pinia";
import axios from "axios";

export const useQuizStore = defineStore("quiz", {
	state: () => ({
		quizzes: [],
		quiz: {},
		quizInstructions: [],
		quizResult: {},
		quizzesResult: [],
		questionsWithAnswers: [],
		loading: false,
		error: null,
		submitted: false, // حالة لتتبع إذا ما تم إرسال الإجابات
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

		async fetchQuizInstructions(quizName) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_quiz_instruction",
					{
						params: {
							quiz_name: quizName,
						},
					}
				);
				if (response.data.status_code !== 200) {
					this.error =
						response.data.message || "An error occurred while fetching quiz instructions.";
				} else {
					this.quizInstructions = response.data.data;
				}
			} catch (error) {
				this.error = error.message || "An error occurred while fetching quiz instructions.";
			} finally {
				this.loading = false;
			}
		},

		async fetchQuiz(quizName, studentId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					`http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_quiz`,
					{
						params: {
							quiz_name: quizName,
							student_id: studentId,
						},
					}
				);
				console.log(response.data);
				if (response.data.status_code !== 200) {
					this.error = response.data.message || "An error occurred while fetching quiz .";
				} else {
					this.quiz = response.data.data;
				}
			} catch (error) {
				this.error = error.message || "An error occurred while fetching the quiz.";
			} finally {
				this.loading = false;
			}
		},

		async submitQuiz(data) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.post(
					`http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.create_quiz_attempt`,
					data
				);
				if (response.data.status_code === 200) {
					this.submitted = true;
					console.log(response.data.quiz_attempt_id);
					return response.data.quiz_attempt_id; // Return the quiz_attempt_id
				} else {
					this.error = response.data.message || "An error occurred while submitting the quiz.";
					return null;
				}
			} catch (error) {
				this.error = error.message || "An error occurred while submitting the quiz.";
				return null;
			} finally {
				this.loading = false;
			}
		},

		async fetchQuizResult(quizAttemptId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					`http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_quiz_result`,
					{
						params: { quiz_attempt_id: quizAttemptId },
					}
				);
				this.quizResult = response.data.data;
			} catch (error) {
				this.error = error.response?.data?.message || error.message;
			} finally {
				this.loading = false;
			}
		},

		async fetchQuizzesResult(courseName, studentId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_all_quiz_attempts",
					{
						params: {
							course_name: courseName,
							student_id: studentId,
						},
					}
				);
				this.quizzesResult = response.data.data;
			} catch (error) {
				this.error = error.message || "An error occurred while fetching quizzes result.";
			} finally {
				this.loading = false;
			}
		},
		async fetchQuizReview(quizAttemptId) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					`http://localhost:8080/api/method/academia.lms_api.student.quiz.quiz.get_quiz_attempt_details`,
					{
						params: {
							quiz_attempt_id: quizAttemptId,
						},
					}
				);
				if (response.data.status_code === 200) {
					this.questionsWithAnswers = response.data.questions_with_answers;
				} else {
					this.error = response.data.message || "An error occurred while fetching quiz details.";
				}
			} catch (error) {
				this.error = error.message || "An error occurred while fetching quiz details.";
			} finally {
				this.loading = false;
			}
		},
	},
});
