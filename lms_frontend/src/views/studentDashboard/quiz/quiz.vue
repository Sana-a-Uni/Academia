<template>
	<div class="container">
		<Header />
		<SubHeader
			:formattedTime="formattedTime"
			:currentQuestion="currentQuestion"
			:prevQuestion="prevQuestion"
			:nextQuestion="nextQuestion"
			:submitAnswers="submitAnswers"
			:totalQuestions="quiz.questions_number"
		/>
		<div class="main">
			<Sidebar :isCollapsed="isCollapsed" :toggleQuestionList="toggleQuestionList">
				<template v-if="!loading && quiz.quiz_question">
					<QuestionList :questions="quiz.quiz_question" :goToQuestion="goToQuestion" />
				</template>
			</Sidebar>
			<div class="content" :style="{ width: isCollapsed ? 'calc(100% - 40px)' : '80%' }" id="content">
				<template v-if="!loading && quiz.quiz_question">
					<QuestionContent :questions="quiz.quiz_question" :currentQuestion="currentQuestion" />
					<Options
						:questions="quiz.quiz_question"
						:currentQuestion="currentQuestion"
						:markAnswered="markAnswered"
					/>
				</template>
			</div>
		</div>
		<Footer
			:nextQuestion="nextQuestion"
			:currentQuestion="currentQuestion"
			:questionsNumber="quiz.questions_number"
			:submitAnswers="submitAnswers"
		/>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useQuizStore } from "@/stores/quizStore";
import { storeToRefs } from "pinia";

import Header from "@/components/quiz/quiz/Header.vue";
import SubHeader from "@/components/quiz/quiz/SubHeader.vue";
import Sidebar from "@/components/quiz/quiz/Sidebar.vue";
import QuestionList from "@/components/quiz/quiz/QuestionList.vue";
import QuestionContent from "@/components/quiz/quiz/QuestionContent.vue";
import Footer from "@/components/quiz/quiz/Footer.vue";
import Options from "@/components/quiz/quiz/Options.vue";

const isCollapsed = ref(false);
const currentQuestion = ref(0);
const quizName = ref("2874210861");

const quizStore = useQuizStore();
const { quiz, loading, error } = storeToRefs(quizStore);

const timeLeft = ref(quiz.value.duration);

const formattedTime = computed(() => {
	const hours = Math.floor(timeLeft.value / 3600);
	const minutes = Math.floor((timeLeft.value % 3600) / 60);
	const seconds = timeLeft.value % 60;
	return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds
		.toString()
		.padStart(2, "0")}`;
});

const startCountdown = () => {
	const interval = setInterval(() => {
		if (timeLeft.value > 0) {
			timeLeft.value--;
		} else {
			clearInterval(interval);
			alert("Time is up!");
			submitAnswers();
		}
	}, 1000);
};

const toggleQuestionList = () => {
	isCollapsed.value = !isCollapsed.value;
};

const nextQuestion = () => {
	if (currentQuestion.value < quiz.value.questions_number - 1) {
		currentQuestion.value++;
	}
};

const prevQuestion = () => {
	if (currentQuestion.value > 0) {
		currentQuestion.value--;
	}
};

const goToQuestion = (index) => {
	currentQuestion.value = index;
};

const markAnswered = (questionIndex, answer) => {
	const updatedQuestions = [...quiz.value.quiz_question];
	updatedQuestions[questionIndex] = {
		...updatedQuestions[questionIndex],
		selectedAnswer: answer,
	};
	quiz.value.quiz_question = updatedQuestions;
};

const submitAnswers = () => {
	alert("Answers submitted!");
};

onMounted(() => {
	quizStore.fetchQuiz(quizName.value);
	startCountdown();
});

watch(
	() => quiz.value,
	(newQuiz) => {
		timeLeft.value = newQuiz.duration;
		startCountdown(); // Restart the countdown if quiz changes
	}
);
</script>

<style scoped>
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}
html,
body {
	height: 100%;
	margin: 0;
}
.container {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}
.header,
.sub-header,
.footer {
	flex-shrink: 0;
}
.main {
	display: flex;
	flex: 1;
	overflow: hidden;
}
.content {
	display: flex;
	flex-direction: column;
	flex: 1;
	overflow: hidden;
}
@media (max-width: 768px) {
	.content {
		width: calc(100% - 40px);
	}
	.sidebar {
		width: 40px;
		overflow: visible;
	}
}
</style>
