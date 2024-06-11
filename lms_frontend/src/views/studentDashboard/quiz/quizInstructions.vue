<template>
	<main-layout>
		<QuizInstructions :instructions="quizInstructions" />
	</main-layout>
</template>

<script setup>
import { ref } from "vue";
import QuizInstructions from "@/components/quiz/QuizInstructions.vue";
import mainLayout from "@/components/MainLayout.vue";

// Define the quiz instructions data
const quizInstructions = ref([
	3, // Attempts allowed
	30, // Time limit in minutes
	20, // Number of questions
	100, // Total score in points
	"5:00 PM", // End time
	"Please ensure you read each question carefully and answer to the best of your ability. Good luck!",
	"Quiz 3",
	"Math001",
]);
</script>
