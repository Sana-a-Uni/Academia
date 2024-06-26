<template>
	<main-layout>
		<LoadingSpinner v-if="quizResultStore.loading" />
		<div v-else-if="quizResultStore.error">{{ quizResultStore.error }}</div>
		<QuizResult v-else-if="quizResult" :quizResult="quizResult" />
		<div v-else>No quiz result available.</div>
	</main-layout>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useQuizStore } from "@/stores/quizStore";
import QuizResult from "@/components/quiz/QuizResult.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const quizResultStore = useQuizStore();
const route = useRoute();

const quizResult = ref(null);

onMounted(async () => {
	const quizAttemptId = route.params.quizAttemptId;
	await quizResultStore.fetchQuizResult(quizAttemptId);
	quizResult.value = quizResultStore.quizResult;
});

watch(
	() => quizResultStore.quizResult,
	(newQuizResult) => {
		quizResult.value = newQuizResult;
	}
);
</script>
