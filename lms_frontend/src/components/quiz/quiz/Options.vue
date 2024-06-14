<template>
	<div class="options">
		<label v-for="(choice, index) in questions[currentQuestion].question_options" :key="index">
			<input
				type="radio"
				:name="'answer' + currentQuestion"
				:value="choice.option"
				@change="() => markAnswered(currentQuestion, choice.option)"
				:checked="questions[currentQuestion].selectedAnswer === choice.option"
			/>
			{{ choice.option }}
		</label>
	</div>
</template>

<script setup>
const props = defineProps({
	questions: {
		type: Array,
		required: true,
	},
	currentQuestion: {
		type: Number,
		required: true,
	},
	markAnswered: {
		type: Function,
		required: true,
	},
});
</script>

<style scoped>
.options {
	flex: 7;
	overflow-y: auto;
	padding: 20px;
	background-color: #fff;
	max-height: 50vh;
}
.options label {
	display: block;
	margin-bottom: 10px;
}
</style>
