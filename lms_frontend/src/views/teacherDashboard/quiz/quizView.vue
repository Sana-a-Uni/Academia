<template>
	<main-layout>
		<LoadingSpinner v-if="quizStore.loading" />
		<div v-else-if="quizStore.error">{{ quizStore.error }}</div>
		<QuizList v-else :quizzes="quizzes" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted, watch , computed} from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import QuizList from "@/components/teacherComponents/quiz/QuizView.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

import { useCourseStore } from "@/stores/teacherStore/courseStore";
const courseStore = useCourseStore();
const selectedCourse = computed(() => courseStore.selectedCourse);

const quizStore = useQuizStore();
console.log(selectedCourse.value);
onMounted(() => {
	if (selectedCourse.value) {
		quizStore.fetchQuizzes(selectedCourse.value.course);
	}
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
