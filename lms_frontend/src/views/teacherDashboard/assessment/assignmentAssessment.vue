<template>
	<Navbar></Navbar>
	<LoadingSpinner v-if="loading" />
	<div v-else-if="error">{{ error }}</div>
	<AssignmentAssessment v-else :details="assignmentDetails" />
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute } from "vue-router";
import { useAssessmentStore } from "@/stores/teacherStore/assessmentStore";
import Navbar from "@/components/teacherComponents/layout/Navbar.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import AssignmentAssessment from "@/components/teacherComponents/assessment/AssignmentAssessment";

const route = useRoute();
const store = useAssessmentStore();
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
	await store.fetchAssignments();
	await store.fetchAssignmentDetails(route.params.id);
	loading.value = store.loading;
	error.value = store.error;
});

watch(
	() => route.params.id,
	async (newId) => {
		await store.fetchAssignmentDetails(newId);
	}
);

const assignmentDetails = computed(() => store.assignmentDetails);
</script>
