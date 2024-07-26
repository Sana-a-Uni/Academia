<template>
	<div class="layout">
		<navbar />
		<dashboard />
	</div>
</template>

<script setup>
import navbar from "@/components/teacherComponents/layout/Navbar.vue";
import dashboard from "@/components/teacherComponents/dashboard/dashboard.vue";
</script>

<style>
.layout {
	display: flex;
	flex-direction: column;
	height: 100%;
	background-color: #f0f5f9;
}
</style>
