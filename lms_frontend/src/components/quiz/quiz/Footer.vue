<template>
	<div class="footer">
		<button class="next-btn" @click="nextQuestion">Next</button>
	</div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
	nextQuestion: {
		type: Function,
		required: true,
	},
});
</script>

<style scoped>
.footer {
	display: flex;
	justify-content: flex-end;
	align-items: center;
	background-color: #f0f0f0;
	color: black;
	padding: 10px;
	margin-top: auto;
}
.next-btn {
	background-color: #0584ae;
	color: white;
	border: none;
	padding: 5px 20px;
	cursor: pointer;
	border-radius: 20px;
	margin-right: 20px;
}
</style>
