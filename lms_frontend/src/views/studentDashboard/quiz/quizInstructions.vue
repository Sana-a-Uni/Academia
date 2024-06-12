<template>
	<main-layout>
		<div v-if="quizStore.loading">Loading quiz instructions...</div>
		<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
		<QuizInstructions v-else :quizInstructions="quizInstructions" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useQuizStore } from "@/stores/quizStore";
import QuizInstructions from "@/components/quiz/QuizInstructions.vue";
import mainLayout from "@/components/MainLayout.vue";

const quizStore = useQuizStore();
const quizName = ref("2874210861");
const studentId = ref("EDU-STU-2024-00001");

onMounted(() => {
	quizStore.fetchQuizInstructions(quizName.value, studentId.value);
});

const quizInstructions = ref({});
quizInstructions.value = quizStore.quizInstructions;

watch(
	() => quizStore.quizInstructions,
	(newQuizInstructions) => {
		quizInstructions.value = newQuizInstructions;
	}
);
</script>
