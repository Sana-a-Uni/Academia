<template>
	<div class="options">
		<div
			v-if="
				questions[currentQuestion] &&
				questions[currentQuestion].question_options &&
				questions[currentQuestion].question_options.length
			"
		>
			<label
				v-for="(choice, index) in questions[currentQuestion].question_options"
				:key="index"
				class="option-label"
			>
				<input
					v-if="questions[currentQuestion].question_type === 'Multiple Choice'"
					type="radio"
					:name="'answer' + currentQuestion"
					:value="choice.option"
					@change="() => markAnswered(currentQuestion, choice.option)"
					:checked="
						mode === 'review'
							? questions[currentQuestion].selected_option === choice.option
							: questions[currentQuestion].selectedAnswer === choice.option
					"
					:disabled="mode === 'review'"
				/>
				<input
					v-if="questions[currentQuestion].question_type === 'Multiple Answer'"
					type="checkbox"
					:name="'answer' + currentQuestion"
					:value="choice.option"
					@change="(event) => markAnswered(currentQuestion, choice.option, event.target.checked)"
					:checked="
						mode === 'review'
							? questions[currentQuestion].selected_option.includes(choice.option)
							: Array.isArray(questions[currentQuestion].selectedAnswer)
							? questions[currentQuestion].selectedAnswer.includes(choice.option)
							: false
					"
					:disabled="mode === 'review'"
				/>
				<span
					:class="{
						'correct-answer': mode === 'review' && choice.is_correct,
						'wrong-answer':
							mode === 'review' &&
							!choice.is_correct &&
							(questions[currentQuestion].selected_option === choice.option ||
								(Array.isArray(questions[currentQuestion].selected_option) &&
									questions[currentQuestion].selected_option.includes(choice.option))),
						'selected-answer':
							mode !== 'review' &&
							(questions[currentQuestion].selectedAnswer === choice.option ||
								(Array.isArray(questions[currentQuestion].selectedAnswer) &&
									questions[currentQuestion].selectedAnswer.includes(choice.option))),
					}"
				>
					{{ choice.option }}
				</span>
				<span v-if="mode === 'review' && choice.is_correct"></span>
			</label>
		</div>
		<div v-else>No options available</div>
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
	mode: {
		type: String,
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
.option-label {
	display: flex;
	align-items: center;
	margin-bottom: 10px;
}
.option-label input {
	margin-right: 10px;
}
.correct-answer {
	color: green;
}
.wrong-answer {
	color: red;
}
</style>
