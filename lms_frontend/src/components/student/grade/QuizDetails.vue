<template>
	<div class="content">
		<div class="section-title">Quiz Details</div>
		<div v-if="quizDetails" class="detail-item">
			<span>Quiz Title:</span> {{ quizDetails.title }}
		</div>
		<div v-if="quizDetails" class="detail-item">
			<span>Grading basis:</span> {{ quizDetails.grading_basis }}
		</div>
		<div v-if="quizDetails" class="detail-item">
			<span>Due Date:</span> {{ quizDetails.to_date }}
		</div>
		<div v-if="quizDetails" class="detail-item">
			<span>Grade Possible:</span> {{ quizDetails.total_grades }}
		</div>
		<!-- <div v-if="quizDetails" class="detail-item">
			<span>Your quiz result:</span> {{ quizDetails.result_grade }}
		</div> -->
		<div class="section-title"></div>

		<div class="sections-title">Attempts Details</div>
		<div v-if="attempts && attempts.length > 0" class="attempts">
			<table>
				<thead>
					<tr>
						<th>Start Time</th>
						<th>End Time</th>
						<th>Time Taken</th>
						<th>Attempt Grade</th>
						<th>Review</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="attempt in attempts" :key="attempt.id">
						<td>{{ attempt.start_time }}</td>
						<td>{{ attempt.end_time }}</td>
						<td>{{ formatTime(attempt.time_taken) }}</td>
						<td>{{ attempt.attempt_grade }}</td>
						<td>
							<a v-if="attempt.show_correct_answer === 1" href="#">
								<router-link
									:to="{
										name: 'quizReview',
										params: { quizAttemptId: attempt.name },
									}"
									class="question-link"
								>
									Review
								</router-link>
							</a>
							<span v-else class="disabled">Review</span>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
		<div v-else>
			<p>No attempts available.</p>
		</div>
	</div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
	quizDetails: {
		type: Object,
		required: true,
		default: () => ({
			title: "",
			grading_basis: "",
			to_date: "",
			total_grades: 0,
		}),
	},
	attempts: {
		type: Array,
		required: true,
		default: () => [],
	},
});

function formatTime(seconds) {
	const days = Math.floor(seconds / (24 * 3600));
	seconds %= 24 * 3600;
	const hours = Math.floor(seconds / 3600);
	seconds %= 3600;
	const minutes = Math.floor(seconds / 60);
	seconds %= 60;

	let timeString = "";
	if (days > 0) {
		timeString += `${days}d `;
	}
	if (hours > 0) {
		timeString += `${hours}h `;
	}
	if (minutes > 0) {
		timeString += `${minutes}m `;
	}
	if (seconds > 0 || timeString === "") {
		timeString += `${seconds}s`;
	}

	return timeString.trim();
}
</script>

<style scoped>
.content {
	padding: 20px;
}
.section-title {
	font-size: 18px;
	font-weight: bold;
	margin-bottom: 10px;
	border-bottom: 1px solid #ddd;
	padding-bottom: 5px;
}
.sections-title {
	font-size: 18px;
	font-weight: bold;
	margin-bottom: 10px;
	padding-bottom: 5px;
	text-align: center;
}
.detail-item {
	margin-bottom: 10px;
}
.detail-item span {
	font-weight: bold;
}
.attempts {
	margin-top: 20px;
}
.attempts table {
	width: 100%;
	border-collapse: collapse;
}
.attempts th,
.attempts td {
	padding: 10px;
	text-align: center;
	border: 1px solid #ddd;
}
.attempts th {
	background-color: #f8f8f8;
}
.attempts .disabled {
	cursor: not-allowed;
}
.legend {
	margin-top: 20px;
	text-align: center;
}
.attempts a {
	color: #2a73cc;
	text-decoration: underline;
	text-decoration: none;
}

.attempts a:hover {
	color: #2a73cc;
	text-decoration: underline;
}
</style>
