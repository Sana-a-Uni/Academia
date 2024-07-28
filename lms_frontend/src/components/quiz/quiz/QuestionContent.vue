<template>
	<div class="question-content">
		<div class="question-title">
			<span>Question {{ currentQuestion + 1 }}</span>
			<div class="points-badge">
				<span>{{ questions[currentQuestion].question_grade }}</span>
				<span>points</span>
			</div>
		</div>
		<div class="question-text">
			<p v-html="questions[currentQuestion].question"></p>
		</div>
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
});
</script>

<style scoped>
.question-content {
	flex: 3;
	display: flex;
	flex-direction: column;
	overflow: hidden;
	padding: 5px 15px;
	background-color: #fff;
	border-bottom: 1px solid #ddd;
	overflow-y: auto;
	max-height: 30vh;
}
.question-title {
	display: flex;
	align-items: center;
	font-weight: bold;
	font-size: 16px;
	border-bottom: 1px solid #ddd;
	padding: 2px 4px;
}
.question-text {
	flex: 1;
	margin-top: 6px;
}
.points-badge {
	display: flex;
	align-items: center;
	background-color: #f0f0f0;
	color: black;
	padding: 5px 10px;
	border-radius: 15px;
	font-weight: bold;
	margin-left: auto;
}
.points-badge span {
	margin-left: 5px;
	font-size: 13px;
}
</style>
