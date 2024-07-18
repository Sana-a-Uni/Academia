<template>
	<div class="container">
		<form @submit.prevent="createAssignment">
			<div class="content-time">
				<h3>Assignment 1</h3>
				<div class="clock-time">
					<i
						style="margin-top: 21px; color: #0584ae"
						class="mdi mdi-clock"
						@click="removeFile(index)"
					></i>
					<h4 class="file-name">Time Remaining 1:00:26</h4>
				</div>
			</div>

			<label for="assignmentTitle">Assignment content:</label>

			<div class="assignment-content">
				Write examples of liberties (negative rights) and claim-rights (positive rights)
				that are at opposition to each other?
			</div>
			<div class="assignment-file">
				<label for="assignmentDescription">Assignment File:</label>
				<label class="file-name" for="assignmentDescription">Assignment1.pdf</label>
			</div>
			<label for="assignmentDescription">Assignment Materials:</label>
			<QuillEditor
				v-model="assignmentDescription"
				:options="editorOptions"
				class="quill-editor"
			></QuillEditor>
			<label for="attachFiles">Attach Files:</label>
			<input
				class="uploadFiles"
				type="file"
				id="attachFiles"
				@change="handleFileUpload"
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
							<td>{{ file.name }}</td>
							<td style="text-align: center">
								<i class="mdi mdi-delete" @click="removeFile(index)"></i>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
			<label for="assignmentDescription">Comment:</label>
			<QuillEditor
				v-model="assignmentComment"
				:options="editorOptions"
				class="quill-editor-comment"
			></QuillEditor>
			<label for="assignmentDescription">Assessment Criteria:</label>
			<div class="assessment-list">
				<table style="width: 100%">
					<thead>
						<tr>
							<th>Assessment Criterion</th>
							<th>Grade</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(criterion, index) in criteria" :key="index">
							<td>{{ criterion.name }}</td>
							<td>{{ criterion.grade }}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div class="button-group">
				<button type="button" @click="saveDraft">Save As Draft</button>
				<button type="button" @click="cancelAssignment">Cancel</button>
				<button type="submit">Submit</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";

const props = defineProps([""]);
const emit = defineEmits(["assignment-created"]);

const assignmentTitle = ref("");
const assignmentDescription = ref("");
const assignmentComment = ref("");
const uploadedFiles = ref([]);
const criteria = ref([
	{ name: "Content Quality", grade: "10" },
	{ name: "Relevance", grade: "10" },
	{ name: "Completeness", grade: "10" },
	{ name: "Presentation", grade: "10" },
	{ name: "Grammar", grade: "10" },
]);

const editorOptions = {
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
};

const createAssignment = () => {
	console.log("Assignment Created:", {
		title: assignmentTitle.value,
		description: assignmentDescription.value,
		comment: assignmentComment.value,
		files: uploadedFiles.value,
		criteria: criteria.value,
	});
	emit("assignment-created");
};

const saveDraft = () => {
	console.log("Assignment Saved as Draft:", {
		title: assignmentTitle.value,
		description: assignmentDescription.value,
		comment: assignmentComment.value,
		files: uploadedFiles.value,
		criteria: criteria.value,
	});
};

const cancelAssignment = () => {
	assignmentTitle.value = "";
	assignmentDescription.value = "";
	assignmentComment.value = "";
	uploadedFiles.value = [];
};

const handleFileUpload = (event) => {
	const files = event.target.files;
	for (let i = 0; i < files.length; i++) {
		uploadedFiles.value.push(files[i]);
	}
};

const removeFile = (index) => {
	uploadedFiles.value.splice(index, 1);
};
</script>

<style>
body {
	font-family: Arial, sans-serif;
	background-color: ;
	margin: 0;
	padding: 0;
}

.container {
	width: 94%;
	padding: 2px 20px;
	margin-left: 10px;
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
	width: 20%;
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

.assignment-file {
	display: flex;
}

button {
	padding: 10px 20px;
	background-color: #c82333;
	color: #fff;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	width: 15%;
	font-size: 14px;
	margin-left: 10px;
	margin-bottom: 10px;
}

button[type="button"] {
	background-color: #f4f4f4;
	color: black;
	border: 1px solid #ccc;
}

button:hover {
	opacity: 0.9;
}

button[type="button"]:hover {
	background-color: #f4f4f4;
}

.quill-editor {
	height: 200px;
	margin-bottom: 20px;
}

.quill-editor-comment {
	height: 100px;
	margin-bottom: 20px;
}

.assessment-list {
	margin-bottom: 20px;
}

.assessment-list table {
	width: 50%;
	border-collapse: collapse;
}

.assessment-list th,
.assessment-list td {
	padding: 10px;
	border: 1px solid #ccc;
	height: 10px;
}

.assessment-list th {
	background-color: #f4f4f4;
}

.assessment-list {
	margin-bottom: 20px;
}

.assessment-list table {
	width: 100%;
	border-collapse: collapse;
}

.assessment-list th,
.assessment-list td {
	padding: 10px;
	border: 1px solid #ccc;
}

.assessment-list th {
	background-color: #f4f4f4;
}

.file-list {
	margin-bottom: 20px;
}

.file-list table {
	width: 50%;
	border-collapse: collapse;
}

.file-list th,
.file-list td {
	padding: 10px;
	border: 1px solid #ccc;
	height: 10px;
}

.file-list th {
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
	background-color: #dc3545;
}

@media (max-width: 600px) {
	.container {
		padding: 10px;
	}

	button {
		padding: 8px;
		font-size: 12px;
		width: 25%;
	}
}
</style>
