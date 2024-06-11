<template>
	<main-layout>
		<div v-if="quizStore.loading">Loading quizzes...</div>
		<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
		<QuizList v-else :quizzes="quizzes" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useQuizStore } from "@/stores/quizStore";
import QuizList from "@/components/quiz/QuizList.vue";
import mainLayout from "@/components/MainLayout.vue";

const quizStore = useQuizStore();
const courseName = ref("00");
const studentId = ref("EDU-STU-2024-00001");

onMounted(() => {
	quizStore.fetchQuizzes(courseName.value, studentId.value);
});

const quizzes = ref([]);
quizzes.value = quizStore.quizzes;

watch(
	() => quizStore.quizzes,
	(newQuizzes) => {
		quizzes.value = newQuizzes;
	}
);
</script>
