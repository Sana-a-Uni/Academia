<template>
	<mainLayout>
		<QuizInformation v-if="currentView === 'information'" @quiz-created="handleQuizCreated" />
		<QuizQuestion
			v-if="currentView === 'questions'"
			:questions="quizStore.quizData.quiz_question"
			@go-back="currentView = 'information'"
			@settings="currentView = 'settings'"
			@addQuestion="currentView = 'addQuestion'"
			@reuseQuestion="currentView = 'reuseQuestion'"
		/>
		<QuizSettings
			v-if="currentView === 'settings'"
			@go-back="currentView = 'questions'"
			@save-settings="handleSaveSettings"
		/>
		<AddQuestion v-if="currentView === 'addQuestion'" @questions="handleAddQuestion" />
		<ReuseQuestion
			v-if="currentView === 'reuseQuestion'"
			@questions="handleReuseQuestion"
			@cancel="currentView = 'questions'"
		/>
	</mainLayout>
</template>

<script setup>
import { ref } from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import { useRouter } from "vue-router";
import QuizInformation from "@/components/teacher/quiz/QuizInformation.vue";
import QuizQuestion from "@/components/teacher/quiz/QuizQuestion.vue";
import QuizSettings from "@/components/teacher/quiz/QuizSettings.vue";
import AddQuestion from "@/components/teacher/quiz/AddQuestion.vue";
import ReuseQuestion from "@/components/teacher/quiz/ReuseQuestion.vue";
import mainLayout from "@/components/teacher/layout/MainLayout.vue";

const currentView = ref("information");
const quizStore = useQuizStore();
const router = useRouter();

const handleQuizCreated = () => {
	currentView.value = "questions";
};

const handleSaveSettings = (settingsData) => {
	quizStore.updateQuizData(settingsData);
	quizStore.createQuiz().then(() => {
		resetFields(); // Call reset fields after creating quiz
		router.push({ name: "quizList" }); // Redirect to quizList after reusing questions
	});
};

const handleAddQuestion = (questionData) => {
	quizStore.addQuestion(questionData);
	currentView.value = "questions";
};

const handleReuseQuestion = (selectedQuestions) => {
	selectedQuestions.forEach((question) => {
		quizStore.addQuestion({
			name: question.name,
			question: question.question,
			question_options: question.question_options,
			question_grade: question.question_grade,
		});
	});
	currentView.value = "questions";
};

const resetFields = () => {
	quizStore.quizData.title = "";
	quizStore.quizData.instruction = "";
	quizStore.quizData.make_the_quiz_availability = false;
	quizStore.quizData.from_date = "";
	quizStore.quizData.to_date = "";
	quizStore.quizData.is_time_bound = false;
	quizStore.quizData.duration = 0;
	quizStore.quizData.multiple_attempts = false;
	quizStore.quizData.number_of_attempts = "";
	quizStore.quizData.grading_basis = "";
	quizStore.quizData.quiz_question = [];
	quizStore.quizData.show_question_score = false;
	quizStore.quizData.show_correct_answer = false;
	quizStore.quizData.randomize_question_order = false;
};
</script>
