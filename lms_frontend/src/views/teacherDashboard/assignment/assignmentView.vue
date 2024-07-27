<template>
	<main-layout>
		<LoadingSpinner v-if="assignmentStore.loading" />
		<div v-else-if="assignmentStore.error">{{ assignmentStore.error }}</div>
		<AssignmentList v-else :assignments="assignments" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import { useRoute } from "vue-router";
import AssignmentList from "@/components/teacher/assignment/AssignmentView.vue";
import mainLayout from "@/components/teacher/layout/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const route = useRoute();

const assignmentStore = useAssignmentStore();
// const courseName = ref(route.params.courseName);
// const facultyMember = ref(route.params.facultyMember);
const courseName = ref("00");
const facultyMember = ref("ACAD-FM-00001");

onMounted(() => {
	assignmentStore.fetchAssignments(courseName.value, facultyMember.value);
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
