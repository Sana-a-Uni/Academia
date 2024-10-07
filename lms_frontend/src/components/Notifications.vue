<template>
  <div
  class="notifications"
	:class="{ hidden: activeTab !== 'notifications' && isSmallScreen }"
			>
				<h3 v-show="!isSmallScreen" style="padding-left: 20px; padding-top: 30px;">Notifications</h3>
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
</template>

<script>
export default {
    props:{
        activeTab:String,
        isSmallScreen: Boolean,
        notifications:Array,
    },
};
</script>


<style scoped>


.courses,
.notifications {
	padding-left: 20px;
	padding-right: 20px;
	margin-top: 70px;
	background-color: white;
}

.notifications {
	height: 402px;
	margin-right: 20px;
	border-radius: 10px;
	height: 420px;
}

.scrollable-card-notification {
	max-height: 290px; /* يمكنك تعديل هذا الارتفاع حسب الحاجة */
	overflow-y: auto;
	padding: 20px;
	margin-top:20px;
	border-radius: 10px;
}



.notification {
	display: flex;
	align-items: center;
	margin-bottom: 9px;
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
	}
	.courses{
		padding-top:15px;
		margin:10px;
		margin-bottom:40px;
		height:680px;
	}
    .scrollable-card-notification{
		max-height: 600px; /* يمكنك تعديل هذا الارتفاع حسب الحاجة */
	overflow-y: auto;
	padding: 20px;
	margin-top:20px;		
	border-radius: 10px;
	}
	.not-up {
		width: 800px;
		margin-left: 15px;
	}
	
	.notifications{
		padding:5px;
		margin-top:10px;
		margin-right:10px;
	    margin-bottom:10px;
		padding-bottom:40px;
		height:660px;
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
