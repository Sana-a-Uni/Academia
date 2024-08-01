<template>
	<main-layout>
		<div class="container">
			<div class="header">View Attempts</div>
			<QuizDetails :quizDetails="quizDetails" :attempts="attempts" />
		</div>
	</main-layout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import QuizDetails from "@/components/student/grade/QuizDetails.vue";
import MainLayout from "@/components/MainLayout.vue";
import { useGradeStore } from "@/stores/studentStore/gradeStore";

const gradeStore = useGradeStore();
const route = useRoute();
const quizName = ref(route.params.quiz_name);

onMounted(async () => {
	await gradeStore.fetchQuizAttempts(quizName.value);
	console.log("Fetched Quiz Details:", gradeStore.quizDetails);
	console.log("Fetched Attempts:", gradeStore.attempts);
});

const quizDetails = computed(() => gradeStore.quizDetails);
const attempts = computed(() => gradeStore.attempts);
</script>

<style scoped>
body {
	font-family: Arial, sans-serif;
	background-color: #f4f4f4;
	margin-top: 90px;
	margin-right: auto;
	padding: 0;
}
.container {
	background-color: white;
	width: 100%;
	height: 97vh;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	overflow: hidden;
}
.header {
	background-color: #f8f8f8;
	padding: 20px;
	text-align: center;
	font-size: 24px;
	font-weight: bold;
	border-bottom: 1px solid #ddd;
}
</style>
