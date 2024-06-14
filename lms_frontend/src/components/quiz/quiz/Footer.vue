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
});

const isLastQuestion = computed(() => props.currentQuestion === props.questionsNumber - 1);

const buttonText = computed(() => (isLastQuestion.value ? "Submit" : "Next"));
const buttonClass = computed(() => (isLastQuestion.value ? "submit-btn" : "next-btn"));

const handleClick = () => {
	if (isLastQuestion.value) {
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
.submit-btn {
	background-color: #dc3545;
	color: white;
	border: none;
	padding: 5px 20px;
	cursor: pointer;
	border-radius: 20px;
	margin-right: 20px;
}
</style>
