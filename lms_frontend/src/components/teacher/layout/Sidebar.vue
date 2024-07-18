<template>
	<aside class="sidebar" :class="{ open: isOpen }">
		<nav>
			<ul>
				<li>
					<a href="#"
						><font-awesome-icon icon="tachometer-alt" class="menu-icon" /> Dashboard</a
					>
				</li>
				<li>
					<a href="#"><font-awesome-icon icon="book" class="menu-icon" /> Study Plan</a>
				</li>
				<li>
					<a href="#"
						><font-awesome-icon icon="folder-open" class="menu-icon" /> Course
						Content</a
					>
				</li>
				<li>
					<a href="#"
						><font-awesome-icon icon="bullhorn" class="menu-icon" /> Announcements</a
					>
				</li>
				<li>
					<router-link :to="{ name: 'assignments' }" class="menu-link">
						<font-awesome-icon icon="tasks" class="menu-icon" /> Assignments
					</router-link>
				</li>

				<li>
					<router-link :to="{ name: 'quizList' }" class="menu-link">
						<font-awesome-icon icon="question-circle" class="menu-icon" /> Quiz
					</router-link>
				</li>
				<li>
					<a href="#"><font-awesome-icon icon="chart-bar" class="menu-icon" /> Grades</a>
				</li>
			</ul>
		</nav>
	</aside>
</template>

<script setup>
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

// Add the icons to the library
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
	top: 63px; /* Adjust based on the height of the navbar */
	left: 0;
	width: 15%;
	height: calc(100% - 70px); /* Adjust based on the height of the navbar */
	background-color: #f4f4f4;
	padding: 20px;
	box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
	z-index: 1000;
	display: block; /* Show sidebar by default on large screens */
}

.sidebar.open {
	display: block; /* Ensure sidebar is shown when open class is added */
}

.sidebar nav ul {
	list-style: none;
	padding: 0;
	margin: 0;
}

.sidebar nav ul li {
	margin-bottom: 10px;
	border-bottom: 1px solid #ddd; /* Add bottom border */
	padding-bottom: 10px; /* Add padding to bottom */
}

.sidebar nav ul li:last-child {
	border-bottom: none; /* Remove border from last item */
}

.sidebar nav ul li a {
	color: #333;
	text-decoration: none;
	padding: 10px;
	display: flex;
	align-items: center;
	border-radius: 4px;
}

.sidebar nav ul li a:hover {
	background-color: #ddd;
}

.sidebar nav ul li a .menu-icon {
	margin-right: 10px; /* Add space between icon and text */
	color: #0584ae; /* Change icon color */
	font-size: 16px; /* Adjust the size of the icons */
	width: 16px; /* Ensure consistent icon width */
	height: 16px; /* Ensure consistent icon height */
}

@media (max-width: 768px) {
	.sidebar {
		display: none; /* Hide sidebar by default on small screens */
		position: fixed;
		left: -100%; /* Initially position off-screen to the left */
		width: 70%; /* Adjust width as needed */
		height: 100%;
		background-color: #f4f4f4;
		overflow-y: auto;
		transition: left 0.3s ease-in-out;
	}

	.sidebar.open {
		left: 0; /* Show sidebar when open class is added */
	}
}
</style>
