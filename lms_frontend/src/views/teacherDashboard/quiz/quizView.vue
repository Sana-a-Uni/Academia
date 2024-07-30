<template>
	<main-layout>
		<LoadingSpinner v-if="quizStore.loading" />
		<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
		<QuizList v-else :quizzes="quizzes" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import { useRoute } from "vue-router";
import QuizList from "@/components/teacherComponents/quiz/QuizView.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const route = useRoute();

const quizStore = useQuizStore();
// const courseName = ref(route.params.courseName);
const courseName = ref("00");

onMounted(() => {
	quizStore.fetchQuizzes(courseName.value);
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
