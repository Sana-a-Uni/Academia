<template>
	<div class="dialog-backdrop">
		<div class="dialog-content">
			<div class="dialog-header">
				<div class="checkmark-circle">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
					>
						<path fill="none" stroke="#fff" stroke-width="2" d="M20 6L9 17l-5-5" />
					</svg>
				</div>
			</div>
			<div class="dialog-body">
				<h2>Success!</h2>
				<p>{{ message }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
	message: {
		type: String,
		required: true,
	},
});
</script>

<style scoped>
.dialog-backdrop {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
	z-index: 9999;
}

.dialog-content {
	background: white;
	padding: 20px;
	border-radius: 10px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	width: 300px;
	text-align: center;
	position: relative;
}

.dialog-header {
	position: absolute;
	top: -30px;
	left: 50%;
	transform: translateX(-50%);
	width: 60px;
	height: 60px;
	background-color: #8bc34a;
	border-radius: 50%;
	display: flex;
	justify-content: center;
	align-items: center;
}

.checkmark-circle {
	width: 60px;
	height: 60px;
	background-color: #8bc34a;
	border-radius: 50%;
	display: flex;
	justify-content: center;
	align-items: center;
}

.dialog-body {
	margin-top: 40px;
}

.dialog-body h2 {
	margin: 10px 0;
	color: #333;
}

.dialog-body p {
	margin: 10px 0;
	color: #666;
}

.dialog-footer {
	margin-top: 20px;
}

.dialog-button {
	background-color: #8bc34a;
	color: white;
	border: none;
	padding: 10px 20px;
	border-radius: 5px;
	cursor: pointer;
	font-size: 16px;
}

.dialog-button:hover {
	background-color: #7cb342;
}
</style>
