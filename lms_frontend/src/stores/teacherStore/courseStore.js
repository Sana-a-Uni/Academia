import { defineStore } from "pinia";
import axios from "axios";
import { useQuizStore } from "@/stores/teacherStore/quizStore";

export const useCourseStore = defineStore("courseStore", {
	state: () => ({
		courses: [],
		selectedCourse: null,
		notifications: [
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
			{
				date: "22 Jan",
				title: "Algorithm",
				description: "3 hour .Dr\\Ghallib",
			},
		],
	}),
	actions: {
		async fetchCourses() {
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.course.get_faculty_details_for_current_term_and_year"
				);
				// console.log(response.data.message);
				if (response.data.error) {
					console.error(response.data.error);
				} else {
					this.courses = response.data.message;
				}
			} catch (error) {
				console.error("There was an error fetching the faculty details: ", error);
			}
		},
		selectCourse(course) {
			this.selectedCourse = course;
			localStorage.setItem("selectedCourse", JSON.stringify(course));
		},
		loadSelectedCourse() {
			const savedCourse = localStorage.getItem("selectedCourse");
			if (savedCourse) {
				this.selectedCourse = JSON.parse(savedCourse);
			}
		},
	},
});
