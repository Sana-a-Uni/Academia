<template>
	<div class="container">
		<Navbar @toggle-drawer="toggleDrawer" />
		<Subheader />

		<div class="content">
			<Sidebar :isOpen="isDrawerOpen" />
			<main class="main-content">
				<slot> </slot>
			</main>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import Navbar from "@/components/Navbar.vue";
import Sidebar from "@/components/Sidebar.vue";
import Subheader from "@/components/Subheader.vue";

const isDrawerOpen = ref(false);

const toggleDrawer = () => {
  isDrawerOpen.value = !isDrawerOpen.value;
};
</script>

<style scoped>
.container {
	display: flex;
	flex-direction: column;
}

.content {
	display: flex;
	/* margin-top: 80px; */
	margin-left: 18.5%;
	width: 88%;
}

main {
	flex: 1;
	padding: 20px;
}

@media (max-width: 768px) {
	.content {
		margin-left: 0;
		width: 100%;
	}
}
</style>
