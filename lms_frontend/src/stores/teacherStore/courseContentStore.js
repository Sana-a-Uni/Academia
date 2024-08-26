import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useCourseContentStore = defineStore("courseContent", {
	state: () => ({
		courseContents: [],
		courseContentDetails: {},
		uploadedFiles: [], // To store files uploaded by the user
		loading: false,
		error: null,
	}),
	actions: {
		// Fetch summary of course contents
		async fetchCourseContents(courseName, courseType) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.courseContent.get_course_content_summary",
					{
						params: { course_name: courseName, course_type: courseType },
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				this.courseContents = response.data.data;
			} catch (error) {
				console.error("Error fetching course contents:", error);
				this.error =
					error.response?.data?.message ||
					error.message ||
					"An error occurred while fetching course contents.";
			} finally {
				this.loading = false;
			}
		},

		// Fetch details of a specific course content
		async fetchCourseContentDetails(contentName) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.teacher.courseContent.get_course_content_details",
					{
						params: { content_name: contentName },
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				this.courseContentDetails = response.data.data;
			} catch (error) {
				console.error("Error fetching course content details:", error);
				this.error =
					error.response?.data?.message ||
					error.message ||
					"An error occurred while fetching course content details.";
			} finally {
				this.loading = false;
			}
		},

		// Handle file upload and convert files to Base64
		handleFileUpload(event) {
			const files = event.target.files;
			for (let i = 0; i < files.length; i++) {
				const file = files[i];
				const reader = new FileReader();
				reader.onload = (e) => {
					this.uploadedFiles.push({
						name: file.name,
						content: e.target.result.split(",")[1], // Extract Base64 content
					});
				};
				reader.readAsDataURL(file);
			}
		},

		// Remove an uploaded file
		removeFile(index) {
			this.uploadedFiles.splice(index, 1);
		},

		// Reset the form after submission
		resetForm() {
			this.uploadedFiles = [];
			this.courseContentDetails = {};
			this.error = null;
		},

		// Add course content with attached files, receiving data as an object
		async addCourseContent(contentData) {
			this.loading = true;
			this.error = null;
			try {
				// Attach uploaded files to the contentData object

				const response = await axios.post(
					"http://localhost:8080/api/method/academia.lms_api.teacher.courseContent.add_course_content",
					contentData,
					{
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				console.log(contentData);
				
				this.resetForm();
				
				return response.data;
			
			} catch (error) {
				console.error("Error adding course content:", error);
				this.error =
					error.response?.data?.message ||
					error.message ||
					"An error occurred while adding course content.";
			} finally {
				this.loading = false;
			}
		},
	},
});
