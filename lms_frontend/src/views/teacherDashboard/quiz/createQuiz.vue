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
		<ReuseQuestion v-if="currentView === 'reuseQuestion'" @go-back="currentView = 'questions'" />
	</mainLayout>
</template>

<script setup>
import { ref } from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import QuizInformation from "@/components/teacher/quiz/QuizInformation.vue";
import QuizQuestion from "@/components/teacher/quiz/QuizQuestion.vue";
import QuizSettings from "@/components/teacher/quiz/QuizSettings.vue";
import AddQuestion from "@/components/teacher/quiz/AddQuestion.vue";
import ReuseQuestion from "@/components/teacher/quiz/ReuseQuestion.vue";
import mainLayout from "@/components/teacher/layout/MainLayout.vue";

const currentView = ref("information");
const quizStore = useQuizStore();

const handleQuizCreated = (quizData) => {
	quizStore.updateQuizData(quizData);
	currentView.value = "questions";
};

const handleSaveSettings = (settingsData) => {
	quizStore.updateQuizData(settingsData);
	quizStore.createQuiz();
	currentView.value = "information"; // أو الصفحة التي تريد الانتقال إليها بعد الحفظ
};

const handleAddQuestion = (questionData) => {
	quizStore.addQuestion(questionData);
	currentView.value = "questions";
};
</script>
