<template>
	<Navbar></Navbar>
	<LoadingSpinner v-if="loading" />
	<div v-else-if="error">{{ error }}</div>
	<div v-else>
		<AssignmentAssessment :details="assignmentDetails" :errors="fieldErrors" />
		<div v-if="fieldErrors.general" class="error-message">{{ fieldErrors.general }}</div>
		<ul v-if="Object.keys(fieldErrors).length > 0">
			<li v-for="(message, field) in fieldErrors" :key="field" class="error-message">
				{{ field }}: {{ message }}
			</li>
		</ul>
	</div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import { useAssessmentStore } from "@/stores/teacherStore/assessmentStore";
import Navbar from "@/components/teacherComponents/layout/Navbar.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import AssignmentAssessment from "@/components/teacherComponents/assessment/AssignmentAssessment.vue";

const route = useRoute();
const store = useAssessmentStore();
const loading = ref(true);
const error = ref(null);
const fieldErrors = ref({});

onMounted(async () => {
	try {
		await store.fetchAssignments();
		await store.fetchAssignmentDetails(route.params.submission_name);
	} catch (e) {
		console.error("Error fetching data:", e);
		alert("An error occurred while fetching data.");
		error.value = e.message;
	} finally {
		loading.value = store.loading;
		error.value = store.error;
	}
});

watch(
	() => route.params.submission_name,
	async (newId) => {
		try {
			await store.fetchAssignmentDetails(newId);
		} catch (e) {
			console.error("Error fetching assignment details:", e);
			alert("An error occurred while fetching assignment details.");
			error.value = e.message;
		}
	}
);

const assignmentDetails = computed(() => store.assignmentDetails);
</script>
