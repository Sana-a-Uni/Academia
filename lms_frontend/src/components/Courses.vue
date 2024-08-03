<template>
    <div class="courses" :class="{ hidden: activeTab !== 'courses' && isSmallScreen }">
			<h3 v-show="!isSmallScreen" style="padding-left: 10px; padding-top: 15px">Courses</h3>
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
</template>

<script>
export default {
	props:{
        activeTab:String,
        isSmallScreen: Boolean,
        courses:Array,
    },
	methods: {
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
	background-color: #f4f4f4;
}

.courses {
	flex: 2;
	overflow: hidden;
	margin-left: 20px;
	margin-right: 20px;
	margin-bottom:15px;
	border-radius: 10px;
	padding-left: 20px;
	padding-right: 20px;
	margin-top: 70px;
	background-color: white;
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
	max-height: 290px; /* يمكنك تعديل هذا الارتفاع حسب الحاجة */
	overflow-y: auto;
	padding: 20px;
	margin-top:20px;
	border-radius: 10px;
}

.card {
	background-color: #f4f4f4;
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
	background-color: #f4f4f4;
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
	height: 280px;
	margin-top: 30px;
	border-radius: 10px;
	margin-right: 20px;
}
.Upcoming-content {
	background-color: #f4f4f4;
	height: 160px;
	margin-top: 40px;
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
		margin-top:0px;
		margin-right:10px;
		height:1000px;
		margin-bottom:295px;
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