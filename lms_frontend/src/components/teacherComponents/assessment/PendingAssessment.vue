<template>
	<div class="assignment-list">
		<div class="header">
			<h2>For Assessment</h2>
		</div>
		<table>
			<thead>
				<tr>
					<th class="student-column">Student Name</th>
					<th class="assignment-column">Assignment Title</th>
					<th class="submission-date-column">Submission Date</th>
					<th class="action-column">Action</th>
				</tr>
			</thead>
			<tbody>
				<tr v-if="assignments.length === 0">
					<td colspan="4" class="no-data">No Data</td>
				</tr>
				<tr
					v-else
					v-for="assignment in assignments"
					:key="assignment.assignment_submission_name"
				>
					<td class="student-column">{{ assignment.student_name }}</td>
					<td class="assignment-column">{{ assignment.assignment_title }}</td>
					<td class="submission-date-column">
						{{ formatDate(assignment.submission_date) }}
					</td>
					<td class="action-column">
						<button
							@click="evaluateAssignment(assignment.assignment_submission_name)"
							class="evaluate-button"
						>
							Evaluate
						</button>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
import { defineProps } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
	assignments: {
		type: Array,
		required: true,
	},
});

const router = useRouter();

function formatDate(dateString) {
	const date = new Date(dateString);
	const day = date.getDate().toString().padStart(2, "0");
	const month = (date.getMonth() + 1).toString().padStart(2, "0");
	const year = date.getFullYear();
	const hours = date.getHours();
	const minutes = date.getMinutes().toString().padStart(2, "0");
	return `${day}/${month}/${year} ${hours}:${minutes}`;
}

function evaluateAssignment(submissionName) {
	router.push({
		name: "assessmentAssignment",
		params: { submission_name: submissionName },
	});
}

</script>

<style scoped>
.assignment-list {
	width: 100%;
	margin: 0 auto;
	border-collapse: collapse;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20px;
	padding: 0 20px;
	position: relative;
	padding: 20px;
}

h2 {
	margin: 0;
	font-size: 24px;
	position: absolute;
	left: 50%;
	transform: translateX(-50%);
}

table {
	width: calc(100% - 40px);
	margin: 0 20px;
	border: 1px solid #ddd;
}

th,
td {
	padding: 12px;
	border: 1px solid #ddd;
	vertical-align: middle;
}

th {
	background-color: #f4f4f4;
	text-align: center;
}

.no-data {
	text-align: center;
	color: #666;
	font-size: 1.2em;
	padding: 20px;
}

.student-column {
	width: 30%;
	text-align: left;
}

.assignment-column {
	width: 30%;
	text-align: left;
}

.submission-date-column {
	width: 20%;
	text-align: center;
}

.action-column {
	width: 20%;
	text-align: center;
}

.evaluate-button {
	background-color: #4caf50;
	color: white;
	border: none;
	padding: 10px 20px;
	cursor: pointer;
	border-radius: 4px;
}

.evaluate-button:hover {
	background-color: #45a049;
}

@media (max-width: 768px) {
	h2 {
		font-size: 18px;
		position: static;
		transform: none;
		order: 1;
	}

	table {
		width: 100%;
		margin: 0;
	}

	th,
	td {
		font-size: 12px;
		padding: 8px;
	}

	.student-column,
	.assignment-column,
	.submission-date-column,
	.action-column {
		width: auto;
		text-align: left;
	}

	.evaluate-button {
		padding: 8px 16px;
	}
}
</style>
