<template>
	<Navbar></Navbar>
	<LoadingSpinner v-if="quizStore.loading" />
	<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
	<QuizResultList :quizzesResult="quizStore.quizzesResult" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import QuizResultList from "@/components/quiz/QuizResultList.vue";
import Navbar from "@/components/Navbar.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import { useQuizStore } from "@/stores/quizStore";

const quizStore = useQuizStore();
const courseName = ref("00");
const studentId = ref("EDU-STU-2024-00001");

onMounted(() => {
	quizStore.fetchQuizzesResult(courseName.value, studentId.value);
});
</script>
