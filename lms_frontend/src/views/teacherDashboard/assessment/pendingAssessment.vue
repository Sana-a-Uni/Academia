<template>
	<main-layout>
		<PendingAssessment :assignments="assignments" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAssessmentStore } from "@/stores/teacherStore/assessmentStore";
import PendingAssessment from "@/components/teacherComponents/assessment/PendingAssessment.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";

const assessmentStore = useAssessmentStore();
const assignments = ref([]);

onMounted(async () => {
	const facultyMemberId = "ACAD-FM-00001";

	await assessmentStore.fetchAssignments(facultyMemberId);
	assignments.value = assessmentStore.assignments;
});
</script>
