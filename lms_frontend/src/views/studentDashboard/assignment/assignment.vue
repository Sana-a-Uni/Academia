<template>
	<main-layout>
		<LoadingSpinner v-if="assignmentStore.loading" />
		<div v-else-if="assignmentStore.error">{{ assignmentStore.error }}</div>
		<Assignment
			v-else-if="assignmentDetails"
			:assignmentDetails="assignmentDetails"
			:onSubmit="submitAssignment"
		/>
		<div v-else>Loading...</div>
	</main-layout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useAssignmentStore } from "@/stores/studentStore/assignmentStore";
import Assignment from "@/components/student/assignment/Assignment.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const route = useRoute();
const assignmentStore = useAssignmentStore();
const assignmentName = ref(route.params.assignmentName || "ecff4b55c2");

const assignmentDetails = ref(null);

const submitAssignment = async (data) => {
	try {
		const response = await assignmentStore.submitAssignment(data);
		console.log(response.message);
	} catch (error) {
		console.error("Error submitting assignment", error);
	}
};

onMounted(async () => {
	try {
		await assignmentStore.fetchAssignmentDetails(assignmentName.value);
		assignmentDetails.value = assignmentStore.assignmentDetails;
	} catch (error) {
		console.error("Error fetching assignment details:", error);
	}
});
</script>
