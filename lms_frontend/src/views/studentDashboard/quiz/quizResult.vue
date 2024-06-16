<template>
	<main-layout>
		<div v-if="quizResultStore.loading">Loading quizzes...</div>
		<div v-else-if="quizResultStore.error">{{ quizResultStore.error }}</div>
		<QuizResult :quizResult="quizResult" />
	</main-layout>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useQuizStore } from "@/stores/quizStore";
import QuizResult from "@/components/quiz/QuizResult.vue";
import mainLayout from "@/components/MainLayout.vue";

const quizResultStore = useQuizStore();

const quizResult = ref(null);

onMounted(async () => {
	const quizAttemptId = "dee2e6f2c0"; 
	await quizResultStore.fetchQuizResult(quizAttemptId);
	quizResult.value = quizResultStore.quizResult;
});
</script>
