import { defineStore } from "pinia";
import axios from "axios";

export const useQuizStore = defineStore("quiz", {
	state: () => ({
		quizData: {
			title: "",
			course: "00",
			faculty_member: "ACAD-FM-00001",
			instruction: "",
			make_the_quiz_availability: 0,
			from_date: "",
			to_date: "",
			is_time_bound: 0,
			duration: "",
			multiple_attempts: 0,
			number_of_attempts: "",
			grading_basis: "",
			quiz_question: [],
		},
		gradingBasisOptions: [],
		questionTypes: [],
		questions: [],
		quizzes: [],
	}),
	actions: {
		async fetchQuizzes(courseName, facultyMember) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.quiz.get_quizzes_by_course_and_faculty",
					{
						params: {
							course: courseName,
							faculty_member: facultyMember,
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

		async fetchQuestionsByCourse(courseName, facultyMember) {
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.quiz.get_questions_by_course_and_faculty_member",
					{
						params: { course_name: courseName, faculty_member: facultyMember },
						headers: {
							"Content-Type": "application/json",
							Authorization: "token 0b88a69d4861506:a0640c80d24119a",
						},
					}
				);
				if (response.data.status_code === 200) {
					this.questions = response.data.data;
					console.log(this.questions);
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
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.quiz.get_grading_basis_options",
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: "token 0b88a69d4861506:a0640c80d24119a",
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
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.quiz.get_question_types",
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: "token 0b88a69d4861506:a0640c80d24119a",
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
				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.teacher.quiz.quiz.create_quiz",
					this.quizData,
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: "token 0b88a69d4861506:a0640c80d24119a",
						},
					}
				);
				if (response.status === 200) {
					console.log("Quiz created successfully");
					console.log(this.quizData);
				} else {
					console.error("Error creating quiz");
				}
			} catch (error) {
				console.error(
					"Error creating quiz:",
					error.response ? error.response.data : error
				);
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
