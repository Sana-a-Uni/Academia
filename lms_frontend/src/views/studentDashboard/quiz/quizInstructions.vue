<template>
	<main-layout>
		<LoadingSpinner v-if="quizStore.loading" />
		<div v-else-if="quizStore.error">
			<p>{{ quizStore.error }}</p>
			<button @click="goBack" class="btn btn-cancel">Back</button>
		</div>
		<QuizInstructions v-else :quizInstructions="quizInstructions" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuizStore } from "@/stores/quizStore";
import QuizInstructions from "@/components/quiz/QuizInstructions.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const quizStore = useQuizStore();
const route = useRoute();
const router = useRouter();
const quizName = ref(route.params.quizName);

onMounted(() => {
	quizStore.fetchQuizInstructions(quizName.value).then(() => {
		if (quizStore.error && quizStore.error.includes("403")) {
			alert(quizStore.error);
			router.push({ name: "quizView" });
		}
	});
});

const quizInstructions = ref({});
watch(
	() => quizStore.quizInstructions,
	(newQuizInstructions) => {
		quizInstructions.value = newQuizInstructions;
	}
);

</script>
