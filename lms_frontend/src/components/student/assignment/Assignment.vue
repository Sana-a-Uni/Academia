<template>
	<div class="container" v-if="assignmentDetails">
		<form @submit.prevent="handleSubmit(true)">
			<div class="content-time">
				<h3>{{ assignmentDetails.assignment_title }}</h3>
				<div class="clock-time" v-if="showCountdown">
					<i style="margin-top: 21px; color: #0584ae" class="mdi mdi-clock"></i>
					<h4 class="file-name">Time Remaining {{ countdownTime }}</h4>
				</div>
			</div>
			<h4>Assignment Instructions</h4>
			<div class="indented-content">
				<p>
					End time: All attempts must be completed before
					{{ formattedEndTime }}
				</p>
				<!-- Note -->
				<span v-html="assignmentDetails.instruction"></span>
			</div>

			<h4>Assignment Content</h4>
			<div class="indented-content">
				<div class="assignment-content" v-html="assignmentDetails.question"></div>
			</div>

			<h4>Assignment File</h4>
			<div class="indented-content">
				<div class="assignment-file">
					<label
						v-for="file in assignmentDetails.attached_files"
						:key="file.file_url"
						class="file-name"
					>
						<a :href="getFullFileUrl(file.file_url)" target="_blank">{{
							file.file_name
						}}</a>
					</label>
				</div>
			</div>

			<h4>Assignment Materials</h4>
			<div class="indented-content">
				<div ref="quillEditor" class="quill-editor"></div>
			</div>

			<h4>Attach Files</h4>
			<div class="indented-content">
				<input
					class="uploadFiles"
					type="file"
					id="attachFiles"
					@change="handleFileUpload"
					multiple
				/>
				<div
					v-if="previousSubmissionFiles.length || uploadedFiles.length"
					class="file-list"
				>
					<table>
						<thead>
							<tr>
								<th style="width: 80%">File Name</th>
								<th>Delete</th>
							</tr>
						</thead>
						<tbody>
							<!-- عرض الملفات السابقة -->
							<tr
								v-for="(file, index) in previousSubmissionFiles"
								:key="file.file_url"
							>
								<td>
									<a :href="getFullFileUrl(file.file_url)" target="_blank">{{
										file.file_name
									}}</a>
								</td>
								<td style="text-align: center">
									<font-awesome-icon
										icon="trash"
										@click="markFileForDeletion(index)"
										style="color: #dc3545"
									/>
								</td>
							</tr>
							<!-- عرض الملفات الجديدة -->
							<tr v-for="(file, index) in uploadedFiles" :key="index">
								<td>
									<a :href="file.previewUrl" target="_blank">{{ file.name }}</a>
								</td>
								<td style="text-align: center">
									<font-awesome-icon
										icon="trash"
										@click="removeFile(index)"
										style="color: #dc3545"
									/>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<h4>Comment</h4>
			<div class="indented-content">
				<div ref="commentEditor" class="quill-editor-comment"></div>
			</div>

			<h4>Assessment Criteria</h4>
			<div class="indented-content">
				<div class="assessment-list">
					<table style="width: 100%">
						<thead>
							<tr>
								<th>Assessment Criterion</th>
								<th>Grade</th>
							</tr>
						</thead>
						<tbody>
							<tr
								v-for="(criterion, index) in assignmentDetails.assessment_criteria"
								:key="index"
							>
								<td>{{ criterion.assessment_criteria }}</td>
								<td>{{ criterion.maximum_grade }}</td>
							</tr>
							<tr>
								<td><strong>Total Grades</strong></td>
								<td>
									<strong>{{ assignmentDetails.total_grades }}</strong>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<div class="button-group">
				<button type="button" @click="cancelAssignment">Cancel</button>
				<button type="button" @click="handleSubmit(false)">Save As Draft</button>
				<button type="submit">Submit</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed, defineProps, watch } from "vue";
import { useAssignmentStore } from "@/stores/studentStore/assignmentStore";
import Quill from "quill";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faTrash } from "@fortawesome/free-solid-svg-icons";

library.add(faTrash);

const props = defineProps({
	assignmentDetails: {
		type: Object,
		required: true,
		default: () => ({}),
	},
	previousSubmission: {
		type: Object,
		default: null,
	},
	previousSubmissionFiles: {
		type: Array,
		default: () => [],
	},
	onSubmit: {
		type: Function,
		required: true,
	},
});

const assignmentStore = useAssignmentStore();

const quillEditor = ref(null);
const commentEditor = ref(null);
const uploadedFiles = ref([]);
const timeRemaining = ref(null);
const previousSubmissionFiles = ref([...props.previousSubmissionFiles]);
const filesMarkedForDeletion = ref([]);

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

const initializeQuillEditors = () => {
	if (quillEditor.value && commentEditor.value) {
		const assignmentEditor = new Quill(quillEditor.value, editorOptions);
		assignmentEditor.root.innerHTML = props.previousSubmission
			? props.previousSubmission.answer
			: "";
		assignmentEditor.on("text-change", () => {
			props.assignmentDetails.answer = assignmentEditor.root.innerHTML;
		});

		const commentEditorInstance = new Quill(commentEditor.value, editorOptions);
		commentEditorInstance.root.innerHTML = props.previousSubmission
			? props.previousSubmission.comment
			: "";
		commentEditorInstance.on("text-change", () => {
			props.assignmentDetails.comment = commentEditorInstance.root.innerHTML;
		});
	} else {
		console.error("Quill containers are not available");
	}
};

onMounted(() => {
	nextTick(initializeQuillEditors);
	updateTimeRemaining();
	const interval = setInterval(updateTimeRemaining, 1000);
	onUnmounted(() => clearInterval(interval));
});

watch(
	() => props.assignmentDetails,
	() => {
		nextTick(initializeQuillEditors);
	}
);

const handleSubmit = async (isFinalSubmission) => {
	const data = {
		student: "EDU-STU-2024-00003",
		assignment: "ecff4b55c2",
		answer: quillEditor.value.querySelector(".ql-editor").innerHTML,
		comment: commentEditor.value.querySelector(".ql-editor").innerHTML,
		submit: isFinalSubmission,
		attachments: [],
	};

	// Handle file upload only if there are files to upload
	if (uploadedFiles.value.length > 0) {
		for (let file of uploadedFiles.value) {
			const reader = new FileReader();
			reader.onloadend = () => {
				data.attachments.push({
					attachment: reader.result.split(",")[1], // Set the attachment as base64 string
					attachment_name: file.name,
				});
				if (data.attachments.length === uploadedFiles.value.length) {
					props.onSubmit(data);
					// Clear the uploaded files to prevent duplicate uploads
					uploadedFiles.value = [];
				}
			};
			reader.readAsDataURL(file.file); // تعديل هنا لقراءة الملف الصحيح
		}
	} else {
		// Submit without file if no file is uploaded
		await props.onSubmit(data);
	}

	// Handle deletion of marked files
	for (let file of filesMarkedForDeletion.value) {
		try {
			const response = await assignmentStore.deleteAttachment(file.file_url);
			if (response.status === "success") {
				previousSubmissionFiles.value = previousSubmissionFiles.value.filter(
					(f) => f.file_url !== file.file_url
				);
			}
		} catch (error) {
			console.error("Error deleting file:", error);
		}
	}
};

const handleFileUpload = (event) => {
	const files = event.target.files;
	for (let i = 0; i < files.length; i++) {
		if (
			!uploadedFiles.value.some(
				(f) => f.file.name === files[i].name && f.file.size === files[i].size
			)
		) {
			const previewUrl = URL.createObjectURL(files[i]); // Create a preview URL
			uploadedFiles.value.push({ file: files[i], previewUrl, name: files[i].name });
		}
	}
};

const cancelAssignment = () => {
	if (quillEditor.value && commentEditor.value) {
		quillEditor.value.querySelector(".ql-editor").innerHTML = "";
		commentEditor.value.querySelector(".ql-editor").innerHTML = "";
	}
	uploadedFiles.value = [];
};

const removeFile = (index) => {
	const file = uploadedFiles.value[index];
	URL.revokeObjectURL(file.previewUrl); // Revoke the object URL to release memory
	uploadedFiles.value.splice(index, 1);
};

const markFileForDeletion = (index) => {
	const file = previousSubmissionFiles.value[index];
	previousSubmissionFiles.value.splice(index, 1);
	filesMarkedForDeletion.value.push(file);
};

const getFullFileUrl = (fileUrl) => {
	return `http://localhost:80${fileUrl}`;
};

const showCountdown = computed(() => {
	return timeRemaining.value && timeRemaining.value.hours < 2;
});

const countdownTime = computed(() => {
	if (!timeRemaining.value) {
		return "";
	}
	const { hours, minutes, seconds } = timeRemaining.value;
	return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds
		.toString()
		.padStart(2, "0")}`;
});

const formattedEndTime = computed(() => {
	if (props.assignmentDetails && props.assignmentDetails.to_date) {
		const toDate = new Date(props.assignmentDetails.to_date);
		return toDate.toISOString().slice(0, 19).replace("T", " ");
	}
	return "";
});

const updateTimeRemaining = () => {
	if (props.assignmentDetails && props.assignmentDetails.to_date) {
		const toDate = new Date(props.assignmentDetails.to_date);
		const now = new Date();
		const diff = toDate - now;

		if (diff > 0) {
			const hours = Math.floor(diff / 1000 / 60 / 60);
			const minutes = Math.floor((diff / 1000 / 60) % 60);
			const seconds = Math.floor((diff / 1000) % 60);

			timeRemaining.value = { hours, minutes, seconds };
		} else {
			timeRemaining.value = null;
		}
	}
};
</script>

<style scoped>
body {
	font-family: Arial, sans-serif;
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
	align-items: center;
}

.clock-time {
	display: flex;
	align-items: center;
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

h4 {
	margin-bottom: 10px;
	margin-top: 20px;
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
	background-color: #dc3545;
	color: #fff;
	border: none;
	border-radius: 3px;
	cursor: pointer;
}

.file-list td button:hover {
	background-color: #dc3545;
}

.indented-content {
	padding-left: 20px;
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
