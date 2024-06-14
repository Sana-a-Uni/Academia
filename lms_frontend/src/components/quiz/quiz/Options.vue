<template>
	<div class="options">
		<label v-for="(choice, index) in questions[currentQuestion].choices" :key="index">
			<input type="radio" :name="'answer' + currentQuestion" :value="choice" @change="markAnswered" />
			{{ choice }}
		</label>
	</div>
</template>

<script setup>
import { defineProps } from "vue";
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
