import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useGradeStore = defineStore("gradeStore", {
	state: () => ({
		grades: [],
		loadingGrades: false,
		errorGrades: null,
		quizDetails: {
			title: "",
			grading_basis: "",
			to_date: "",
			total_grades: 0,
		},
		attempts: [],
		loadingQuiz: false,
		errorQuiz: null,
		assignmentDetails: {},
		assessmentCriteria: [],
		feedback: "",
		assignment_grade: 0,
		loadingAssignment: false,
		errorAssignment: null,
	}),
	actions: {
		async fetchGrades(courseName ,course_type) {
			this.loadingGrades = true;
			this.errorGrades = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.grade.get_quiz_and_assignment_grades",
					{
						params: { course: courseName ,course_type:course_type },
					}
				);
				console.log("API Response:", response.data.message); 
				this.grades = [
					...response.data.message.quizzes,
					...response.data.message.assignments,
				];
			} catch (err) {
				this.errorGrades = "Failed to fetch grades";
			} finally {
				this.loadingGrades = false;
			}
		},
		async fetchQuizAttempts(quizName) {
			this.loadingQuiz = true;
			this.errorQuiz = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.grade.get_quiz_attempts",
					{
						params: { quiz_name: quizName },
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				console.log(response.data.message.map((attempt) => attempt.attempts).flat());
				if (response.data.message.length > 0) {
					this.quizDetails = response.data.message[0].quizDetails;
					this.attempts = response.data.message
						.map((attempt) => attempt.attempts)
						.flat();
				} else {
					this.errorQuiz = "No attempts found";
				}
			} catch (error) {
				this.errorQuiz = error.message || "Failed to fetch quiz attempts";
			} finally {
				this.loadingQuiz = false;
			}
		},
		updateQuizDetails(partialData) {
			this.quizDetails = { ...this.quizDetails, ...partialData };
		},
		addAttempt(attempt) {
			this.attempts.push(attempt);
		},
		removeAttempt(index) {
			this.attempts.splice(index, 1);
		},
		async fetchAssignmentDetails(assignmentName) {
			this.loadingAssignment = true;
			this.errorAssignment = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.grade.get_assignment_assessment_details",
					{
						params: { assignment_name: assignmentName },
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				const data = response.data.message;
				this.assignmentDetails = data.assignment_info;
				this.assessmentCriteria = data.assessment_details;
				this.feedback = data.feedback;
				this.assignment_grade = data.assignment_grade;
			} catch (error) {
				this.errorAssignment = "Failed to fetch assignment details";
			} finally {
				this.loadingAssignment = false;
			}
		},
	},
});
