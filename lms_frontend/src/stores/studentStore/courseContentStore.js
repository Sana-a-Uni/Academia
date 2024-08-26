import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useCourseContentStore = defineStore("courseContent", {
	state: () => ({
		courseContents: [],
		courseContentDetails: {},
		loading: false,
		error: null,
	}),
	actions: {
		async fetchCourseContents(courseName, courseType) {
			this.loading = true;
			this.error = null;
			try {
				const response = await axios.get(
					"http://localhost:8080/api/method/academia.lms_api.student.courseContent.get_course_content_summary",
					{
						params: { course_name: courseName, course_type: courseType },
						headers: {
							"Content-Type": "application/json",
							Authorization: Cookies.get("authToken"),
						},
					}
				);
				console.log(response.data.data);

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
        async fetchCourseContentDetails(contentName) {
            this.loading = true;
            this.error = null;
            try {
              const response = await axios.get(
                "http://localhost:8080/api/method/academia.lms_api.student.courseContent.get_course_content_details",
                {
                  params: { content_name: contentName },
                  headers: {
                    "Content-Type": "application/json",
                    Authorization: Cookies.get("authToken"),
                  },
                }
              );
            //   console.log(response.data.data);
              
              this.courseContentDetails = response.data.data;
            } catch (error) {
              console.error("Error fetching course content details:", error);
              this.error = error.response?.data?.message || error.message || "An error occurred while fetching course content details.";
            } finally {
              this.loading = false;
            }
          },
        },
});
