<template>
    <Navbar></Navbar>
	<!-- <main-layout> -->
		<!-- <LoadingSpinner v-if="loading" /> -->
		<!-- <div v-else-if="error">{{ error }}</div> -->
		<QuizResultList :quizzes="quizzes" />
	<!-- </main-layout> -->
</template>

<script setup>
import { ref, onMounted } from "vue";
import QuizResultList from "@/components/quiz/QuizResultList.vue";
import Navbar from "@/components/Navbar.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const quizzes = ref([
	{
		id: 1,
		title: "Quiz 1",
		review: "Review",
		grade: 85,
		total_grades: 100,
		time_taken: 2700, // in seconds
		date_started: "2024-06-23T14:00:00",
		date_ended: "2024-06-23T14:45:00",
	},
	{
		id: 2,
		title: "Quiz 2",
		review: "Review",
		grade: 70,
		total_grades: 100,
		time_taken: 1800, // in seconds
		date_started: "2024-06-22T11:30:00",
		date_ended: "2024-06-22T12:00:00",
	},
]);

const loading = ref(false);
const error = ref(null);
</script>
