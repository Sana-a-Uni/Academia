<template>
	<div class="main">
		<div class="courses">
			<div class="scrollable-card">
				<h3 style="padding-left: 20px">Courses</h3>
				<!-- <div class="tabs">
					<div class="tab">Active</div>
					<div class="tab">Completed</div>
				</div> -->
				<div class="courses-grid">
					<div
						class="card"
						v-for="(course, index) in courses"
						:key="index"
						@click="navigateToCourseView(course)"
					>
						<img src="@/assets/images/book1.jpeg" alt="course image" />
						<h3>{{ course.title }}</h3>
						<div class="info">
							<p>{{ course.instructor }}</p>
							<p>{{ course.type }}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="notifications">
			<div class="scrollable-card">
				<h3 style="padding-left: 20px">Notifications</h3>
				<div
					class="notification"
					v-for="(notification, index) in notifications"
					:key="index"
				>
					<div class="notification-date">
						{{ notification.date }}
					</div>
					<div class="notification-info">
						<h4>{{ notification.title }}</h4>
						<p>{{ notification.description }}</p>
					</div>
					<i class="fas fa-bell"></i>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const courses = ref([
	{
		image: "images/book1.jpeg",
		title: "DataBase",
		instructor: "Ebrahim Alhadad",
		type: "Lab",
	},
	{
		image: "images/book1.jpeg",
		title: "DataBase",
		instructor: "Ebrahim Alhadad",
		type: "Lab",
	},
	{
		image: "images/book1.jpeg",
		title: "DataBase",
		instructor: "Ebrahim Alhadad",
		type: "Lab",
	},
	{
		image: "images/book1.jpeg",
		title: "DataBase",
		instructor: "Ebrahim Alhadad",
		type: "Lab",
	},
	{
		image: "images/book1.jpeg",
		title: "DataBase",
		instructor: "Ebrahim Alhadad",
		type: "Lab",
	},
	{
		image: "images/book1.jpeg",
		title: "DataBase",
		instructor: "Ebrahim Alhadad",
		type: "Lab",
	},
	{
		image: "images/book1.jpeg",
		title: "DataBase",
		instructor: "Ebrahim Alhadad",
		type: "Lab",
	},
]);

const notifications = ref([
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
	{
		date: "22 Jan",
		title: "Algorithm",
		description: "3 hour .Dr\\Ghallib",
	},
]);

const navigateToCourseView = (course) => {
	router.push(`/teacherDashboard/courseView`);
};
</script>

<style scoped>
.main {
	display: flex;
	flex: 1;
	flex-direction: column;
}

.courses,
.notifications {
	padding-left: 20px;
	padding-right: 20px;
	background-color: white;
}

.courses {
	flex: 2;
	overflow: hidden;
	margin-left: 20px;
	margin-right: 20px;
	border-radius: 10px;
}

.notifications {
	flex: 1;
	overflow-y: auto;
	margin-right: 20px;
	border-radius: 10px;
}

.scrollable-card {
	max-height: 600px;
	overflow-y: auto;
	padding: 20px;
	border-radius: 10px;
}

.card {
	background-color: #f0f5f9;
	margin-top: 20px;
	margin-left: 20px;
	margin-right: 20px;
	border-radius: 10px;
	width: 87%;
	height: 95%;
	cursor: pointer;
}

.card img {
	width: 100%;
	height: 100px;
	object-fit: cover;
	border-radius: 10px 10px 0 0;
}

.card h3 {
	text-align: center;
	margin: 10px 0;
}

.card .info {
	display: flex;
	justify-content: space-between;
	padding: 0 20px;
}

.card p {
	text-align: center;
	margin: 5px 0;
}

.tabs {
	display: flex;
	justify-content: start;
	margin-top: 20px;
}

.tab {
	margin: 0 20px;
	cursor: pointer;
}

.notification {
	display: flex;
	align-items: center;
	margin-bottom: 10px;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 10px;
	background-color: #f0f5f9;
	margin-left: 15px;
	margin-right: 15px;
}

.notification-date {
	text-align: center;
	padding: 10px;
	border-right: 1px solid #ccc;
	margin-right: 10px;
}

.notification-info {
	flex: 1;
	margin-left: 10px;
}

.notification-info h4 {
	margin: 0;
}

.courses-grid {
	display: grid;
	grid-template-columns: 1fr;
	gap: 20px;
}

@media (min-width: 600px) {
	.courses-grid {
		grid-template-columns: repeat(2, 1fr);
	}
}

@media (min-width: 900px) {
	.main {
		flex-direction: row;
	}

	.courses-grid {
		grid-template-columns: repeat(3, 1fr);
	}
}
</style>
