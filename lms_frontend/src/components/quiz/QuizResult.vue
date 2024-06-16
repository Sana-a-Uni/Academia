<template>
	<div class="quiz-result">
		<header class="header">
			<h1>Quiz Result</h1>
		</header>
		<div class="result-details">
			<div class="details-row">
				<span class="label">Name:</span> <span class="value">Week 2 Quiz</span>
			</div>
			<div class="details-row">
				<span class="label">Date Start:</span> <span class="value">22/02/24 3:18pm</span>
			</div>
			<div class="details-row">
				<span class="label">Date Submitted:</span> <span class="value">22/02/24 3:18pm</span>
			</div>
			<div class="details-row">
				<span class="label">Time Spent:</span> <span class="value">31m 52s</span>
			</div>
			<div class="details-row score">
				<span class="label">Grade:</span> <span class="value"> 25/25 </span>
			</div>
		</div>
		<div class="questions-result">
			<div class="questions-row">
				<div class="questions-label">Questions: 25</div>
				<div class="questions-label">Correct: 25</div>
				<div class="questions-label">Partial Credit: 0</div>
				<div class="questions-label">Incorrect: 0</div>
				<div class="questions-label">Incomplete: 0</div>
			</div>
			<div class="questions-list">
				<div class="question" v-for="q in questions" :key="q.number">
					<span class="question-icon">
						<i :class="q.score === 1 ? 'correct-icon' : 'incorrect-icon'"></i>
					</span>
					<span class="question-number">Question {{ q.number }}</span>
					<span class="question-score">({{ q.score }}/1)</span>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";

const questions = ref(
	Array.from({ length: 25 }, (_, i) => ({
		number: i + 1,
		score: 1, // Change to 0 to simulate incorrect answers
	}))
);
</script>

<style scoped>
.quiz-result {
	font-family: Arial, sans-serif;
	width: 95%;
	margin: 0 auto;
	padding: 20px;
	border: 1px solid #ccc;
	border-radius: 15px;
	background-color: #fff;
}

.header h1 {
	text-align: left;
	margin: 0;
	border-bottom: 1px solid #ccc;
	padding-bottom: 10px;
}

.result-details {
	margin-bottom: 20px;
}

.details-row {
	display: flex;
	align-items: center;
	padding: 5px 0;
}

.details-row .label {
	margin-right: 5px;
	font-weight: bold;
}

.score .value {
	color: green;
	font-weight: bold;
}

.questions-result {
	border-top: 1px solid #ccc;
	padding-top: 10px;
	margin-top: 20px;
}

.questions-row {
	display: flex;
	justify-content: space-between;
	margin-bottom: 10px;
	padding-bottom: 10px;
	border-bottom: 1px solid #ccc;
	flex-wrap: wrap;
}

.questions-label {
	flex: 1;
	text-align: center;
	padding: 10px;
	min-width: 120px;
}

.questions-list {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
	margin-top: 10px;
}

.question {
	display: flex;
	align-items: center;
	padding: 5px;
	width: calc(25% - 10px);
	box-sizing: border-box;
	font-size: 1.1em;
}

.question-icon {
	margin-right: 5px;
}

.question-number {
	margin-right: 5px;
}

.question-score {
	margin-left: 5px;
}

.correct-icon::before {
	content: "✔";
	color: green;
}

.incorrect-icon::before {
	content: "✘";
	color: red;
}

@media (max-width: 1200px) {
	.question {
		width: calc(33.333% - 10px);
	}
}

@media (max-width: 900px) {
	.question {
		width: calc(50% - 10px);
	}
}

@media (max-width: 600px) {
	.question {
		width: 100%;
	}
}
</style>
