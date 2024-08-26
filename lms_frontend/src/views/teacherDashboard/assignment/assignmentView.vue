<template>
	<main-layout>
		<LoadingSpinner v-if="assignmentStore.loading" />
		<div v-else-if="assignmentStore.error">{{ assignmentStore.error }}</div>
		<AssignmentList v-else :assignments="assignments" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import { useRoute } from "vue-router";
import AssignmentList from "@/components/teacherComponents/assignment/AssignmentView.vue";
import mainLayout from "@/components/teacherComponents/layout/MainSub.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const route = useRoute();

const assignmentStore = useAssignmentStore();
import { useCourseStore } from "@/stores/teacherStore/courseStore";
const courseStore = useCourseStore();
const selectedCourse = computed(() => courseStore.selectedCourse);

onMounted(() => {
	if (selectedCourse.value) {
		assignmentStore.fetchAssignments(
			selectedCourse.value.course,
			selectedCourse.value.course_type
		);
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
* {
	width: 94%;
	margin: 0px;
}
</style>
