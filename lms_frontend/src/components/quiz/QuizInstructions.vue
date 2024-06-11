<template>
	<div class="container">
		<h1>Quiz Instructions</h1>
		<div class="instructions">
			<p>
				Welcome to <strong>{{ instructions[6] }}</strong> in <strong>{{ instructions[7] }}</strong> !
				Please read the following instructions carefully before you begin:
			</p>
			<ul>
				<li>
					Attempts allowed: <strong>{{ instructions[0] }}</strong>
				</li>
				<li>
					Time limit: <strong>{{ instructions[1] }} minutes</strong>
				</li>
				<li>
					Number of questions: <strong>{{ instructions[2] }}</strong>
				</li>
				<li>
					Total score: <strong>{{ instructions[3] }} points</strong>
				</li>
				<li>
					End time: <strong>{{ instructions[4] }}</strong>
				</li>
				<li>Instructor's notes: {{ instructions[5] }}</li>
			</ul>
		</div>
		<div class="btn-container">
			<router-link to="/" class="btn btn-start">Start Quiz</router-link>
			<router-link to="/" class="btn btn-cancel">Cancel</router-link>
		</div>
	</div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
	instructions: {
		type: Array,
	},
});
</script>

<style scoped>
body {
	font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
	background-color: #eef2f7;
	color: #333;
	margin: 200px 20px;
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
	text-align: center;
}

.container {
	background-color: #fff;
	border-radius: 15px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	width: 95%;
	padding: 20px;
	margin: 0px 30px;
}

.instructions {
	overflow-y: auto;
	max-height: calc(100vh - 210px); /* Adjusted for fixed header, footer and padding */
}

h1 {
	color: #0584ae;
	margin-bottom: 10px; /* Reduced margin */
}

p {
	color: #555;
	margin-bottom: 20px;
}

ul {
	list-style-type: none;
	padding: 0;
	text-align: left;
	color: #555;
}

ul li {
	margin-bottom: 10px;
	display: flex;
	align-items: flex-start; /* Align items to the start to handle multiline */
}

ul li::before {
	content: "✔";
	color: #0584ae;
	margin-right: 10px;
	flex-shrink: 0; /* Prevent the checkmark from shrinking */
}

.btn-container {
	display: flex;
	justify-content: center;
	gap: 10px;
	margin-top: 10px; /* Reduced margin */
}

.btn {
	display: inline-block;
	padding: 10px 20px;
	color: #fff;
	text-decoration: none;
	border-radius: 5px;
	transition: background-color 0.3s ease;
}

.btn-start {
	background-color: #0584ae;
}

.btn-cancel {
	background-color: #dc3545;
}

.btn-cancel:hover {
	background-color: #c82333;
}

@media (max-width: 768px) {
	h1 {
		font-size: 18px; /* Smaller font size for small screens */
	}

	.btn-container {
		gap: 5px; /* Reduce gap between buttons */
	}

	.btn {
		padding: 8px 16px; /* Smaller padding for buttons */
		font-size: 14px; /* Smaller font size for buttons */
	}

	.instructions {
		max-height: calc(100vh - 160px); /* Reduce max height to account for smaller screens */
	}

	.container {
		padding: 10px; /* Reduce padding for the container */
		margin: 0px; /* Reduce margin-top for the container */
	}
}
</style>
