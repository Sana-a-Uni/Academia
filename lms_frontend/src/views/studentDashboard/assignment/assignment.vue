<template>
	<main-layout>
		<LoadingSpinner v-if="assignmentStore.loading" />
		<div v-else-if="assignmentStore.error">{{ assignmentStore.error }}</div>
		<Assignment
			v-else
			:assignmentDetails="assignmentDetails"
			:previousSubmission="previousSubmission"
			:previousSubmissionFiles="previousSubmissionFiles"
			@submit="submitAssignment"
		/>
	</main-layout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAssignmentStore } from "@/stores/studentStore/assignmentStore";
import Assignment from "@/components/student/assignment/Assignment.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const route = useRoute();
const router = useRouter();
const assignmentStore = useAssignmentStore();
const assignmentName = ref(route.params.assignmentName);

const assignmentDetails = computed(() => assignmentStore.assignmentDetails);
const previousSubmission = computed(() => assignmentStore.previousSubmission);
const previousSubmissionFiles = computed(() => assignmentStore.previousSubmissionFiles);

const submitAssignment = async (data) => {
	try {
		const response = await assignmentStore.submitAssignment(data);
		console.log("Server response:", response); // عرض استجابة السيرفر في وحدة التحكم

		// التحقق من حقل status_code
		if (response && response.data.status_code === 200) {
			alert(response.data.message || "Assignment submitted successfully!");
			router.push({ path: "/studentDashboard/assignmentView" });
		} else {
			console.error("Unexpected response format", response);
			alert("Unexpected response format");
		}
	} catch (error) {
		console.error("Error submitting assignment", error);
		alert(error.message);
	}
};

onMounted(async () => {
	try {
		await assignmentStore.fetchAssignmentDetails(route.params.assignmentName);
		await assignmentStore.fetchPreviousSubmission(route.params.assignmentName);
		console.log("Assignment Details:", assignmentStore.assignmentDetails);
		console.log("Previous Submission:", assignmentStore.previousSubmission);
	} catch (error) {
		console.error("Error fetching assignment details or previous submission:", error);
	}
});
</script>
