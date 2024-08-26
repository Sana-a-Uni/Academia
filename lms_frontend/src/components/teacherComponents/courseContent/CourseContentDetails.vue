<template>
	<div class="course-content-detail">
		<h1>{{ courseContent.title }}</h1>

		<h2>Topics</h2>
		<div v-html="courseContent.topic" class="content-body"></div>

		<h2>Files</h2>
		<ul>
			<li v-for="(file, index) in courseContent.attachment_files" :key="index">
				<a :href="getFullFileUrl(file.file_url)" target="_blank">{{ file.file_name }}</a>
			</li>
		</ul>
	</div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
	courseContent: {
		type: Object,
		required: true,
	},
});
const getFullFileUrl = (fileUrl) => {
	return `http://localhost:80${fileUrl}`;
};
</script>

<style scoped>
.course-content-detail {
	padding: 20px;
	width: 96%;
	/* max-width: 800px; */
	margin: 0 auto;
	background-color: #ffffff;
	border-radius: 8px;
	box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
	font-size: 32px;
	color: #2c3e50;
	margin-bottom: 15px;
	text-align: center;
}

h2 {
	font-size: 24px;
	color: #34495e;
	margin-top: 20px;
	margin-bottom: 10px;
	border-bottom: 2px solid #ecf0f1;
	padding-bottom: 5px;
}

.content-body {
	margin-top: 10px;
	color: #555;
	text-align: left;
}

ul {
	list-style-type: disc;
	padding-left: 20px;
	margin-left: 0;
}

li {
	margin-bottom: 10px;
}

a {
	color: #3498db;
	text-decoration: none;
}

a:hover {
	text-decoration: underline;
}
</style>
