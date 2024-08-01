<template>
	<div class="content">
		<div class="section-title">Assignment Details</div>
		<div v-if="assignmentDetails" class="detail-item">
			<span>Assignment Title:</span> {{ assignmentDetails.assignment_title }}
		</div>
		<div v-if="assignmentDetails" class="detail-item">
			<span>Due Date:</span> {{ assignmentDetails.to_date }}
		</div>
		<div v-if="assignmentDetails" class="detail-item">
			<span>Grade Possible:</span> {{ assignmentDetails.total_grades }}
			<div v-if="assignment_grade" class="detail-item">
				<span>Your assignment grade:</span> {{ assignment_grade }}
			</div>
			<div v-if="assignmentDetails.result_grade !== undefined" class="detail-item">
				<span>Your assignment result:</span> {{ assignmentDetails.result_grade }}
			</div>
			<div class="section-title"></div>

			<div class="sections-title">Assessment Criteria</div>
			<div v-if="assessmentCriteria && assessmentCriteria.length > 0" class="criteria">
				<table>
					<thead>
						<tr>
							<th>Criteria</th>
							<th>Maximum Grade</th>
							<th>Grade</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="criteria in assessmentCriteria" :key="criteria.id">
							<td>{{ criteria.criteria_text }}</td>
							<td>{{ criteria.maximum_grade }}</td>
							<td>{{ criteria.criteria_grade }}</td>
						</tr>
					</tbody>
				</table>
				<div v-if="feedback" class="feedback">
					<h3>Feedback:</h3>
					<p v-html="feedback"></p>
				</div>
			</div>
			<div v-else>
				<p>No assessment criteria available.</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
	assignmentDetails: {
		type: Object,
		required: true,
	},
	assessmentCriteria: {
		type: Array,
		required: true,
	},
	feedback: {
		type: String,
		required: true,
	},
	assignment_grade: {
		type: Number,
		required: true,
	},
});
</script>

<style scoped>
.content {
	padding: 20px;
}
.section-title {
	font-size: 18px;
	font-weight: bold;
	margin-bottom: 10px;
	border-bottom: 1px solid #ddd;
	padding-bottom: 5px;
}
.sections-title {
	font-size: 18px;
	font-weight: bold;
	margin-bottom: 10px;
	padding-bottom: 5px;
	text-align: center;
}
.detail-item {
	margin-bottom: 10px;
}
.detail-item span {
	font-weight: bold;
}
.criteria {
	margin-top: 20px;
}
.criteria table {
	width: 100%;
	border-collapse: collapse;
}
.criteria th,
.criteria td {
	padding: 10px;
	text-align: center;
	border: 1px solid #ddd;
}
.criteria th {
	background-color: #f8f8f8;
}
.feedback {
	margin-top: 20px;
}
</style>
