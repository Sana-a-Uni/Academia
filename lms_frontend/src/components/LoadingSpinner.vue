<template>
	<div class="loading-spinner">
		<font-awesome-icon :icon="['fas', 'spinner']" spin />
	</div>
</template>

<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faSpinner } from "@fortawesome/free-solid-svg-icons";

library.add(faSpinner);
</script>

<style scoped>
.loading-spinner {
	display: flex;
	align-items: center;
	justify-content: center;
	position: fixed;
	top: 50%;
	left: 60%;
	transform: translate(-50%, -50%);
}

.font-awesome-icon {
	font-size: 3em;
	color: #3498db;
}

@media (max-width: 768px) {
	.loading-spinner {
		left: 50%;
	}
}
</style>
