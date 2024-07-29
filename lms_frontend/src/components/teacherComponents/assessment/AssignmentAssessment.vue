<template>
	<div class="container">
		<div class="assignment-panel">
			<div :class="['panel-header', { 'grey-background': !showDetails }]">
				<h4>Assignment Details</h4>
				<button @click="toggleDetails">
					<span v-if="showDetails">▲</span>
					<span v-else>▼</span>
				</button>
			</div>
			<div v-if="showDetails" class="grey-background">
				<div class="content-block">
					<h4>Question:</h4>
					<div class="assignment-content" v-html="details.question_text"></div>
				</div>
				<div class="content-block">
					<h4>Assignment Files</h4>
					<div class="indented-content">
						<div class="assignment-file">
							<ul>
								<li v-for="file in details.assignment_files" :key="file.file_name">
									<a :href="file.file_url" target="_blank">{{
										file.file_name
									}}</a>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</div>
			<div class="content-block">
				<h4>Student Answer:</h4>
				<p>{{ details.student_answer }}</p>
			</div>
			<div class="content-block">
				<h4>Student Files</h4>
				<div class="indented-content">
					<div class="assignment-file">
						<ul>
							<li v-for="file in details.student_files" :key="file.file_name">
								<a :href="file.file_url" target="_blank">{{ file.file_name }}</a>
							</li>
						</ul>
					</div>
				</div>
			</div>
			<div class="content-block">
				<h4>Comment:</h4>
				<p>{{ details.comment }}</p>
			</div>
		</div>
		<div class="evaluation-panel">
			<div class="panel-header">
				<h1>Assignment Evaluation</h1>
			</div>
			<div class="assessment-list">
				<table>
					<thead>
						<tr>
							<th>Assessment Criterion</th>
							<th>Max Grade</th>
							<th>Grade</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="(criteria, index) in details.assessment_criteria" :key="index">
							<td>{{ criteria.assessment_criteria }}</td>
							<td>{{ criteria.maximum_grade }}</td>
							<td>
								<input
									type="number"
									v-model="criteriaGrades[index]"
									:max="criteria.maximum_grade"
									min="0"
								/>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div class="feedback-section">
				<label for="feedback">Student Feedback</label>
				<textarea id="feedback" v-model="feedback" rows="10"></textarea>
			</div>
			<div class="buttons-section">
				<button @click="cancel">Cancel</button>
				<button @click="saveDraft">Save Draft</button>
				<button @click="submitEvaluation">Submit</button>
			</div>
			<div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
		</div>
		<SuccessDialog v-if="showDialog" :message="dialogMessage" />
	</div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAssessmentStore } from "@/stores/teacherStore/assessmentStore";
import SuccessDialog from "@/components/teacherComponents/SuccessDialog.vue"; 

const props = defineProps({
	details: {
		type: Object,
		required: true,
	},
	errors: {
		type: Object,
		default: () => ({}),
	},
});

const store = useAssessmentStore();
const route = useRoute();
const router = useRouter();
const criteriaGrades = ref([]);
const feedback = ref("");
const showDetails = ref(false);
const errorMessage = computed(() => store.error);
const showDialog = ref(false);
const dialogMessage = ref("");

const toggleDetails = () => {
	showDetails.value = !showDetails.value;
};

const cancel = () => {
	router.push({ name: "pendingAssessment" });
};

onMounted(async () => {
	try {
		const response = await fetchAssessmentDetails(route.params.submission_name);
		if (response && response.error) {
			throw new Error(response.error);
		}
	} catch (e) {
		console.error("Error fetching assessment details:", e);
		errorMessage.value = e.message;
	}
});

const fetchAssessmentDetails = async (assignmentSubmissionName) => {
	try {
		const response = await store.fetchAssignmentAssessment(assignmentSubmissionName);
		if (response && response.assignment_assessment_details) {
			const assessmentData = response;
			feedback.value = assessmentData.feedback || "";

			criteriaGrades.value = props.details.assessment_criteria.map((criteria) => {
				const detail = assessmentData.assignment_assessment_details.find(
					(detail) => detail.assessment_criteria === criteria.name
				);
				return detail ? detail.grade : 0;
			});
		} else {
			feedback.value = "";
			if (props.details && props.details.assessment_criteria) {
				criteriaGrades.value = props.details.assessment_criteria.map(() => 0);
			}
		}
		return response;
	} catch (e) {
		console.error("Error in fetchAssessmentDetails:", e);
		errorMessage.value = e.message;
		return { error: e.message };
	}
};

const saveDraft = async () => {
	try {
		if (props.details && props.details.assessment_criteria) {
			const payload = {
				assignment_submission: route.params.submission_name,
				feedback: feedback.value,
				assessment_date: formatDateTime(new Date()),
				criteria_grades: props.details.assessment_criteria.map((criteria, index) => ({
					assessment_criteria: criteria.name,
					grade: criteriaGrades.value[index],
				})),
				status: "draft",
			};

			const response = await store.saveAssessment(payload);
			if (response && response.status === "success") {
				dialogMessage.value = "Draft saved successfully.";
				showDialog.value = true;
				setTimeout(handleDialogClose, 1000);
			} else {
				throw new Error(response.message);
			}
		}
	} catch (e) {
		console.error("Error saving draft:", e);
		errorMessage.value = e.message;
	}
};

const submitEvaluation = async () => {
	try {
		if (props.details && props.details.assessment_criteria) {
			const payload = {
				assignment_submission: route.params.submission_name,
				feedback: feedback.value,
				assessment_date: formatDateTime(new Date()),
				criteria_grades: props.details.assessment_criteria.map((criteria, index) => ({
					assessment_criteria: criteria.name,
					grade: criteriaGrades.value[index],
				})),
				status: "submitted",
			};

			const response = await store.saveAssessment(payload);
			if (response && response.status === "success") {
				dialogMessage.value = "Evaluation submitted successfully.";
				showDialog.value = true;
				setTimeout(handleDialogClose, 1000); 
			} else {
				throw new Error(response.message);
			}
		}
	} catch (e) {
		console.error("Error submitting evaluation:", e);
		errorMessage.value = e.message;
	}
};

const handleDialogClose = () => {
	showDialog.value = false;
	router.push({ name: "pendingAssessment" });
};

const formatDateTime = (date) => {
	const d = new Date(date);
	const year = d.getFullYear();
	const month = String(d.getMonth() + 1).padStart(2, "0");
	const day = String(d.getDate()).padStart(2, "0");
	const hours = String(d.getHours()).padStart(2, "0");
	const minutes = String(d.getMinutes()).padStart(2, "0");
	const seconds = String(d.getSeconds()).padStart(2, "0");
	return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};
</script>

<style scoped>
body {
	font-family: Arial, sans-serif;
	margin: 0;
	padding: 0;
}
.error-message {
	color: red;
	margin-top: 10px;
}
.container {
	display: flex;
	width: 100%;
	padding: 20px;
	margin: 50px auto;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	box-sizing: border-box;
	border-radius: 8px;
	background-color: #fff;
}

.assignment-panel {
	width: 70%;
	padding-right: 20px;
	border-right: 1px solid #ddd;
}

.evaluation-panel {
	width: 30%;
	padding: 20px;
}

.panel-header {
	display: flex;
	justify-content: center;
	align-items: center;
	margin-bottom: 20px;
	position: relative;
	padding: 10px;
}

.panel-header h1 {
	margin: 0;
	font-size: 20px;
	display: flex;
	align-items: center;
}

.panel-header button {
	background: none;
	border: none;
	font-size: 16px;
	cursor: pointer;
	margin-left: 10px;
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
	padding: 8px;
	border: 1px solid #ccc;
	text-align: left;
	font-size: 12px;
}

.assessment-list th {
	background-color: #f4f4f4;
}

.feedback-section {
	margin-bottom: 20px;
}

.feedback-section label {
	display: block;
	margin-bottom: 5px;
	font-weight: bold;
}

.feedback-section textarea {
	width: 100%;
	padding: 10px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
	font-size: 12px;
}

.buttons-section button {
	width: 100%;
	padding: 10px;
	margin-bottom: 10px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	font-size: 14px;
}

.buttons-section button:first-of-type {
	background-color: #f4f4f4;
	color: #333;
}

.buttons-section button:nth-of-type(2) {
	background-color: #007bff;
	color: #fff;
	margin-bottom: 10px;
}

.buttons-section button:last-of-type {
	background-color: #007bff;
	color: #fff;
}

.content-block {
	margin-bottom: 20px;
}

h4 {
	margin-bottom: 10px;
	margin-top: 10px;
	font-size: 14px;
}

p {
	margin-bottom: 10px;
	font-size: 12px;
}

.indented-content {
	padding-left: 20px;
}

.assignment-content {
	width: 100%;
	padding: 10px;
	margin-bottom: 10px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
	background-color: #f4f4f4;
	font-size: 12px;
}

.assignment-file {
	margin-bottom: 20px;
}

ul {
	padding-left: 20px;
	list-style-type: disc;
	font-size: 12px;
}

.loading {
	font-size: 1.2em;
	text-align: center;
}

a {
	color: #2a73cc;
	text-decoration: none;
	font-size: 12px;
}

a:hover {
	text-decoration: underline;
}

.grey-background {
	background-color: #f9f9f9;
}

@media (max-width: 768px) {
	.container {
		flex-direction: column;
	}

	.assignment-panel {
		width: 100%;
		border-right: none;
		border-bottom: 1px solid #ddd;
		padding-right: 0;
	}

	.evaluation-panel {
		width: 100%;
	}

	.panel-header {
		justify-content: space-between;
	}

	h1 {
		font-size: 18px;
	}

	h4 {
		font-size: 14px;
	}

	.feedback-section textarea {
		font-size: 12px;
	}

	.buttons-section button {
		font-size: 12px;
		padding: 8px;
	}
}
</style>
