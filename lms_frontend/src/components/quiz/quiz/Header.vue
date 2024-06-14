<template>
	<div class="header">
		<div class="left-section">Student Name</div>
		<div class="right-section">Course Name</div>
	</div>
</template>

<style scoped>
.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	background-color: white;
	color: black;
	padding: 5px;
}
.left-section {
	font-size: 16px;
	font-weight: bold;
}
.right-section {
	font-size: 16px;
}
@media (max-width: 768px) {
	.header {
		flex-direction: column;
		align-items: center;
		text-align: center;
	}
	.header .left-section,
	.header .right-section {
		margin-bottom: 5px;
	}
}
</style>
