<template>
	<Navbar></Navbar>
	<LoadingSpinner v-if="quizStore.loading" />
	<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
	<QuizResultList :quizzesResult="quizStore.quizzesResult" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import QuizResultList from "@/components/quiz/QuizResultList.vue";
import { useStudentStore } from "@/stores/studentStore/courseStore";
import Navbar from "@/components/Navbar.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import { useQuizStore } from "@/stores/quizStore";

const quizStore = useQuizStore();
const studentStore = useStudentStore(); 

const courseCode = ref("");
const course_type=ref("");
onMounted(() => {
	if (studentStore.selectedCourse) {
		courseCode.value = studentStore.selectedCourse.course_code;
		course_type.value = studentStore.selectedCourse.course_type;
		quizStore.fetchQuizzesResult(courseCode.value , course_type.value);
		console.log(courseCode.value);
		
	} else {
		console.error("No course selected. Please select a course.");
	}
});
</script>
