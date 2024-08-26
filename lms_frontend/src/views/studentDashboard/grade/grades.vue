<template>
	<main-layout>
		<LoadingSpinner v-if="gradeStore.loadingGrades" />
		<div v-else-if="gradeStore.errorGrades">{{ gradeStore.errorGrades }}</div>
		<GradeList v-else :grades="gradeStore.grades" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useGradeStore } from "@/stores/studentStore/gradeStore";
import { useStudentStore } from "@/stores/studentStore/courseStore";
import GradeList from "@/components/student/grade/Grades.vue";
import mainLayout from "@/components/MainSub.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const gradeStore = useGradeStore();

const studentStore = useStudentStore();
const courseCode = ref("");
const courseType = ref("");
onMounted(() => {
	if (studentStore.selectedCourse) {
		courseCode.value = studentStore.selectedCourse.course_code;
		courseType.value = studentStore.selectedCourse.course_type;
		gradeStore.fetchGrades(courseCode.value, courseType.value);
		console.log(courseCode.value);
	} else {
		console.error("No course selected. Please select a course.");
	}
});
</script>
<style scoped>
* {
	width: 94%;
	margin: 0px;
}
</style>
