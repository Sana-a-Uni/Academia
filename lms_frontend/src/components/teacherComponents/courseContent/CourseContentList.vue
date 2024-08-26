<template>
	<div class="course-content-list">
		<div class="header">
			<h2>All Courses Content</h2>
			<div class="actions">
				<button class="create-course-content-btn" @click="goToCreateCourseContent">
					Create Course Content
				</button>
			</div>
		</div>

		<div class="content">
			<div
				class="card"
				v-for="(course, index) in courseContents"
				:key="index"
				@click="navigateToCourseDetail(course.name)"
			>
				<h3>{{ course.title }}</h3>
			</div>
		</div>
	</div>
</template>
<script setup>
import { useRouter } from "vue-router";

const props = defineProps({
	courseContents: Array,
});

const router = useRouter();

const navigateToCourseDetail = (courseName) => {
	router.push({ name: "courseContentDetail", params: { courseName } });
};

const goToCreateCourseContent = () => {
	router.push({ name: "createCourseContents" });
};
</script>

<style scoped>
.course-content-list {
	width: 100%;
	margin: 0 auto;
	border-collapse: collapse;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 40px;
	margin-top: 20px;
	padding: 0 20px;
	position: relative;
}

.create-course-content-btn {
	background-color: #4caf50;
	color: white;
	border: none;
	border-radius: 5px;
	padding: 10px 20px;
	cursor: pointer;
	font-size: 16px;
}

.create-course-content-btn:hover {
	background-color: #45a049;
}

.actions {
	display: flex;
	justify-content: end;
	align-items: center;
	width: 100%;
}

.create-content-btn {
	background-color: #4caf50;
	color: white;
	border: none;
	border-radius: 5px;
	padding: 10px 20px;
	cursor: pointer;
	font-size: 16px;
	display: flex;
	justify-content: end;
}

.create-content-btn:hover {
	background-color: #45a049;
}

.card {
	background-color: #f4f4f4;
	margin: 15px;
	padding: 15px;
	border-radius: 10px;
	width: 87%;
	height: 95%;
	cursor: pointer;
	text-align: center;
}

h2 {
	margin: 0;
	font-size: 24px;
	position: absolute;
	left: 45%;
	transform: translateX(-50%);
}

@media (max-width: 768px) {
	h2 {
		font-size: 18px;
		position: static;
		transform: none;
		order: 1;
	}

	.actions {
		flex-direction: column;
		align-items: flex-start;
	}

	.filters {
		order: 2;
		flex: 1;
		display: flex;
		justify-content: flex-end;
		margin-top: 10px;
	}

	.filters select {
		font-size: 14px;
	}
}
</style>
