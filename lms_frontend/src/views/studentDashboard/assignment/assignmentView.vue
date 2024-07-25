<template>
	<main-layout>
		<LoadingSpinner v-if="assignmentStore.loading" />
		<div v-else-if="assignmentStore.error">{{ assignmentStore.error }}</div>
		<AssignmentList v-else :assignments="assignments" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useAssignmentStore } from "@/stores/studentStore/assignmentStore";
import { useRoute } from "vue-router";
import AssignmentList from "@/components/student/assignment/AssignmentView.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
const route = useRoute();

const assignmentStore = useAssignmentStore();
// const courseName = ref(route.params.courseName);
// const studentId = ref(route.params.studentId);
const courseName = ref("00");
const studentId = ref("EDU-STU-2024-00001");

onMounted(() => {
	assignmentStore.fetchAssignments(courseName.value, studentId.value);
});

const assignments = ref([]);
assignments.value = assignmentStore.assignments;

watch(
	() => assignmentStore.assignments,
	(newAssignments) => {
		assignments.value = newAssignments;
	}
);
</script>
