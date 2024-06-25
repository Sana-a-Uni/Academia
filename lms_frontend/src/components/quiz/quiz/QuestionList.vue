<template>
	<div class="question-list">
		<ul>
			<li
				v-for="(question, index) in questions"
				:key="index"
				:class="{
					'correct-question': mode === 'review' && question.is_correct,
					'wrong-question': mode === 'review' && !question.is_correct && question.selected_option,
					'unanswered-question': mode === 'review' && !question.selected_option,
					'checked-question': mode === 'attempt' && question.selectedAnswer,
				}"
				@click="goToQuestion(index)"
			>
				<div
					class="custom-radio"
					:class="{
						correct: mode === 'review' && question.is_correct,
						wrong: mode === 'review' && !question.is_correct && question.selected_option,
						unanswered: mode === 'review' && !question.selected_option,
						checked: mode === 'attempt' && question.selectedAnswer,
					}"
				>
					<span v-if="mode === 'review' && question.is_correct">✔</span>
					<span v-if="mode === 'review' && !question.is_correct && question.selected_option"
						>✘</span
					>
				</div>
				<label>Question {{ index + 1 }}</label>
			</li>
		</ul>
	</div>
</template>

<script setup>
const props = defineProps({
	questions: {
		type: Array,
		required: true,
	},
	goToQuestion: {
		type: Function,
		required: true,
	},
	mode: {
		type: String,
		required: true,
	},
});
</script>

<style scoped>
.question-list {
	flex: 1;
	overflow-y: auto;
	max-height: 60vh;
}
.question-list ul {
	list-style: none;
	padding: 0;
	margin: 0;
}
.question-list li {
	display: flex;
	align-items: center;
	padding: 20px;
	border-bottom: 1px solid #f0f0f0;
	cursor: pointer;
}
.question-list li:last-child {
	border-bottom: none;
}
.custom-radio {
	width: 16px;
	height: 16px;
	border-radius: 50%;
	background-color: #fff; /* Default background color */
	margin-right: 10px;
	display: flex;
	justify-content: center;
	align-items: center;
	color: white;
	font-size: 12px;
	font-weight: bold;
	position: relative;
	border: 2px solid black; /* Black border color */
}
.custom-radio::before {
	content: "";
	position: absolute;
	top: 2px;
	left: 2px;
	right: 2px;
	bottom: 2px;
	background-color: white; /* White gap */
	border-radius: 50%;
}
.custom-radio.correct {
	background-color: green !important;
	border-color: green !important;
}
.custom-radio.correct::before {
	background-color: green;
}
.custom-radio.correct span {
	color: white;
}
.custom-radio.wrong {
	background-color: red !important;
	border-color: red !important;
}
.custom-radio.wrong::before {
	background-color: red;
}
.custom-radio.wrong span {
	color: white;
}
.custom-radio.unanswered {
	background-color: white !important;
	border-color: red !important;
}
.custom-radio.checked::before {
	background-color: green;
}
.custom-radio span {
	position: absolute;
}
.question-list li label {
	font-size: 18px;
}
.question-list li:hover {
	background-color: #f9f9f9;
}
@media (max-width: 768px) {
	.question-list li label {
		display: none;
	}
	.question-list li {
		justify-content: center;
	}
}
</style>
