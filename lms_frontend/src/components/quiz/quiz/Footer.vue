<template>
	<div class="footer">
		<button :class="buttonClass" @click="handleClick">
			{{ buttonText }}
		</button>
	</div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
	nextQuestion: {
		type: Function,
		required: true,
	},
	currentQuestion: {
		type: Number,
		required: true,
	},
	questionsNumber: {
		type: Number,
		required: true,
	},
	submitAnswers: {
		type: Function,
		required: true,
	},
	mode: {
		type: String,
		required: true,
	},
	closeReview: {
		type: Function,
		required: true,
	},
});

const isLastQuestion = computed(() => props.currentQuestion === props.questionsNumber - 1);

const buttonText = computed(() => {
	if (props.mode === "review" && isLastQuestion.value) {
		return "Close";
	}
	if (props.mode === "review") {
		return "Next";
	}
	return isLastQuestion.value ? "Submit" : "Next";
});

const buttonClass = computed(() => {
	if (props.mode === "review" && isLastQuestion.value) {
		return "close-btn";
	}
	if (props.mode === "review") {
		return "next-btn";
	}
	return isLastQuestion.value ? "submit-btn" : "next-btn";
});

const handleClick = () => {
	if (props.mode === "review" && isLastQuestion.value) {
		props.closeReview();
	} else if (props.mode === "review") {
		props.nextQuestion();
	} else if (isLastQuestion.value) {
		props.submitAnswers();
	} else {
		props.nextQuestion();
	}
};
</script>

<style scoped>
.footer {
	position: fixed;
	bottom: 0;
	left: 0;
	width: 100%;
	z-index: 1000;
	display: flex;
	justify-content: flex-end;
	align-items: center;
	background-color: #f0f0f0;
	color: black;
	padding: 10px;
	margin-top: auto;
}
.next-btn {
	background-color: #0584ae;
	color: white;
	border: none;
	padding: 5px 20px;
	cursor: pointer;
	border-radius: 20px;
	margin-right: 20px;
}
.submit-btn,
.close-btn {
	background-color: #dc3545;
	color: white;
	border: none;
	padding: 5px 20px;
	cursor: pointer;
	border-radius: 20px;
	margin-right: 20px;
}
</style>
