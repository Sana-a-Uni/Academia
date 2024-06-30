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
import { useRoute } from "vue-router";
import QuizList from "@/components/quiz/QuizList.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
const route = useRoute();

const quizStore = useQuizStore();
const courseName = ref(route.params.courseName);
const studentId = ref(route.params.studentId);

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
