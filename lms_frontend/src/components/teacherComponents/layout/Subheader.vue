<template>
	<p>{{ currentYear }} - {{ semester }} Semester - {{ courseName }}</p>
</template>

<script setup>
import { computed, ref } from "vue";
import { useCourseStore } from "@/stores/teacherStore/courseStore";

// const courseName = ref("Data Structure"); 

const courseStore = useCourseStore();
const semester = computed(
	() => courseStore.selectedCourse?.academic_term 
);
const currentYear = computed(
	() => courseStore.selectedCourse?.academic_year 
);
const courseName = computed(
	() => courseStore.selectedCourse?.course_name 
);
</script>

<style scoped>
p {
	flex: 1;
	display: flex;
	justify-content: flex-start;
	margin-top: 55px;
	background-color: white;
	padding: 15px;
	/* padding-left: 20px; */
	border-bottom: 1px solid black;
	border-color: grey;
	font-size: 20px;
}

@media (max-width: 768px) {
	p {
		margin: 0px;
		margin-top: 40px;
	}
}

@media (min-width: 768px) {
	p {
		margin: 0px;
		margin-top: 52px;
		margin-left: 270px;
		margin-right: 10px;
	}
}
</style>
