import { defineStore } from "pinia";
import axios from "axios";

export const useQuizStore = defineStore("quiz", {
	state: () => ({
		quizData: {
			title: "",
			course: "00",
			instruction: "",
			make_the_quiz_availability: 0,
			from_date: "",
			to_date: "",
			is_time_bound: 0,
			duration: 60,
			multiple_attempts: 0,
			number_of_attempts: "",
			grading_basis: "",
			quiz_question: [], 
		},
	}),
	actions: {
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
				console.error("Error creating quiz:", error.response ? error.response.data : error);
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
