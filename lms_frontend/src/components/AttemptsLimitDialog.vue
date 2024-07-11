<template>
	<div v-if="showDialog" class="dialog-overlay">
		<div class="blur-background"></div>
		<div class="dialog">
			<div class="icon">!</div>
			<h2>Attempts Limit Reached</h2>
			<p>{{ message }}</p>
			<div class="buttons">
				<button @click="closeDialog">Close</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
	showDialog: {
		type: Boolean,
		required: true,
	},
	message: {
		type: String,
		required: true,
	},
});

const emit = defineEmits(["close"]);

const closeDialog = () => {
	emit("close");
};
</script>

<style scoped>
.dialog-overlay {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
	z-index: 1000;
}
.blur-background {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	backdrop-filter: blur(2px);
	z-index: -1;
}
.dialog {
	background-color: white;
	border-radius: 12px;
	box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
	width: 320px;
	text-align: center;
	padding: 40px 20px 20px;
	position: relative;
	z-index: 1001;
}
.dialog .icon {
	background-color: #ff3d4f;
	border-radius: 50%;
	width: 50px;
	height: 50px;
	display: flex;
	justify-content: center;
	align-items: center;
	position: absolute;
	top: -25px;
	left: 50%;
	transform: translateX(-50%);
	color: white;
	font-size: 24px;
	font-weight: bold;
	border: 4px solid white;
}
.dialog h2 {
	color: #ff3d4f;
	margin: 10px 0 10px;
	font-size: 23px;
}
.dialog p {
	color: #0a0a0a;
	margin: 0 0 15px;
	font-size: 17px;
	line-height: 1.5;
}
.dialog .buttons {
	display: flex;
	justify-content: center;
}
.dialog button {
	flex: 1;
	padding: 10px 0;
	border: none;
	cursor: pointer;
	font-size: 16px;
	margin: 0 5px;
	border-radius: 8px;
}
.dialog button {
	background-color: #ff3d4f;
	color: white;
}
</style>
