<template>
  <div class="Upcoming" :class="{ hidden: activeTab !== 'upcoming' && isSmallScreen }">
				<h3 v-show="!isSmallScreen" style="padding-left: 35px; padding-top: 25px; padding-bottom:15px;">Upcoming Task</h3>
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
</template>


<script>
export default {
	props:{
        activeTab:String,
        isSmallScreen: Boolean,
    },
};
</script>

<style scoped>

.Upcoming {
	background-color: white;
	height: 275px;
	margin-top: 10px;
	border-radius: 10px;
	margin-right: 20px;
}
.Upcoming-content {
	background-color: #f4f4f4;
	height: 160px;
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
