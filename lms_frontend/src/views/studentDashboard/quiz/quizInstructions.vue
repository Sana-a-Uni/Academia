<template>
	<main-layout>
		<LoadingSpinner v-if="quizStore.loading" />
		<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
		<QuizInstructions v-else :quizInstructions="quizInstructions" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { useQuizStore } from "@/stores/quizStore";
import QuizInstructions from "@/components/quiz/QuizInstructions.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const quizStore = useQuizStore();
const route = useRoute();
const quizName = ref(route.params.quizName);
const studentId = ref("EDU-STU-2024-00002");

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
