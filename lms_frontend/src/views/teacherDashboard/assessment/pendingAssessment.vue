<template>
	<main-layout>
		<PendingAssessment :assignments="assignments" />
	</main-layout>
</template>

<script setup>
import { ref } from "vue";
import PendingAssessment from "@/components/teacher/assessment/PendingAssessment.vue";
import mainLayout from "@/components/MainLayout.vue";

const assignments = ref([
	{
		id: 1,
		studentName: "John Doe",
		assignmentTitle: "Math Homework",
		submissionDate: "2024-07-24T10:30:00",
	},
	{
		id: 2,
		studentName: "Jane Smith",
		assignmentTitle: "Science Project",
		submissionDate: "2024-07-23T14:00:00",
	},
	{
		id: 3,
		studentName: "Emily Johnson",
		assignmentTitle: "History Essay",
		submissionDate: "2024-07-22T16:45:00",
	},
]);
</script>
