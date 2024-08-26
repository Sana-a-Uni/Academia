<template>
	<aside class="sidebar" :class="{ open: isOpen }">
		<nav>
			<ul>
				<li>
					<router-link to="/studentDashboard" class="menu-link">
						<font-awesome-icon icon="tachometer-alt" class="menu-icon" /> Dashboard
					</router-link>
				</li>

				<li>
					<router-link :to="{ name: 'courseContentView' }" class="menu-link"
						><font-awesome-icon icon="folder-open" class="menu-icon" /> Course Content
					</router-link>
				</li>

				<li>
					<router-link :to="{ name: 'assignmentView' }" class="menu-link"
						><font-awesome-icon icon="tasks" class="menu-icon" /> Assignments
					</router-link>
				</li>

				<li>
					<router-link
						:to="{
							name: 'quizView',
						}"
						class="menu-link"
					>
						<font-awesome-icon icon="question-circle" class="menu-icon" /> Quiz
					</router-link>
				</li>
				<li>
					<router-link :to="{ name: 'grades' }">
						<font-awesome-icon icon="chart-bar" class="menu-icon" />
						Grades</router-link
					>
				</li>
			</ul>
		</nav>
	</aside>
</template>

<script setup>
import { ref } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
	faTachometerAlt,
	faBook,
	faFolderOpen,
	faBullhorn,
	faTasks,
	faQuestionCircle,
	faChartBar,
} from "@fortawesome/free-solid-svg-icons";

library.add(
	faTachometerAlt,
	faBook,
	faFolderOpen,
	faBullhorn,
	faTasks,
	faQuestionCircle,
	faChartBar
);

const props = defineProps({
	isOpen: Boolean,
});
</script>

<style scoped>
.sidebar {
	position: fixed;
	top: 63px;
	left: 0;
	width: 15%;
	height: calc(100% - 70px);
	background-color: #f4f4f4;
	padding: 20px;
	box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
	z-index: 1000;
	display: block;
}
.sidebar.open {
	display: block;
}

.sidebar nav ul {
	list-style: none;
	padding: 0;
	margin: 0;
}

.sidebar nav ul li {
	margin-bottom: 10px;
	border-bottom: 1px solid #ddd;
	padding-bottom: 10px;
}

.sidebar nav ul li:last-child {
	border-bottom: none;
}

.sidebar nav ul li a,
.sidebar nav ul li .menu-link {
	color: #333;
	text-decoration: none;
	padding: 10px;
	display: flex;
	align-items: center;
	border-radius: 4px;
}

.sidebar nav ul li a:hover,
.sidebar nav ul li .menu-link:hover {
	background-color: #ddd;
}

.sidebar nav ul li a .menu-icon,
.sidebar nav ul li .menu-link .menu-icon {
	margin-right: 10px;
	color: #0584ae;
	font-size: 16px;
	width: 16px;
	height: 16px;
}

@media (max-width: 768px) {
	.sidebar {
		display: none;
		position: fixed;
		left: -100%;
		width: 70%;
		height: 100%;
		background-color: #f4f4f4;
		overflow-y: auto;
		transition: left 0.3s ease-in-out;
	}

	.sidebar.open {
		left: 0;
	}
}
</style>
