<template>
	<div class="question-list">
		<ul>
			<li
				v-for="(question, index) in questions"
				:key="index"
				:class="{ checked: question.checked }"
				@click="goToQuestion(index)"
			>
				<input type="radio" name="question" :checked="question.checked" disabled />
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
}
.question-list li:last-child {
	border-bottom: none;
}
.question-list li input[type="radio"] {
	transform: scale(1.5);
	margin-right: 15px;
}
.question-list li label {
	font-size: 18px;
	margin-left: 15px;
}
.question-list li.checked {
	color: #4caf50;
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
