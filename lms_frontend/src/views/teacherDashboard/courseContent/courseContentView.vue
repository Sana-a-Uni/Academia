<template>
	<main-layout>
		<LoadingSpinner v-if="courseContentStore.loading" />
		<div v-else-if="courseContentStore.error">{{ courseContentStore.error }}</div>
		<CourseContent v-else :courseContents="courseContents" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch,computed } from "vue";
import { useCourseContentStore } from "@/stores/teacherStore/courseContentStore";
import { useCourseStore } from "@/stores/teacherStore/courseStore";
import { useRoute } from "vue-router";
import mainLayout from "@/components/teacherComponents/layout/MainSub.vue";
import CourseContent from "@/components/teacherComponents/courseContent/CourseContentList.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const route = useRoute();
const courseContentStore = useCourseContentStore();
const courseStore = useCourseStore();
const selectedCourse = computed(() => courseStore.selectedCourse);

const courseCode = ref("");
const courseType = ref("");

onMounted(() => {
	if (selectedCourse.value) {
		courseContentStore.fetchCourseContents(
			selectedCourse.value.course,
			selectedCourse.value.course_type
		);
		console.log(courseCode.value);
	} else {
		console.error("No course selected. Please select a course.");
	}
});

const courseContents = ref([]);
courseContents.value = courseContentStore.courseContents;

watch(
	() => courseContentStore.courseContents,
	(newCourseContents) => {
		courseContents.value = newCourseContents;
	}
);
</script>

<style scoped>
* {
	width: 94%;
	margin: 0;
}
</style>
