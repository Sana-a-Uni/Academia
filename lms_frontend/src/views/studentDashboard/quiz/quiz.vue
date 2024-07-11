<template>
	<LoadingSpinner v-if="quizStore.loading" />
	<AttemptsLimitDialog
		v-else-if="quizStore.error"
		:showDialog="true"
		@close="goBack"
		:message="quizStore.error"
	/>
	<div v-else class="container">
		<Header />
		<SubHeader
			:formattedTime="shouldShowTimer ? formattedTime : ''"
			:currentQuestion="currentQuestion"
			:prevQuestion="prevQuestion"
			:nextQuestion="nextQuestion"
			:submitAnswers="confirmSubmit"
			:totalQuestions="quiz.questions_number"
			:mode="'attempt'"
			:closeReview="closeReview"
		/>

		<div class="main">
			<Sidebar :isCollapsed="isCollapsed" :toggleQuestionList="toggleQuestionList">
				<template v-if="!loading && quiz.quiz_question">
					<QuestionList
						:questions="quiz.quiz_question"
						:goToQuestion="goToQuestion"
						:mode="'attempt'"
					/>
				</template>
			</Sidebar>
			<div class="content" :style="{ width: isCollapsed ? 'calc(100% - 40px)' : '80%' }" id="content">
				<template v-if="!loading && quiz.quiz_question">
					<QuestionContent :questions="quiz.quiz_question" :currentQuestion="currentQuestion" />
					<Options
						:questions="quiz.quiz_question"
						:currentQuestion="currentQuestion"
						:markAnswered="markAnswered"
						:mode="'attempt'"
					/>
				</template>
			</div>
		</div>
		<Footer
			:nextQuestion="nextQuestion"
			:currentQuestion="currentQuestion"
			:questionsNumber="quiz.questions_number"
			:submitAnswers="confirmSubmit"
			:mode="'attempt'"
			:closeReview="closeReview"
		/>
		<ConfirmationDialog
			:showDialog="showDialog"
			@close="closeDialog"
			@confirm="submitAnswers"
			:message="dialogMessage"
			:unansweredCount="unansweredCount"
		/>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useQuizStore } from "@/stores/quizStore";
import { storeToRefs } from "pinia";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import Header from "@/components/quiz/quiz/Header.vue";
import SubHeader from "@/components/quiz/quiz/SubHeader.vue";
import Sidebar from "@/components/quiz/quiz/Sidebar.vue";
import QuestionList from "@/components/quiz/quiz/QuestionList.vue";
import QuestionContent from "@/components/quiz/quiz/QuestionContent.vue";
import Footer from "@/components/quiz/quiz/Footer.vue";
import Options from "@/components/quiz/quiz/Options.vue";
import ConfirmationDialog from "@/components/ConfirmationDialog.vue";
import AttemptsLimitDialog from "@/components/AttemptsLimitDialog.vue";

const isCollapsed = ref(false);
const currentQuestion = ref(0);
const route = useRoute();
const router = useRouter();
const quizName = ref(route.params.quizName);
const studentId = ref("EDU-STU-2024-00001");

const quizStore = useQuizStore();
const { quiz, loading, error } = storeToRefs(quizStore);

const timeLeft = ref(0);
const showDialog = ref(false);
const dialogMessage = ref("");
const unansweredCount = ref(0);

const interval = ref(null);

const formattedTime = computed(() => {
	const hours = Math.floor(timeLeft.value / 3600);
	const minutes = Math.floor((timeLeft.value % 3600) / 60);
	const seconds = timeLeft.value % 60;
	return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds
		.toString()
		.padStart(2, "0")}`;
});

const shouldShowTimer = ref(false);

const updateShouldShowTimer = () => {
	if (!quiz.value) return;

	const endTime = new Date(quiz.value.to_date).getTime();
	const currentTime = new Date().getTime();
	const timeRemaining = (endTime - currentTime) / 1000;

	shouldShowTimer.value = quiz.value.is_time_bound || timeRemaining <= 7200;

	if (timeRemaining <= 0) {
		clearInterval(interval.value);
		alert("الوقت انتهى!");
		confirmSubmit();
	}
};

const startCountdown = () => {
	interval.value = setInterval(() => {
		if (timeLeft.value > 0) {
			timeLeft.value--;
			updateShouldShowTimer();
		} else {
			clearInterval(interval.value);
			alert("الوقت انتهى!");
			confirmSubmit();
		}
	}, 1000);
};

const stopCountdown = () => {
	if (interval.value) {
		clearInterval(interval.value);
		interval.value = null;
	}
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

const markAnswered = (questionIndex, option, checked = false) => {
	const updatedQuestions = [...quiz.value.quiz_question];
	const question = updatedQuestions[questionIndex];

	if (question.question_type === "Multiple Choice") {
		question.selectedAnswer = option;
	} else if (question.question_type === "Multiple Answer") {
		if (!question.selectedAnswer) {
			question.selectedAnswer = [];
		}
		if (checked) {
			question.selectedAnswer.push(option);
		} else {
			question.selectedAnswer = question.selectedAnswer.filter((item) => item !== option);
		}
	}

	quiz.value.quiz_question = updatedQuestions;
};

const startTime = new Date().toISOString().replace("T", " ").split(".")[0];

const confirmSubmit = () => {
	unansweredCount.value = quiz.value.quiz_question.filter(
		(q) => !q.selectedAnswer || q.selectedAnswer.length === 0
	).length;
	dialogMessage.value =
		unansweredCount.value > 0 ? "You have NOT completed your quiz!" : "You want to submit your quiz";
	showDialog.value = true;

	if (shouldShowTimer.value) {
		stopCountdown(); // إيقاف المؤقت عند عرض رسالة التأكيد
	}
};

const closeDialog = () => {
	showDialog.value = false;
};

const submitAnswers = async () => {
	if (shouldShowTimer.value) {
		stopCountdown(); // إيقاف المؤقت عند إرسال الإجابات
	}
	showDialog.value = false;

	const answers = quiz.value.quiz_question.map((q) => {
		if (q.question_type === "Multiple Choice") {
			return {
				question: q.name,
				selected_option: q.selectedAnswer || "",
			};
		} else if (q.question_type === "Multiple Answer") {
			return {
				question: q.name,
				selected_option: q.selectedAnswer || [],
			};
		}
	});

	const quizAttemptId = await quizStore.submitQuiz({
		student: "EDU-STU-2024-00001",
		quiz: quizName.value,
		start_time: startTime,
		answers: answers,
	});

	if (quizAttemptId) {
		router.push({ name: "quizResult", params: { quizAttemptId } });
	} else {
		alert("حدث خطأ أثناء إرسال الامتحان.");
	}
};

const closeReview = () => {
	router.push({ name: "home" });
};

const goBack = () => {
	router.go(-1);
	stopCountdown(); // إيقاف المؤقت عند العودة للخلف
};

onMounted(() => {
	quizStore.fetchQuiz(quizName.value, studentId.value).then(() => {
		if (quizStore.error && quizStore.error.includes("403")) {
			alert(quizStore.error);
			router.push({ name: "quizView" });
			return;
		}

		updateShouldShowTimer();

		const endTime = new Date(quiz.value.to_date).getTime();
		const currentTime = new Date().getTime();
		const remainingTime = Math.floor((endTime - currentTime) / 1000);
		if (quiz.value.duration) {
			timeLeft.value = Math.min(quiz.value.duration, remainingTime);
		} else {
			timeLeft.value = remainingTime;
		}

		startCountdown();
	});
});

watch(
	() => quiz.value,
	(newQuiz) => {
		updateShouldShowTimer();

		const endTime = new Date(newQuiz.to_date).getTime();
		const currentTime = new Date().getTime();
		const remainingTime = Math.floor((endTime - currentTime) / 1000);
		if (newQuiz.duration) {
			timeLeft.value = Math.min(newQuiz.duration, remainingTime);
		} else {
			timeLeft.value = remainingTime;
		}
	}
);

watch(
	() => timeLeft.value,
	() => {
		updateShouldShowTimer();
	}
);

onBeforeUnmount(() => {
	stopCountdown();
});
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
