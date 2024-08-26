<template>
	<div class="container">
		<h3>Add Course Content</h3>
		<form @submit.prevent="createCourseContent">
			<label for="lessonTitle">Lesson Title:</label>
			<input class="name-input" v-model="title" id="lessonTitle" />

			<label for="lessonTopics">Lesson Topics:</label>
			<div class="topics">
				<div ref="topicEditor" class="quill-editor"></div>
			</div>

			<label for="attachFiles">Lesson Content:</label>
			<div class="lesson-content">
				<input
					class="uploadFiles"
					type="file"
					id="attachFiles"
					@change="handleFileUpload"
					:disabled="!isTimeRemaining || isSubmitted"
					multiple
				/>
				<div v-if="uploadedFiles.length" class="file-list">
					<table>
						<thead>
							<tr>
								<th style="width: 80%">File Name</th>
								<th>Delete</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="(file, index) in uploadedFiles" :key="index">
								<td>
									<a :href="file.previewUrl" target="_blank">{{ file.name }}</a>
								</td>
								<td style="text-align: center">
									<font-awesome-icon
										icon="trash"
										@click="removeFile(index)"
										style="color: #dc3545"
										v-if="isTimeRemaining && !isSubmitted"
									/>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<div class="button-group">
				<button style="margin-right: 30px" type="button" @click="cancelCourseContent">
					Cancel
				</button>
				<button type="submit">Create</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, onMounted, nextTick, defineEmits, computed } from "vue";
import Quill from "quill";
import { useCourseContentStore } from "@/stores/teacherStore/courseContentStore";
import { useCourseStore } from "@/stores/teacherStore/courseStore";
import { useRouter } from "vue-router";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faTrash } from "@fortawesome/free-solid-svg-icons";

library.add(faTrash);

const router = useRouter();
const emit = defineEmits(["course-content-created"]);
const title = ref("");
const topic = ref("");
const uploadedFiles = ref([]);
const isTimeRemaining = ref(true);
const isSubmitted = ref(false);

const store = useCourseContentStore();
const courseStore = useCourseStore();
const selectedCourse = computed(() => courseStore.selectedCourse);
const topicEditor = ref(null);

const initializeQuillEditors = () => {
	if (topicEditor.value) {
		const topicQuill = new Quill(topicEditor.value, {
			theme: "snow",
			modules: {
				toolbar: [
					[{ header: [1, 2, false] }],
					["bold", "italic", "underline"],
					[{ list: "ordered" }, { list: "bullet" }],
					[{ align: [] }],
					["clean"],
				],
			},
		});

		topicQuill.on("text-change", () => {
			topic.value = topicQuill.root.innerHTML;
		});
	} else {
		console.error("Quill container is not available");
	}
};

const createCourseContent = async () => {
	if (!selectedCourse.value) {
		console.error("No selected course found.");
		return;
	}

	const contentData = {
		title: title.value,
		topic: topic.value,
		course: selectedCourse.value.course,
		course_type: selectedCourse.value.course_type,
		attachments: uploadedFiles.value,
	};

	try {
		await store.addCourseContent(contentData);
		emit("course-content-created");
		resetForm();
		router.push({ path: "/teacherDashboard/courseView/courseContent" });
	} catch (error) {
		console.error("Error creating course content:", error);
	}
};

const handleFileUpload = (event) => {
	const files = event.target.files;
	if (!files.length) return;

	for (let i = 0; i < files.length; i++) {
		const file = files[i];

		if (
			!uploadedFiles.value.some(
				(f) => f.file.name === file.name && f.file.size === file.size
			)
		) {
			const previewUrl = URL.createObjectURL(file);
			uploadedFiles.value.push({ file, previewUrl, name: file.name });
		}
	}
};

const removeFile = (index) => {
	URL.revokeObjectURL(uploadedFiles.value[index].previewUrl);
	uploadedFiles.value.splice(index, 1);
};

const cancelCourseContent = () => {
	resetForm();
	router.go(-1);
};

const resetForm = () => {
	title.value = "";
	topic.value = "";
	uploadedFiles.value = [];
};

onMounted(() => {
	nextTick(initializeQuillEditors);
});
</script>

<style scoped>
body {
	font-family: Arial, sans-serif;
	margin: 0;
	padding: 0;
	width: 100%;
}

.name-input {
	height: 45px;
	width: 100%;
}
.file-list td {
	text-align: center;
}
.topics {
	width: 100%;
}

h3 {
	font-size: 24px;
	text-align: center;
}

.lesson-content {
	width: 100%;
	margin-bottom: 30px;
}

.container {
	width: 94%;
	padding: 20px;
	box-shadow: 0 0 rgba(0, 0, 0, 0.1);
	box-sizing: border-box;
}

.container table {
	border-collapse: collapse;
	border-radius: 10px;
	overflow: hidden;
}

.assignment-content {
	width: 100%;
	padding: 10px;
	margin-bottom: 10px;
	height: 100px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
	background-color: #f4f4f4;
}

.content-time {
	display: flex;
	justify-content: space-between;
}

.clock-time {
	display: flex;
}

.file-name {
	margin-left: 10px;
	color: #0584ae;
}

h1 {
	text-align: center;
	margin-bottom: 20px;
	font-size: 24px;
}

label {
	display: block;
	margin: 10px 0 7px;
}

.uploadFiles {
	width: 100%;
}

input,
select,
textarea {
	width: 100%;
	padding: 10px;
	margin-bottom: 20px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
}

.mdi-delete {
	color: red;
	font-size: 20px;
	cursor: pointer;
}

.button-group {
	display: flex;
	justify-content: flex-end;
}

button {
	padding: 10px 20px;
	background-color: #0584ae;
	color: #fff;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	width: 15%;
	font-size: 14px;
}

button[type="button"] {
	background-color: #c82333;
	color: #fff;
}

button:hover {
	opacity: 0.9;
}

.quill-editor {
	margin-bottom: 20px;
}

.quill-editor-comment {
	height: 100px;
	margin-bottom: 20px;
}

.assesstent-list {
	margin-bottom: 20px;
}

.assesstent-list table {
	width: 100%;
	border-collapse: collapse;
}

.assesstent-list th,
.assesstent-list td {
	padding: 10px;
	border: 1px solid #ccc;
}

.assesstent-list th {
	background-color: #f4f4f4;
}

.file-list {
	margin-bottom: 20px;
}

.file-list table {
	width: 100%;
	border-collapse: collapse;
}

.file-list th,
.file-list td {
	padding: 10px;
	border: 1px solid #ccc;
}

.file-list th {
	background-color: #f4f4f4;
}

.file-list td button {
	padding: 5px 10px;
	background-color: #c82333;
	color: #fff;
	border: none;
	border-radius: 3px;
	cursor: pointer;
}

.file-list td button:hover {
	opacity: 0.8;
}

.file-list td a {
	color: #0584ae;
	text-decoration: none;
}

.file-list td a:hover {
	text-decoration: underline;
}
</style>
