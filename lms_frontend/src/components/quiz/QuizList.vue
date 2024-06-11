<template>
	<div class="quiz-list">
		<div class="header">
			<h2>All Quizzes</h2>
			<div class="filters">
				<select v-model="selectedQuiz" class="custom-select">
					<option value="all">All Quizzes</option>
					<option value="homework">Homework</option>
					<option value="tests">Tests</option>
				</select>
			</div>
		</div>
		<table>
			<thead>
				<tr>
					<th class="due-column">Due</th>
					<th class="quiz-column">Quiz</th>
					<th class="time-limit-column">Time Limit</th>
					<th class="attempts-column">Attempts</th>
					<th class="grade-column">Grade</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="quiz in filteredQuizzes" :key="quiz.id">
					<td class="due-column">
						<div>{{ formatDate(quiz.to_date) }}</div>
						<div>{{ formatTime(quiz.to_date) }}</div>
					</td>
					<td class="quiz-column">
						<a :href="quiz.link">{{ quiz.title }}</a>
					</td>
					<td class="time-limit-column">{{ formatDuration(quiz.duration) }}</td>
					<td class="attempts-column">
						{{ quiz.attempts_taken }} of {{ quiz.number_of_attempts }}
					</td>
					<td class="grade-column">
						{{ quiz.grade ? `${quiz.grade} / ${quiz.total_grades}` : "" }}
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
import { ref, computed, defineProps } from "vue";

const props = defineProps({
	quizzes: {
		type: Array,
		required: true,
	},
});

const selectedQuiz = ref("all");

const filteredQuizzes = computed(() => {
	return props.quizzes.filter((quiz) => {
		return selectedQuiz.value === "all" || quiz.type === selectedQuiz.value;
	});
});

function formatDuration(seconds) {
	if (typeof seconds !== "number") {
		return "";
	}

	const days = Math.floor(seconds / (24 * 3600));
	const remainingSecondsAfterDays = seconds % (24 * 3600);
	const hours = Math.floor(remainingSecondsAfterDays / 3600);
	const remainingSecondsAfterHours = remainingSecondsAfterDays % 3600;
	const minutes = Math.floor(remainingSecondsAfterHours / 60);

	const parts = [];
	if (days > 0) parts.push(`${days}d`);
	if (hours > 0) parts.push(`${hours}h`);
	if (minutes > 0) parts.push(`${minutes}m`);

	return parts.join(" ");
}

function formatDate(dateString) {
	const date = new Date(dateString);
	const day = date.getDate().toString().padStart(2, "0");
	const month = (date.getMonth() + 1).toString().padStart(2, "0"); // Months are zero-indexed
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
	margin: 0px 10px;
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
	width: calc(100% - 40px); /* Adjust the width to leave space on both sides */
	margin: 0 20px; /* Add margins to the left and right */
	border: 1px solid #ddd;
}

th,
td {
	padding: 12px;
	border: 1px solid #ddd;
	vertical-align: middle; /* Center align vertically for both th and td */
}

th {
	background-color: #f4f4f4;
	text-align: center; /* Center align header cells horizontally */
}

a {
	color: #2a73cc;
	text-decoration: none;
}

a:hover {
	text-decoration: underline;
}

.due-column {
	width: 10%;
}

.due-column div {
	line-height: 1.5;
}

.quiz-column {
	width: 55%;
}

.time-limit-column,
.attempts-column,
.grade-column {
	width: 10%;
	text-align: center; /* Center align content horizontally */
}

@media (max-width: 768px) {
	h2 {
		font-size: 18px; /* Reduce font size for smaller screens */
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
		font-size: 14px; /* Reduce font size for smaller screens */
	}

	table {
		width: 100%; /* Make table full width on smaller screens */
		margin: 0; /* Remove side margins on smaller screens */
	}

	th,
	td {
		font-size: 12px; /* Reduce font size on smaller screens */
		padding: 8px; /* Reduce padding on smaller screens */
	}

	.due-column,
	.time-limit-column,
	.attempts-column,
	.grade-column {
		width: auto; /* Auto width for columns on smaller screens */
	}

	.quiz-column {
		width: auto; /* Auto width for quiz column on smaller screens */
	}
}
</style>
