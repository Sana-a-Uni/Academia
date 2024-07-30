<template>
	<div class="container" v-if="assignmentDetails">
		<div v-if="alert.message" :class="`alert ${alert.type}`">
			{{ alert.message }}
		</div>
		<div v-if="isSubmitted && !alert.message" class="alert alert-success">
			The assignment has been submitted. You cannot edit or resubmit it.
		</div>
		<div v-else-if="!isTimeRemaining && !alert.message" class="alert alert-danger">
			The submission period has ended. You can no longer edit your answers.
		</div>

		<form @submit.prevent="handleSubmit(true)">
			<div class="content-time">
				<h3>
					{{ assignmentDetails.assignment_title }} ({{
						assignmentDetails.assignment_type
					}})
				</h3>
				<div v-if="!isSubmitted">
					<div class="clock-time" v-if="showCountdown">
						<i style="margin-top: 21px; color: #0584ae" class="mdi mdi-clock"></i>
						<h4 class="file-name">Time Remaining {{ countdownTime }}</h4>
					</div>
				</div>
			</div>
			<h4>Assignment Instructions</h4>
			<div class="indented-content">
				<p>End time: All attempts must be completed before {{ formattedEndTime }}</p>
				<span v-html="assignmentDetails.instruction"></span>
			</div>

			<div v-if="assignmentDetails.question">
				<h4>Assignment Content</h4>
				<div class="indented-content">
					<div class="assignment-content" v-html="assignmentDetails.question"></div>
				</div>
			</div>

			<div
				v-if="
					assignmentDetails.attached_files && assignmentDetails.attached_files.length > 0
				"
			>
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
					:disabled="!isTimeRemaining || isSubmitted"
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
										@click="markFileForDeletion(index, file.file_url)"
										style="color: #dc3545"
										v-if="isTimeRemaining && !isSubmitted"
									/>
								</td>
							</tr>
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
				<template v-if="isTimeRemaining && !isSubmitted">
					<button type="button" @click="handleSubmit(false)">Save As Draft</button>
					<button type="submit">Submit</button>
				</template>
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
import { useRoute, useRouter } from "vue-router";

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
const router = useRouter();
const route = useRoute();

const quillEditor = ref(null);
const commentEditor = ref(null);
const uploadedFiles = ref([]);
const timeRemaining = ref(null);
const previousSubmissionFiles = ref([...props.previousSubmissionFiles]);
const filesMarkedForDeletion = ref([]);
const isSubmitted = computed(() => assignmentStore.isSubmitted);
const isTimeRemaining = computed(() => timeRemaining.value !== null);
const alert = ref({ message: "", type: "" });

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
	readOnly: !isTimeRemaining.value || isSubmitted.value,
};

const initializeQuillEditors = () => {
	if (quillEditor.value && commentEditor.value) {
		const assignmentEditor = new Quill(quillEditor.value, editorOptions);
		const commentEditorInstance = new Quill(commentEditor.value, editorOptions);

		if (props.previousSubmission) {
			assignmentEditor.root.innerHTML = props.previousSubmission.answer || "";
			commentEditorInstance.root.innerHTML = props.previousSubmission.comment || "";
		}

		assignmentEditor.enable(isTimeRemaining.value && !isSubmitted.value);
		assignmentEditor.on("text-change", () => {
			props.assignmentDetails.answer = assignmentEditor.root.innerHTML;
		});

		commentEditorInstance.enable(isTimeRemaining.value && !isSubmitted.value);
		commentEditorInstance.on("text-change", () => {
			props.assignmentDetails.comment = commentEditorInstance.root.innerHTML;
		});
	} else {
		console.error("Quill containers are not available");
	}
};

onMounted(() => {
	console.log("Assignment Details in Component: ", props.assignmentDetails); // عرض البيانات في وحدة التحكم
	nextTick(initializeQuillEditors);
	updateTimeRemaining();
	const interval = setInterval(updateTimeRemaining, 1000);
	onUnmounted(() => clearInterval(interval));
});

watch(
	() => props.assignmentDetails,
	(newVal) => {
		console.log("Updated Assignment Details:", newVal);
		if (newVal) {
			nextTick(initializeQuillEditors);
		} else {
			alert.value = { message: "Assignment details are missing", type: "alert-danger" };
		}
	}
);

const showAlert = (message) => {
	return confirm(message);
};

const handleSubmit = async (isFinalSubmission) => {
	const confirmMessage = isFinalSubmission
		? "Are you sure you want to submit the assignment?"
		: "Are you sure you want to save the draft?";
	if (!showAlert(confirmMessage)) {
		return;
	}

	const data = {
		assignment: route.params.assignmentName,
		answer: quillEditor.value.querySelector(".ql-editor").innerHTML,
		comment: commentEditor.value.querySelector(".ql-editor").innerHTML,
		submit: isFinalSubmission,
		attachments: [],
	};

	if (uploadedFiles.value.length > 0) {
		for (let file of uploadedFiles.value) {
			const reader = new FileReader();
			reader.onloadend = async () => {
				data.attachments.push({
					attachment: reader.result.split(",")[1],
					attachment_name: file.name,
				});
				if (data.attachments.length === uploadedFiles.value.length) {
					await submitData(data, isFinalSubmission);
				}
			};
			reader.readAsDataURL(file.file);
		}
	} else {
		await submitData(data, isFinalSubmission);
	}
};

const submitData = async (data, isFinalSubmission) => {
	try {
		const response = await props.onSubmit(data);
		if (response && response.hasOwnProperty("is_submitted")) {
			isSubmitted.value = response.is_submitted;
		} else {
			alert.value = { message: "Unexpected response format", type: "alert-danger" };
			return;
		}
		uploadedFiles.value = [];
		await assignmentStore.fetchPreviousSubmission(route.params.assignmentName);

		if (isFinalSubmission) {
			alert.value = { message: "Assignment submitted successfully!", type: "alert-success" };
		} else {
			alert.value = { message: "Draft saved successfully!", type: "alert-success" };
		}

		router.push({ path: "/studentDashboard/assignmentView" });
	} catch (error) {
		console.error("Error submitting data:", error);
		alert.value = { message: "Error submitting data: " + error.message, type: "alert-danger" };
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
			const previewUrl = URL.createObjectURL(files[i]);
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
	router.push({ path: "/studentDashboard/assignmentView" });
};

const removeFile = (index) => {
	const file = uploadedFiles.value[index];
	URL.revokeObjectURL(file.previewUrl);
	uploadedFiles.value.splice(index, 1);
};

const markFileForDeletion = async (index, fileUrl) => {
	try {
		await assignmentStore.deleteAttachment(fileUrl);
		previousSubmissionFiles.value.splice(index, 1);
		console.log("File marked for deletion successfully");
	} catch (error) {
		console.error("Error deleting file:", error);
		alert("Error deleting file: " + error.message);
	}
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
	return formatTimeRemaining(hours, minutes, seconds);
});

const formatTimeRemaining = (hours, minutes, seconds) => {
	return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds
		.toString()
		.padStart(2, "0")}`;
};

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

.alert {
	width: 100%;
	padding: 10px;
	margin-bottom: 20px;
	border: 1px solid transparent;
	border-radius: 4px;
}

.alert-danger {
	color: #a94442;
	background-color: #f2dede;
	border-color: #ebccd1;
}

.alert-success {
	color: #3c763d;
	background-color: #dff0d8;
	border-color: #d6e9c6;
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
