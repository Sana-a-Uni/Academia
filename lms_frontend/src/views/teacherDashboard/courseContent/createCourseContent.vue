<template>
	<main-layout>
		<create-course-content @quiz-created="handleQuizCreated" />
	</main-layout>
</template>

<script setup>
import { computed } from "vue";
import { useCourseContentStore } from "@/stores/teacherStore/courseContentStore";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";
import createCourseContent from "@/components/teacherComponents/courseContent/CreateCourseContent.vue";
import { useCourseStore } from "@/stores/teacherStore/courseStore";
const courseStore = useCourseStore();
const selectedCourse = computed(() => courseStore.selectedCourse);

const store = useCourseContentStore();

const handleQuizCreated = () => {
	store.fetchCourseContents(selectedCourse.value.course, selectedCourse.value.course_type);
};
</script>

<style scoped>
* {
	width: 94%;
	margin: 0;
}
</style>
