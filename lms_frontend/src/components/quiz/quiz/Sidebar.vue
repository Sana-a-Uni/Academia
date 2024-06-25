<template>
	<div class="sidebar" :class="{ 'collapsed-container': isCollapsed }">
		<button class="expand-button" v-if="isCollapsed" @click="toggleQuestionList">&#9654;</button>
		<div class="question-list-container">
			<div class="question-list-title" :class="{ 'collapsed-title': isCollapsed }">
				Question List
				<button class="toggle-button" v-if="!isCollapsed" @click="toggleQuestionList">&#9664;</button>
			</div>
			<slot></slot>
		</div>
	</div>
</template>

<script setup>
const props = defineProps({
	isCollapsed: {
		type: Boolean,
		required: true,
	},
	toggleQuestionList: {
		type: Function,
		required: true,
	},
});
</script>

<style scoped>
.sidebar {
	width: 20%;
	border-right: 1px solid #ccc;
	box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
	display: flex;
	flex-direction: column;
	position: relative;
	transition: width 0.3s ease;
}
.expand-button,
.toggle-button {
	cursor: pointer;
	padding: 5px;
	border: none;
	background: none;
	font-size: 16px;
}
.question-list-container {
	flex: 1;
	display: flex;
	flex-direction: column;
	overflow: hidden;
}
.question-list-title {
	font-size: 1.5em;
	font-weight: bold;
	padding: 20px;
	background: white;
	z-index: 1;
	position: sticky;
	top: 0;
	display: flex;
	justify-content: space-between;
	align-items: center;
	transition: opacity 0.3s ease;
}
.collapsed-container {
	width: 40px;
}
.collapsed-title {
	opacity: 0;
}
@media (max-width: 768px) {
	.sidebar {
		width: 40px;
	}
	.expand-button,
	.toggle-button {
		display: none !important;
	}
	.collapsed-container .expand-button {
		display: block;
	}
}
</style>
