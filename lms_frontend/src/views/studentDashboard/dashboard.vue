<template>
	<div class="layout">
		<navbar />
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
		<div class="courses-section">
			<Courses :courses="courses" :activeTab="activeTab" :isSmallScreen="isSmallScreen"/>
		</div>	
			<div class="notification-upcoming-section">
			<Notifications class="notification-section" :activeTab="activeTab" :isSmallScreen="isSmallScreen" :notifications="notifications"/>
			<UpcomingTask :activeTab="activeTab" :isSmallScreen="isSmallScreen" />
			  
			</div>
		
	</div>
	</div>
</template>

<script>
import navbar from "@/components/Navbar.vue";
import Courses from "@/components/Courses.vue";
import Notifications from "@/components/Notifications.vue";
import UpcomingTask from "@/components/UpcomingTask.vue";

export default {
	components: {
		navbar,
		Courses,
		Notifications,
	    UpcomingTask,
	},
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
/* Your styles for the layout */
.layout {
	display: flex;
	flex-direction: column;
	height: 100%;
	background-color: #f0f5f9;
}
.main {
	display: flex;
	flex-direction: column;
	background-color: #f4f4f4;
    margin-top:10px;
	height:100%;
}
.courses-section{
	flex:6;
}
.notification-upcoming-section{
	flex:3;
	display:flex;
	flex-direction:column;
	gap:10px;
}
.not-up{
	display:flex;
	flex-direction:column;
	
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
	background-color: #f4f4f4;
	border: 1px solid #ccc;
	margin-top:55px;
	
}

.tab.active {
	background-color: #0584ae;
	font-weight: bold;
	color:white;
}

.hidden {
	display: none;
}

@media (max-width: 899px) {
	.main {
		flex-direction: column;
		height:800px;
	}
    .courses-section{
		height:500px;
	}
	.notification-section{
	
	}

	.courses,
	.notifications,
	.{
		margin: 0;
		padding: 0;
		flex: none;
		max-height: none;
	}
	.courses{
		padding-top:15px;
		margin:10px;
		margin-bottom:40px;
		height:680px;
	}

	.not-up {
		width: 800px;
		margin-left: 15px;
	}
	
	.notifications{
		padding:5px;
		margin-left:8px;
		margin-right:10px;

		
	}
	.Upcoming-content{
		
		padding:20px;
	}
	.Upcoming{
		padding-top:1px;
		margin-bottom:398px;
	}
	.tabs {
		display: flex; /* عرض التبويبات في الشاشات الصغيرة */
		justify-content: space-around;
		margin-bottom: 10px;
	}
}
</style>
