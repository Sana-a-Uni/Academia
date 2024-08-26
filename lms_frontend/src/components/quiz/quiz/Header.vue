<template>
	<div class="header">
		<div class="left-section">{{ student_name }}</div>
		<div class="right-section">{{ courseName }}</div>
	</div>
</template>
<script setup>
import { useStudentStore } from "@/stores/studentStore/courseStore";
import { onMounted , computed } from "vue";

const courseStore = useStudentStore();

onMounted(() => {
	courseStore.loadSelectedCourse();
	courseStore.fetchStudentProgramDetails(); 
});

const student_name = computed(
	() => courseStore.studentDetails.student_name
	|| "Default Student name"
);
const courseName = computed(
	() => courseStore.selectedCourse?.course_name || "Default Course Name"
);

</script>

<style scoped>
.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	background-color: white;
	color: black;
	padding: 5px;
}
.left-section {
	font-size: 16px;
	font-weight: bold;
}
.right-section {
	font-size: 16px;
}
@media (max-width: 768px) {
	.header {
		flex-direction: column;
		align-items: center;
		text-align: center;
	}
	.header .left-section,
	.header .right-section {
		margin-bottom: 5px;
	}
}
</style>
