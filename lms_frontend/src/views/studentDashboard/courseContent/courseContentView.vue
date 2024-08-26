<template>
	<main-layout>
	  <LoadingSpinner v-if="courseContentStore.loading" />
	  <div v-else-if="courseContentStore.error">{{ courseContentStore.error }}</div>
	  <CourseContent v-else :courseContents="courseContents" />
	</main-layout>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from "vue";
  import { useCourseContentStore } from "@/stores/studentStore/courseContentStore";
  import { useStudentStore } from "@/stores/studentStore/courseStore";
  import { useRoute } from "vue-router";
  import MainLayout from "@/components/MainSub.vue";
  import CourseContent from "@/components/student/courseContent/CourseContentList.vue";
  import LoadingSpinner from "@/components/LoadingSpinner.vue";
  
  const route = useRoute();
  const courseContentStore = useCourseContentStore();
  const studentStore = useStudentStore();
  
  const courseCode = ref("");
  const courseType = ref("");
  
  onMounted(() => {
	if (studentStore.selectedCourse) {
	  courseCode.value = studentStore.selectedCourse.course_code;
	  courseType.value = studentStore.selectedCourse.course_type;
	  courseContentStore.fetchCourseContents(courseCode.value, courseType.value);
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
  