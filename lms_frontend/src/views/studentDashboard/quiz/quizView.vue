<template>
	<main-layout>
		<LoadingSpinner v-if="quizStore.loading" />
		<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
		<QuizList v-else :quizzes="quizzes" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useQuizStore } from "@/stores/quizStore";
import { useStudentStore } from "@/stores/studentStore/courseStore";
import QuizList from "@/components/quiz/QuizList.vue";
import MainLayout from "@/components/MainSub.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";


const quizStore = useQuizStore();
const studentStore = useStudentStore(); 

const courseCode = ref("");
const course_type=ref("");
onMounted(() => {
	if (studentStore.selectedCourse) {
		courseCode.value = studentStore.selectedCourse.course_code;
		course_type.value = studentStore.selectedCourse.course_type;
		quizStore.fetchQuizzes(courseCode.value , course_type.value);
		console.log(courseCode.value);
		
	} else {
		console.error("No course selected. Please select a course.");
	}
});

const quizzes = ref([]);
watch(
	() => quizStore.quizzes,
	(newQuizzes) => {
		quizzes.value = newQuizzes;
	}
);
</script>
<style scoped>
*{
	width: 93%;
	margin: 0px ;
}
</style>
