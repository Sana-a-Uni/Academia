<template>
	<div class="sub-header">
		<div v-if="mode !== 'review' && formattedTime !== ''" class="timer">{{ formattedTime }}</div>
		<div class="middle-section">
			<div class="arrows">
				<span v-if="currentQuestion > 0" @click="prevQuestion">&#9664;</span>
				<span class="question">{{ currentQuestion + 1 }} of {{ totalQuestions }}</span>
				<span v-if="currentQuestion < totalQuestions - 1" @click="nextQuestion">&#9654;</span>
			</div>
		</div>
		<button v-if="mode !== 'review'" class="submit-btn" @click="submitAnswers">Submit</button>
		<button v-if="mode === 'review'" class="close-btn" @click="closeReview">Close</button>
	</div>
</template>

<script setup>
const props = defineProps({
	formattedTime: {
		type: String,
		required: true,
	},
	currentQuestion: {
		type: Number,
		required: true,
	},
	prevQuestion: {
		type: Function,
		required: true,
	},
	nextQuestion: {
		type: Function,
		required: true,
	},
	totalQuestions: {
		type: Number,
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
	submitAnswers: {
		type: Function,
		required: true,
	},
});
</script>

<style scoped>
.sub-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	background-color: #0584ae;
	color: white;
	padding: 25px;
	position: relative;
}
.middle-section {
	display: flex;
	align-items: center;
	position: absolute;
	left: 50%;
	transform: translateX(-50%);
}
.middle-section .question {
	margin: 0 10px;
}
.middle-section .arrows {
	display: flex;
	align-items: center;
}
.middle-section .arrows span {
	cursor: pointer;
	margin: 0 5px;
}
.submit-btn,
.close-btn {
	background-color: #dc3545;
	color: white;
	border: none;
	padding: 5px 20px;
	cursor: pointer;
	border-radius: 20px;
	position: absolute;
	right: 25px;
}
.timer {
	font-size: 14px;
}
@media (max-width: 768px) {
	.sub-header {
		flex-direction: row;
		flex-wrap: nowrap;
		justify-content: space-between;
		align-items: center;
		font-size: 12px;
		padding: 15px;
	}
	.submit-btn,
	.close-btn {
		font-size: 12px;
		padding: 2px 10px;
		margin: 0 5px;
		order: 3;
	}
	.timer {
		font-size: 12px;
		margin: 0 5px;
		order: 1;
	}
	.timer::before {
		content: "T: ";
	}
	.middle-section {
		order: 2;
		margin: 0 10px;
	}
	.question {
		font-size: 12px;
		margin: 0 5px;
	}
	.question::before {
		content: "Q ";
	}
	.sub-header .middle-section .arrows span {
		font-size: 12px;
		margin: 0 2px;
	}
}

@media (min-width: 769px) {
	.sub-header {
		padding: 25px;
	}

	.timer::before {
		content: "Time Remaining: ";
	}

	.question::before {
		content: "Question ";
	}
}
</style>
