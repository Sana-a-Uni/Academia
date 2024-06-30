<template>
	<div class="layout">
		<navbar />
		<dashboard />
	</div>
</template>

<script setup>
import navbar from "@/components/Navbar.vue";
import dashboard from "@/components/dashboard.vue";
</script>

<style>
/* Your styles for the layout */
.layout {
	display: flex;
	flex-direction: column;
	height: 100%;
	background-color: #f0f5f9;
}
</style>
