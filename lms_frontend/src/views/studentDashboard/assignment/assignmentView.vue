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
import { useStudentStore } from "@/stores/studentStore/courseStore";
import { useRoute } from "vue-router";
import AssignmentList from "@/components/student/assignment/AssignmentView.vue";
import mainLayout from "@/components/MainSub.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
const route = useRoute();

const assignmentStore = useAssignmentStore();

const studentStore = useStudentStore();
const courseCode = ref("");
const courseType = ref("");
onMounted(() => {
	if (studentStore.selectedCourse) {
		courseCode.value = studentStore.selectedCourse.course_code;
		courseType.value = studentStore.selectedCourse.course_type;
		assignmentStore.fetchAssignments(courseCode.value,courseType.value );
		console.log(courseCode.value);
	} else {
		console.error("No course selected. Please select a course.");
	}
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
<style scoped>
*{
	width: 94%;
	margin: 0px ;
}
</style>
