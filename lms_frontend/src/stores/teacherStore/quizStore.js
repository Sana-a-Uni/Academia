import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useQuizStore = defineStore("quiz", {
	state: () => ({
		quizData: {
			title: "",
			course: "00",
			instruction: "",
			make_the_quiz_availability: false,
			from_date: "",
			to_date: "",
			is_time_bound: false,
			duration: 0,
			multiple_attempts: false,
			number_of_attempts: 1,
			grading_basis: "",
			quiz_question: [],
			show_question_score: false,
			show_correct_answer: false,
			randomize_question_order: false,
			randomize_option_order: false,
		},
		gradingBasisOptions: [],
		questionTypes: [],
		questions: [],
		quizzes: [],
		errors: {},
	}),
	actions: {
		async fetchQuizzes(courseName) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.fetch_quizzes_for_course",
					{
						params: {
							course: courseName,
						},
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
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

		async fetchCourseQuestions(courseName) {
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.fetch_course_questions",
					{
						params: { course_name: courseName },
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				if (response.data.status_code === 200) {
					this.questions = response.data.data;
				} else {
					console.error("Error fetching questions");
				}
			} catch (error) {
				console.error(
					"Error fetching questions:",
					error.response ? error.response.data : error
				);
			}
		},

		async fetchGradingBasisOptions() {
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.fetch_grading_basis_options",
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				if (response.data.status_code === 200) {
					this.gradingBasisOptions = response.data.data;
				} else {
					console.error("Error fetching grading basis options");
				}
			} catch (error) {
				console.error(
					"Error fetching grading basis options:",
					error.response ? error.response.data : error
				);
			}
		},
		async fetchQuestionTypes() {
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.fetch_question_types",
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				if (response.data.status_code === 200) {
					this.questionTypes = response.data.data;
				} else {
					console.error("Error fetching question types");
				}
			} catch (error) {
				console.error(
					"Error fetching question types:",
					error.response ? error.response.data : error
				);
			}
		},
		async createQuiz() {
			try {
				this.errors = {};
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.create_quiz",
					this.quizData,
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				if (response.data.status_code === 200) {
					console.log("Quiz created successfully");
					return true;
				} else {
					if (response.data.status_code == 400) {
						this.errors = response.data.errors;
					}
					return false;
				}
			} catch (error) {
				if (error.response && error.response.data && error.response.data.message) {
					this.errors = error.response.data.message;
				} else {
					console.error(
						"Error creating quiz:",
						error.response ? error.response.data : error
					);
				}
				return false;
			}
		},

		setQuizData(data) {
			this.quizData = data;
		},
		updateQuizData(partialData) {
			this.quizData = { ...this.quizData, ...partialData };
		},
		addQuestion(question) {
			this.quizData.quiz_question.push(question);
		},
	},
});
