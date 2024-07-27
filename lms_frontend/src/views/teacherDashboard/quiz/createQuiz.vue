<template>
	<mainLayout>
		<QuizInformation
			v-if="currentView === 'information'"
			@quiz-created="handleQuizCreated"
			:errors="errors"
		/>
		<QuizQuestion
			v-if="currentView === 'questions'"
			:questions="quizStore.quizData.quiz_question"
			:errors="errors"
			@go-back="currentView = 'information'"
			@settings="currentView = 'settings'"
			@addQuestion="currentView = 'addQuestion'"
			@reuseQuestion="currentView = 'reuseQuestion'"
			@deleteQuestion="handleDeleteQuestion"
		/>
		<QuizSettings
			v-if="currentView === 'settings'"
			:errors="errors"
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
import { ref, watch } from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import { useRouter } from "vue-router";
import QuizInformation from "@/components/teacherComponents/quiz/QuizInformation.vue";
import QuizQuestion from "@/components/teacherComponents/quiz/QuizQuestion.vue";
import QuizSettings from "@/components/teacherComponents/quiz/QuizSettings.vue";
import AddQuestion from "@/components/teacherComponents/quiz/AddQuestion.vue";
import ReuseQuestion from "@/components/teacherComponents/quiz/ReuseQuestion.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";

const currentView = ref("information");
const quizStore = useQuizStore();
const router = useRouter();
const errors = ref({});

watch(errors, (newErrors) => {
	console.log("Errors updated:", newErrors);
});

const handleQuizCreated = () => {
	currentView.value = "questions";
};

const handleSaveSettings = async (settingsData) => {
	quizStore.updateQuizData(settingsData);
	try {
		const success = await quizStore.createQuiz();
		if (success) {
			resetFields();
			router.push({ name: "quizList" });
		} else {
			if (quizStore.errors) {
				errors.value = quizStore.errors;
				console.log(errors.value);

				if (errors.value.title || errors.value.instruction) {
					currentView.value = "information";
				} else if (errors.value.questions) {
					currentView.value = "questions";
				}
			}
		}
	} catch (err) {
		if (err.response && err.response.data && err.response.data.errors) {
			errors.value = err.response.data.errors;
			console.log(errors.value);
			if (errors.value.title || errors.value.instruction) {
				currentView.value = "information";
			} else if (errors.value.questions) {
				currentView.value = "questions";
			}
		} else {
			alert("An unexpected error occurred.");
		}
	}
};

const handleAddQuestion = (questionData) => {
	quizStore.addQuestion(questionData);
	currentView.value = "questions";
	errors.value = {};
};

const handleReuseQuestion = (selectedQuestions) => {
	if (!selectedQuestions) {
		selectedQuestions = [];
	}
	selectedQuestions.forEach((question) => {
		quizStore.addQuestion({
			name: question.name,
			question: question.question,
			question_options: question.question_options,
			question_grade: question.question_grade,
		});
	});
	currentView.value = "questions";
	errors.value = {};
};

const handleDeleteQuestion = (index) => {
	quizStore.quizData.quiz_question.splice(index, 1);
	if (quizStore.quizData.quiz_question.length === 0) {
		errors.value = { questions: [{ question: "At least one question is required." }] };
	} else {
		errors.value = {};
	}
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
	errors.value = {};
};
</script>
