<template>
	<div class="quiz-result" v-if="quizResult">
		<header class="header">
			<h1>Quiz Result</h1>
		</header>
		<div class="result-details">
			<div class="details-row">
				<span class="label">Name:</span> <span class="value">Student Name</span>
			</div>
			<div class="details-row">
				<span class="label">Title:</span> <span class="value">{{ quizResult.quiz }}</span>
			</div>
			<div class="details-row">
				<span class="label">Date Start:</span> <span class="value">{{ quizResult.start_time }}</span>
			</div>
			<div class="details-row">
				<span class="label">Date Submitted:</span>
				<span class="value">{{ quizResult.end_time }}</span>
			</div>
			<div class="details-row">
				<span class="label">Time Spent:</span> <span class="value">{{ quizResult.time_taken }}</span>
			</div>
			<div class="details-row score">
				<span class="label">Grade:</span>
				<span class="value">{{ quizResult.grade }} / {{ quizResult.grade_out_of }}</span>
			</div>
		</div>
		<div class="questions-result">
			<div class="questions-row">
				<div class="questions-label">Questions: {{ quizResult.number_of_questions }}</div>
				<div class="questions-label">Correct: {{ quizResult.number_of_correct_answers }}</div>
				<div class="questions-label">Incorrect: {{ quizResult.number_of_incorrect_answers }}</div>
				<div class="questions-label">Incomplete: {{ quizResult.number_of_unanswered_questions }}</div>
			</div>
			<div class="questions-list">
				<div class="question" v-for="(q, index) in quizResult.questions_with_grades" :key="index">
					<span class="question-icon" v-if="quizResult.show_question_score">
						<i :class="q.user_grade === q.grade ? 'correct-icon' : 'incorrect-icon'"></i>
					</span>
					<template v-if="quizResult.show_correct_answer">
						<router-link
							:to="{
								name: 'quizReview',
								params: { quizAttemptId: quizResult.id, questionIndex: index },
							}"
							class="question-link"
						>
							<span class="question-number">Question {{ index + 1 }}</span>
						</router-link>
					</template>
					<template v-else>
						<span class="question-number">Question {{ index + 1 }}</span>
					</template>
					<span class="question-score" v-if="quizResult.show_question_score"
						>({{ q.user_grade }} / {{ q.grade }})</span
					>
				</div>
			</div>
		</div>
	</div>
	<div v-else>
		<p>No quiz result available.</p>
	</div>
</template>

<script setup>
const props = defineProps({
	quizResult: {
		type: Object,
		required: true,
	},
});
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
	color: black; /* النص يكون باللون الأسود افتراضياً */
}

.question-link {
	text-decoration: none;
	color: #2a73cc;
	display: flex;
	align-items: center;
}

.question-link:hover {
	text-decoration: underline;
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
