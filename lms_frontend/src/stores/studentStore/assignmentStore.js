import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

export const useAssignmentStore = defineStore("assignment", {
  state: () => ({
    assignments: [],
    assignmentDetails: null,
    loading: false,
    error: null,
    previousSubmission: null,
    previousSubmissionFiles: [],
    isSubmitted: false,
  }),
  actions: {
    async fetchAssignments(courseName = "00") {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(
          "http://localhost:8080/api/method/academia.lms_api.student.assignment.get_assignments_by_course",
          {
            params: { course_name: courseName },
          }
        );
        this.assignments = response.data.data;
      } catch (error) {
        console.error("Error fetching assignments:", error);
        this.error =
          error.response?.data?.message ||
          error.message ||
          "An error occurred while fetching assignments.";
      } finally {
        this.loading = false;
      }
    },
    async fetchAssignmentDetails(assignmentName) {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(
          "http://localhost:8080/api/method/academia.lms_api.student.assignment.get_assignment",
          {
            params: { assignment_name: assignmentName },
            headers: {
              "Content-Type": "application/json",
              Authorization: Cookies.get("authToken"),
            },
          }
        );
        this.assignmentDetails = response.data.data;
        this.isSubmitted = response.data.is_submitted;
        console.log(this.isSubmitted);
      } catch (error) {
        console.error("Error fetching assignment details:", error);
        this.error =
          error.response?.data?.message ||
          error.message ||
          "An error occurred while fetching the assignment details.";
      } finally {
        this.loading = false;
      }
    },
    async fetchPreviousSubmission(assignmentName) {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(
          "http://localhost:8080/api/method/academia.lms_api.student.assignment.get_assignment_and_submission_details",
          {
            params: { assignment: assignmentName },
            headers: {
              "Content-Type": "application/json",
              Authorization: Cookies.get("authToken"),
            },
          }
        );
        this.previousSubmission = response.data.previous_submission;
        this.previousSubmissionFiles = response.data.files;
      } catch (error) {
        console.error("Error fetching previous submission:", error);
        this.error =
          error.response?.data?.message ||
          error.message ||
          "Error fetching previous submission.";
      } finally {
        this.loading = false;
      }
    },
    async deleteAttachment(fileUrl) {
      try {
        const response = await axios.post(
          "http://localhost:8080/api/method/academia.lms_api.student.assignment.delete_attachment",
          { file_url: fileUrl },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: Cookies.get("authToken"),
            },
          }
        );
        console.log("Attachment deleted:", response);

        if (response.data.message && response.data.message.status === "success") {
          this.previousSubmissionFiles = this.previousSubmissionFiles.filter(
            (file) => file.file_url !== fileUrl
          );
        } else {
          throw new Error(response.data.message.message || "Unknown error");
        }
      } catch (error) {
        if (error.response && error.response.data && error.response.data.message) {
          throw new Error(error.response.data.message);
        } else {
          throw new Error("Error deleting file.");
        }
      }
    },
    async submitAssignment(data) {
      try {
        const response = await axios.post(
          "http://localhost:8080/api/method/academia.lms_api.student.assignment.create_assignment_submission",
          data,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: Cookies.get("authToken"),
            },
          }
        );
        this.isSubmitted = response.data.is_submitted;
        console.log(response.data);
        return response; // إضافة هذه التعليمة
      } catch (error) {
        console.error("Error submitting assignment:", error);
        let errorMessage = "An error occurred while submitting the assignment.";
        if (error.response?.data?.exception.includes("UpdateAfterSubmitError")) {
          errorMessage =
            "Cannot update a submitted assignment. Please create a new submission.";
        }
        throw new Error(errorMessage);
      }
    },
  },
});
