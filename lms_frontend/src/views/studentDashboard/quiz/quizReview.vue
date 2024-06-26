<template>
	<div class="container">
		<Header />
		<SubHeader
			:formattedTime="formattedTime"
			:currentQuestion="currentQuestion"
			:prevQuestion="prevQuestion"
			:nextQuestion="nextQuestion"
			:totalQuestions="questionsWithAnswers.length"
			:mode="'review'"
			:closeReview="closeReview"
			:submitAnswers="submitAnswers"
		/>
		<div class="main">
			<Sidebar :isCollapsed="isCollapsed" :toggleQuestionList="toggleQuestionList">
				<template v-if="!loading && questionsWithAnswers.length">
					<QuestionList
						:questions="questionsWithAnswers"
						:goToQuestion="goToQuestion"
						:mode="'review'"
					/>
				</template>
			</Sidebar>
			<div class="content" :style="{ width: isCollapsed ? 'calc(100% - 40px)' : '80%' }" id="content">
				<template v-if="!loading && questionsWithAnswers.length">
					<QuestionContent :questions="questionsWithAnswers" :currentQuestion="currentQuestion" />
					<Options
						:questions="questionsWithAnswers"
						:currentQuestion="currentQuestion"
						:mode="'review'"
						:markAnswered="markAnswered"
					/>
				</template>
				<div v-else>No Data Available</div>
			</div>
		</div>
		<Footer
			:nextQuestion="nextQuestion"
			:currentQuestion="currentQuestion"
			:questionsNumber="questionsWithAnswers.length"
			:mode="'review'"
			:closeReview="closeReview"
			:submitAnswers="submitAnswers"
		/>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
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
const route = useRoute();
const router = useRouter();
const quizAttemptId = ref(route.params.quizAttemptId);

const quizStore = useQuizStore();
const { questionsWithAnswers, loading, error } = storeToRefs(quizStore);

const formattedTime = computed(() => {
	return "--:--:--"; // No timer in review mode
});

const toggleQuestionList = () => {
	isCollapsed.value = !isCollapsed.value;
};

const nextQuestion = () => {
	if (currentQuestion.value < questionsWithAnswers.value.length - 1) {
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
	// No marking in review mode
};

const closeReview = () => {
	router.push({ name: "quizResultList" });
};

const submitAnswers = () => {
	// This function is not used in review mode, but must be passed as a prop
};

onMounted(() => {
	quizStore.fetchQuizReview(quizAttemptId.value);
	if (route.params.questionIndex !== undefined) {
		currentQuestion.value = parseInt(route.params.questionIndex, 10);
	}
	watch(questionsWithAnswers, (newVal) => {
		console.log("Questions with Answers:", newVal); // تحقق من البيانات المحدثة
	});
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
