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
@import "@/assets/style/QuizList.css";
</style>
