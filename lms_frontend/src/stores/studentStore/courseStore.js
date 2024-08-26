import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useStudentStore = defineStore("student", {
	state: () => ({
		studentDetails: {},
		courses: [],
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
		selectedCourse: null,
		error: null,
	}),
	actions: {
		async fetchStudentProgramDetails() {
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.course.get_student_program_details",
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);

				const data = response.data.message;
				if (data.error) {
					this.error = data.error;
				} else {
					this.studentDetails = data;
					this.courses = data.courses;
					console.log(data);
				}
			} catch (error) {
				this.error = "An error occurred while fetching student program details.";
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
