<template>
	<div class="assignment-details">
		<h2 class="center-title">Assignment Details</h2>
		<form @submit.prevent="saveAssignmentDetails">
			<!-- Question Field -->
			<div class="form-group">
				<label for="question">Question</label>
				<div ref="quillQuestionEditor" class="quill-editor"></div>
			</div>

			<!-- Attach Files Field -->
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

			<!-- Assessment Criteria Fields -->
			<div class="form-group">
				<label for="assessment-criteria">Assessment Criteria</label>
				<div class="criteria-container">
					<table class="criteria-table">
						<thead>
							<tr>
								<th>Assessment Criteria</th>
								<th>Maximum Grade</th>
								<th></th>
							</tr>
						</thead>
						<tbody>
							<tr
								v-for="(criteria, index) in assignmentStore.assignmentData
									.assessment_criteria"
								:key="index"
							>
								<td class="criteria-column">
									<input type="text" v-model="criteria.assessment_criteria" />
								</td>
								<td class="grade-column">
									<input
										type="number"
										v-model="criteria.maximum_grade"
										@input="validateGrade(index)"
									/>
								</td>
								<td class="trash-column">
									<button
										type="button"
										@click="removeCriteria(index)"
										class="remove-button"
									>
										<font-awesome-icon
											:icon="['fas', 'trash']"
											class="trash-icon"
										/>
									</button>
								</td>
							</tr>
						</tbody>
					</table>
					<button type="button" @click="addCriteria" class="add-button">
						Add New Criteria
					</button>
				</div>
			</div>

			<!-- Form Actions -->
			<div class="form-actions">
				<button class="prev-btn" @click="previousPage">Previous</button>
				<button class="next-btn" type="submit">Next</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import Quill from "quill";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faTrash } from "@fortawesome/free-solid-svg-icons";

library.add(faTrash);

const emit = defineEmits(["settings", "go-back"]);
const assignmentStore = useAssignmentStore();
const quillQuestionEditor = ref(null);
const uploadedFiles = ref([]);
const previousSubmissionFiles = ref([]);
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

onMounted(() => {
	nextTick(() => {
		const editor = new Quill(quillQuestionEditor.value, editorOptions);
		editor.root.innerHTML = assignmentStore.assignmentData.question; // Load existing data
		editor.on("text-change", () => {
			assignmentStore.assignmentData.question = editor.root.innerHTML;
		});

		// Ensure at least one criteria is present
		if (assignmentStore.assignmentData.assessment_criteria.length === 0) {
			addCriteria();
		}
	});
});

const addCriteria = () => {
	assignmentStore.assignmentData.assessment_criteria.push({
		assessment_criteria: "",
		maximum_grade: 0,
	});
};

const removeCriteria = (index) => {
	assignmentStore.assignmentData.assessment_criteria.splice(index, 1);
};

const validateGrade = (index) => {
	if (assignmentStore.assignmentData.assessment_criteria[index].maximum_grade < 0) {
		assignmentStore.assignmentData.assessment_criteria[index].maximum_grade = 0;
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
			const reader = new FileReader();
			reader.onload = (e) => {
				uploadedFiles.value.push({
					file: files[i],
					previewUrl,
					name: files[i].name,
					content: e.target.result.split(",")[1],
				});
			};
			reader.readAsDataURL(files[i]);
		}
	}
};

const removeFile = (index) => {
	const file = uploadedFiles.value[index];
	URL.revokeObjectURL(file.previewUrl);
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

const saveAssignmentDetails = () => {
	assignmentStore.updateAssignmentData({
		question: assignmentStore.assignmentData.question,
		assessment_criteria: assignmentStore.assignmentData.assessment_criteria,
		attachments: uploadedFiles.value.map((file) => ({
			attachment: file.content,
			attachment_name: file.name,
		})),
	});
	emit("settings");
};

const previousPage = () => {
	emit("go-back");
};
</script>

<style scoped>
.assignment-details {
	background-color: #fff;
	padding: 20px;
	width: 96%;
	margin: auto;
}

.center-title {
	text-align: center;
}

.form-group {
	margin-bottom: 20px;
}

.form-group label {
	display: block;
	margin-bottom: 5px;
	font-weight: bold;
}

.form-group input,
.form-group textarea {
	width: 100%;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
}

.quill-editor {
	height: 200px;
	margin-bottom: 20px;
}

.criteria-container {
	background-color: #f9f9f9;
	padding: 10px;
	border: 1px solid #ddd;
	border-radius: 5px;
	margin-bottom: 20px;
}

.criteria-table {
	width: 100%;
	border-collapse: collapse;
}

.criteria-table th,
.criteria-table td {
	padding: 5px;
	text-align: center;
	vertical-align: middle;
}

.criteria-table th {
	background-color: #f9f9f9;
}

.criteria-table thead th {
	padding-bottom: 15px;
}

.criteria-table td.criteria-column {
	width: 80%;
}
.criteria-table td.grade-column {
	width: 20%;
}

.criteria-table td.trash-column {
	width: 5%;
}

.trash-icon {
	color: #c82333;
	transform: translateY(-3px);
}

.add-button,
.remove-button {
	background-color: transparent;
	color: white;
	border: none;
	cursor: pointer;
	font-size: 14px;
	outline: none;
}

.add-button {
	background-color: #0584ae;
	color: white;
}

.add-button:hover,
.add-button:focus {
	opacity: 0.9;
	background-color: #0584ae;
	color: #fff;
}

.remove-button:hover,
.remove-button:focus {
	opacity: 0.9;
	background-color: transparent;
	color: #c82333;
}

.form-actions {
	display: flex;
	justify-content: flex-end;
	margin-top: 20px;
}

button {
	padding: 10px 20px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	width: 15%;
	font-size: 14px;
}

.prev-btn {
	background-color: #0584ae;
	color: white;
	margin-right: 10px;
}

.next-btn {
	background-color: #0584ae;
	color: white;
}

.prev-btn:hover,
.next-btn:hover {
	opacity: 0.9;
}

.uploadFiles {
	width: 20%;
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
</style>
