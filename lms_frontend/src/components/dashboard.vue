<template>
	<div class="main">
		<div class="tabs" v-show="isSmallScreen">
			<div class="tab" :class="{ active: activeTab === 'courses' }" @click="activeTab = 'courses'">
				Courses
			</div>
			<div
				class="tab"
				:class="{ active: activeTab === 'notifications' }"
				@click="activeTab = 'notifications'"
			>
				Notifications
			</div>
			<div class="tab" :class="{ active: activeTab === 'upcoming' }" @click="activeTab = 'upcoming'">
				Upcoming
			</div>
		</div>
		<div :class="{ hidden: activeTab !== 'courses' && isSmallScreen }" class="courses">
			<h3 style="padding-left: 10px; padding-top: 15px">Courses</h3>
			<div class="scrollable-card">
				<div class="courses-grid">
					<div
						class="card"
						v-for="(course, index) in courses"
						:key="index"
						@click="navigateToCourseView"
					>
						<!-- <img :src="course.image" alt="course image" /> -->
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
		<div class="not-up">
			<div
				:class="{ hidden: activeTab !== 'notifications' && isSmallScreen }"
				class="notifications"
				style="height: 402px"
			>
				<h3 style="padding-left: 20px; padding-top: 20px">Notifications</h3>
				<div class="scrollable-card-notification">
					<div class="notification" v-for="(notification, index) in notifications" :key="index">
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
			<div :class="{ hidden: activeTab !== 'upcoming' && isSmallScreen }" class="Upcoming">
				<h3 style="padding-left: 35px; padding-top: 20px">Upcoming Task</h3>
				<div class="Upcoming-content">
					<h3 style="padding-left: 35px; padding-top: 20px">Select the date:</h3>
					<div class="ava-h">
						<div class="avatar">
							<h4 style="text-align: center; margin-top: 3px">3</h4>
						</div>
						<h4 style="margin-top: 25px; margin-left: 10px">Today</h4>
						<div class="avatar">
							<h4 style="text-align: center; margin-top: 3px">4</h4>
						</div>
						<h4 style="margin-top: 25px; margin-left: 10px">Tomorrow</h4>
						<div class="avatar">
							<h4 style="text-align: center; margin-top: 3px">2</h4>
						</div>
						<h4 style="margin-top: 25px; margin-left: 10px">The Week</h4>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	data() {
		return {
			activeTab: "courses",
			isSmallScreen: false,
			courses: [
				{
					image: "@/assets/images/book1.jpeg",
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
				{
					image: "images/book1.jpeg",
					title: "DataBase",
					instructor: "Ebrahim Alhadad",
					type: "Lab",
				},
				// Add more course objects as needed
			],
			notifications: [
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
				// {
				// 	date: "22 Jan",
				// 	title: "Algorithm",
				// 	description: "3 hour .Dr\\Ghallib",
				// },
				// {
				// 	date: "22 Jan",
				// 	title: "Algorithm",
				// 	description: "3 hour .Dr\\Ghallib",
				// },
				// {
				// 	date: "22 Jan",
				// 	title: "Algorithm",
				// 	description: "3 hour .Dr\\Ghallib",
				// },
				// {
				// 	date: "22 Jan",
				// 	title: "Algorithm",
				// 	description: "3 hour .Dr\\Ghallib",
				// },
				// {
				// 	date: "22 Jan",
				// 	title: "Algorithm",
				// 	description: "3 hour .Dr\\Ghallib",
				// },
				// Add more notification objects as needed
			],
		};
	},
	created() {
		this.isSmallScreen = window.innerWidth < 900;
		window.addEventListener("resize", this.handleResize);
	},
	beforeDestroy() {
		window.removeEventListener("resize", this.handleResize);
	},
	methods: {
		handleResize() {
			this.isSmallScreen = window.innerWidth < 900;
		},
		navigateToCourseView() {
			this.$router.push("/courseview"); // Assumes you have a route set up for 'courseview'
		},
	},
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
	height: 402px;
	margin-right: 20px;
	border-radius: 10px;
}

.scrollable-card {
	max-height: 600px; /* يمكنك تعديل هذا الارتفاع حسب الحاجة */
	overflow-y: auto;
	padding: 20px;
	border-radius: 10px;
}
.scrollable-card-notification {
	max-height: 350px; /* يمكنك تعديل هذا الارتفاع حسب الحاجة */
	overflow-y: auto;
	padding: 20px;
	border-radius: 10px;
}

.card {
	background-color: #f0f5f9;
	margin-left: 10px;
	margin-right: 10px;
	padding-bottom: 15px;
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
.not-up {
	width: 35%;
	gap: 20;
}
.Upcoming {
	background-color: white;
	height: 230px;
	margin-top: 20px;
	border-radius: 10px;
	margin-right: 20px;
}
.Upcoming-content {
	background-color: #f0f5f9;
	height: 140px;
	margin-top: 20px;
	border-radius: 10px;
	margin-right: 20px;
	margin-left: 20px;
}
.avatar {
	cursor: pointer;
	border-radius: 50%;
	overflow: hidden;
	width: 30px;
	height: 30px;
	margin-left: 30px;
	margin-top: 20px;
	background-color: white;
}
.ava-h {
	display: flex;
	flex: 1;
	flex-direction: row;
}

@media (min-width: 600px) {
	.courses-grid {
		grid-template-columns: repeat(3, 1fr);
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

.tabs {
	display: none; /* إخفاء التبويبات في الشاشات الكبيرة */
}

.tab {
	padding: 10px;
	cursor: pointer;
	flex: 1;
	text-align: center;
	background-color: #f0f5f9;
	border: 1px solid #ccc;
}

.tab.active {
	background-color: #e0e7ff;
	font-weight: bold;
}

.hidden {
	display: none;
}

@media (max-width: 899px) {
	.main {
		flex-direction: column;
	}

	.courses,
	.notifications,
	.Upcoming {
		margin: 0;
		padding: 0;
		flex: none;
		max-height: none;
	}
	.not-up {
		width: 800px;
		margin-left: 15px;
	}

	.tabs {
		display: flex; /* عرض التبويبات في الشاشات الصغيرة */
		justify-content: space-around;
		margin-bottom: 10px;
	}
}
</style>
