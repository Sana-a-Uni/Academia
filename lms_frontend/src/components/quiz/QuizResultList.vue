<template>
	<div class="quiz-list">
		<div class="header">
			<h2>All Quizzes Results</h2>
			<div class="filters">
				<select v-model="selectedQuiz" class="custom-select">
					<option value="all">All Quizzes</option>
					<option value="passed">Passed</option>
					<option value="failed">Failed</option>
				</select>
			</div>
		</div>
		<table>
			<thead>
				<tr>
					<th class="quiz-column">Quiz</th>
					<th class="review-column">Review</th>
					<th class="grade-column">Grade</th>
					<th class="time-taken-column">Time Taken</th>
					<th class="date-started-column">Date Started</th>
					<th class="date-ended-column">Date Ended</th>
				</tr>
			</thead>
			<tbody>
				<tr v-if="filteredQuizzes.length === 0">
					<td colspan="6" class="no-data">No Data</td>
				</tr>
				<tr v-else v-for="quiz in filteredQuizzes" :key="quiz.name">
					<td class="quiz-column">{{ quiz.quiz }}</td>
					<td class="review-column">
						<template v-if="quiz.show_correct_answer">
							<router-link
								:to="{ name: 'quizReview', params: { quizAttemptId: quiz.name } }"
								class="review-link"
							>
								Review
							</router-link>
						</template>
						<template v-else>
							<span class="review-disabled">Review</span>
						</template>
					</td>
					<td class="grade-column">
						{{ `${quiz.grade} / ${quiz.grade_out_of}` }}
					</td>
					<td class="time-taken-column">{{ quiz.time_taken }}</td>
					<td class="date-started-column">
						{{ formatDate(quiz.start_time) }} {{ formatTime(quiz.start_time) }}
					</td>
					<td class="date-ended-column">
						{{ formatDate(quiz.end_time) }} {{ formatTime(quiz.end_time) }}
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
	quizzesResult: {
		type: Array,
		required: true,
	},
});

const selectedQuiz = ref("all");

const filteredQuizzes = computed(() => {
	if (!props.quizzesResult) return [];
	return props.quizzesResult.filter((quiz) => {
		switch (selectedQuiz.value) {
			case "passed":
				return quiz.grade >= 50;
			case "failed":
				return quiz.grade < 50;
			default:
				return true;
		}
	});
});

function formatDate(dateString) {
	const date = new Date(dateString);
	const day = date.getDate().toString().padStart(2, "0");
	const month = (date.getMonth() + 1).toString().padStart(2, "0");
	const year = date.getFullYear();
	return `${day}/${month}/${year}`;
}

function formatTime(dateString) {
	const date = new Date(dateString);
	let hours = date.getHours();
	const minutes = date.getMinutes();
	const ampm = hours >= 12 ? "PM" : "AM";
	hours = hours % 12;
	hours = hours ? hours : 12; // the hour '0' should be '12'
	const strMinutes = minutes < 10 ? "0" + minutes : minutes;
	return hours + ":" + strMinutes + " " + ampm;
}
</script>

<style scoped>
.quiz-list {
	width: 100%;
	margin: 90px auto;
	border-collapse: collapse;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20px;
	padding: 0 20px;
	position: relative;
}

.filters {
	flex: 1;
	display: flex;
	justify-content: flex-start;
}

.filters select {
	padding: 8px;
	padding-right: 32px; /* Add space for arrow */
	border: 1px solid #ddd;
	border-radius: 4px;
	font-size: 16px;
	appearance: none; /* Remove default arrow */
	background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down"><polyline points="6 9 12 15 18 9"></polyline></svg>')
		no-repeat right 8px center;
	background-size: 16px 16px;
}

h2 {
	margin: 0;
	font-size: 24px;
	position: absolute;
	left: 50%;
	transform: translateX(-50%);
}

table {
	width: calc(100% - 40px);
	margin: 0 20px;
	border: 1px solid #ddd;
	margin-top: 20px; /* Add space between header and table */
}

th,
td {
	padding: 12px;
	border: 1px solid #ddd;
	vertical-align: middle;
}

th {
	background-color: #f4f4f4;
	text-align: center;
}

.quiz-column,
.review-column,
.grade-column,
.time-taken-column,
.date-started-column,
.date-ended-column {
	width: 16%;
	text-align: center;
}

.review-link {
	color: #2a73cc;
	text-decoration: none;
	cursor: pointer;
}

.review-link:hover {
	text-decoration: underline;
}

.review-disabled {
	color: black;
	cursor: not-allowed;
}

.no-data {
	text-align: center;
	color: #666;
	font-size: 1.2em;
	padding: 20px;
}

@media (max-width: 768px) {
	h2 {
		font-size: 18px;
		position: static;
		transform: none;
		order: 1;
	}

	.filters {
		order: 2;
		flex: 1;
		display: flex;
		justify-content: flex-end;
	}

	.filters select {
		font-size: 14px;
	}

	table {
		width: 100%;
		margin: 0;
	}

	th,
	td {
		font-size: 12px;
		padding: 8px;
	}

	.quiz-column,
	.review-column,
	.grade-column,
	.time-taken-column,
	.date-started-column,
	.date-ended-column {
		width: auto;
	}

	.quiz-column {
		width: auto;
	}
}
</style>
