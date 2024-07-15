<template>
	<div class="container">
		<h1>Quiz Instructions</h1>
		<div class="instructions">
			<p>
				Welcome to <strong>{{ quizInstructions.title }}</strong> in
				<strong>{{ quizInstructions.course }}</strong
				>! Please read the following instructions carefully before you begin:
			</p>
			<ul>
				<li>
					Attempts allowed: You have
					<strong>{{ quizInstructions.number_of_attempts }}</strong> attempts to complete the quiz.
				</li>
				<li v-if="quizInstructions.duration !== null">
					Time limit: You have <strong>{{ formatDuration(quizInstructions.duration) }}</strong> to
					complete the quiz from the moment you start your attempt.
				</li>
				<li>
					Total score: The maximum possible score is
					<strong>{{ quizInstructions.total_grades }}</strong> points.
				</li>
				<li>
					Grading basis: Your grade will be determined based on
					<strong>{{ quizInstructions.grading_basis }}</strong
					>.
				</li>
				<li>
					End time: All attempts must be completed before
					<strong>{{ quizInstructions.to_date }}</strong
					>.
				</li>
				<li v-if="quizInstructions.instruction">
					<div class="inline-container">
						<span class="note-label">Notes:</span>
						<span v-html="quizInstructions.instruction" class="instruction-text"></span>
					</div>
				</li>
			</ul>
		</div>
		<div class="btn-container">
			<button @click="startQuiz" class="btn btn-start">Start Quiz</button>
			<button @click="cancel" class="btn btn-cancel">Cancel</button>
		</div>
	</div>
</template>

<script setup>
import { useRouter, useRoute } from "vue-router";

const props = defineProps({
	quizInstructions: {
		type: Object,
		required: true,
	},
});

const router = useRouter();
const route = useRoute();

const startQuiz = () => {
	const quizName = route.params.quizName;
	router.push({ name: "quiz", params: { quizName } });
};

const cancel = () => {
	router.push({ name: "quizView" });
};

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
	if (days > 0) parts.push(`${days} days`);
	if (hours > 0) parts.push(`${hours} hours`);
	if (minutes > 0) parts.push(`${minutes} minutes`);

	return parts.join(" ");
}
</script>

<style scoped>
.container {
	background-color: #fff;
	border-radius: 15px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	width: 95%;
	padding: 20px;
	margin: 0px auto;
}

.instructions {
	overflow-y: auto;
	max-height: calc(100vh - 210px);
}

h1 {
	color: #0584ae;
	margin-bottom: 10px;
}

p {
	color: #555;
	margin-bottom: 20px;
}

ul {
	list-style-type: none;
	padding: 0;
	text-align: left;
	color: #555;
}

ul li {
	margin-bottom: 10px;
	display: flex;
	align-items: flex-start;
}

ul li::before {
	content: "✔";
	color: #0584ae;
	margin-right: 10px;
	flex-shrink: 0;
}

ul li strong {
	white-space: pre;
}

ul li strong::before,
ul li strong::after {
	content: "\00a0";
}

.inline-container {
	display: flex;
	align-items: baseline;
}

.note-label {
	margin-right: 5px;
	color: #555;
}

.instruction-text {
	color: #555;
}

.btn-container {
	display: flex;
	justify-content: center;
	gap: 10px;
	margin-top: 10px;
}

.btn {
	display: inline-block;
	padding: 10px 20px;
	color: #fff;
	text-decoration: none;
	border-radius: 5px;
	transition: background-color 0.3s ease;
	cursor: pointer;
}

.btn-start {
	background-color: #0584ae;
}

.btn-cancel {
	background-color: #dc3545;
}

.btn-cancel:hover {
	background-color: #c82333;
}

@media (max-width: 768px) {
	h1 {
		font-size: 18px;
	}

	.btn-container {
		gap: 5px;
	}

	.btn {
		padding: 8px 16px;
		font-size: 14px;
	}

	.instructions {
		max-height: calc(100vh - 160px);
	}

	.container {
		padding: 10px;
		margin: 0px;
	}
}
</style>
