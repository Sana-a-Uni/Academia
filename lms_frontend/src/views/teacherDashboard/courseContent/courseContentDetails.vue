<template>
	<main-layout>
		<LoadingSpinner v-if="loading" />
		<div v-else-if="error">{{ error }}</div>
		<CourseContentDetail v-else :courseContent="courseContent" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useCourseContentStore } from "@/stores/teacherStore/courseContentStore";
import CourseContentDetail from "@/components/teacherComponents/courseContent/CourseContentDetails.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";

const route = useRoute();
const courseName = route.params.courseName;

const courseContentStore = useCourseContentStore();

const loading = computed(() => courseContentStore.loading);
const error = computed(() => courseContentStore.error);
const courseContent = computed(() => courseContentStore.courseContentDetails);

onMounted(async () => {
	try {
		await courseContentStore.fetchCourseContentDetails(route.params.courseName);
		console.log(courseContent.value);
	} catch (err) {
		console.error("Error during component mount:", err);
	}
});
</script>

<style scoped>
*{
	width: 94%;
	margin: 0px ;
}
</style>

