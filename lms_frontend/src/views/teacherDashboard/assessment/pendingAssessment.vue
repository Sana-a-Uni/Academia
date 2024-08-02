<template>
	<main-layout>
		<PendingAssessment :assignments="assignments" />
	</main-layout>
</template>


<script setup>
import { ref, onMounted, computed } from "vue";
import { useAssessmentStore } from "@/stores/teacherStore/assessmentStore";
import { useCourseStore } from "@/stores/teacherStore/courseStore";
import PendingAssessment from "@/components/teacherComponents/assessment/PendingAssessment.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";

const assessmentStore = useAssessmentStore();
const courseStore = useCourseStore();
const assignments = ref([]);

const selectedCourse = computed(() => courseStore.selectedCourse);

onMounted(async () => {
	if (selectedCourse.value) {
		await assessmentStore.fetchAssignments(selectedCourse.value.course);
		assignments.value = assessmentStore.assignments;
		console.log(selectedCourse.value.course);
	} else {
		console.error("No course selected");
	}
});
</script>
