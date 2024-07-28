<template>
	<div class="assignment-list">
		<div class="header">
			<h2>All Assignments</h2>
			<div class="actions">
				<div class="filters">
					<select v-model="selectedAssignment" class="custom-select">
						<option value="all">All Assignments</option>
						<option value="available">Available</option>
						<option value="expired">Expired</option>
					</select>
				</div>
				<button class="create-assignment-btn" @click="goToCreateAssignment">
					Create Assignment
				</button>
			</div>
		</div>
		<table>
			<thead>
				<tr>
					<th class="number-column">#</th>
					<th class="assignment-column">Assignment Title</th>
					<th class="due-column">Start Date</th>
					<th class="due-column">End Date</th>
					<th class="grade-column">Total Grades</th>
				</tr>
			</thead>
			<tbody v-if="assignments && assignments.length > 0">
				<tr v-if="filteredAssignments.length === 0">
					<td colspan="5" class="no-data">No Data</td>
				</tr>
				<tr
					v-else
					v-for="(assignment, index) in filteredAssignments"
					:key="assignment.name"
				>
					<td class="number-column">{{ index + 1 }}</td>
					<td class="assignment-column">{{ assignment.assignment_title }}</td>
					<td class="due-column">
						<div>{{ formatDate(assignment.from_date) }}</div>
						<div>{{ formatTime(assignment.from_date) }}</div>
					</td>
					<td class="due-column">
						<div>{{ formatDate(assignment.to_date) }}</div>
						<div>{{ formatTime(assignment.to_date) }}</div>
					</td>
					<td class="grade-column">{{ assignment.total_grades }}</td>
				</tr>
			</tbody>
		</table>
		<div v-show="!(assignments && assignments.length > 0)" class="no-data">No Data</div>
	</div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const props = defineProps({
	assignments: {
		type: Array,
		required: true,
	},
});

const selectedAssignment = ref("all");
const router = useRouter();

const filteredAssignments = computed(() => {
	if (!props.assignments) return [];
	const now = new Date();
	return props.assignments.filter((assignment) => {
		const dueDate = new Date(assignment.to_date);
		switch (selectedAssignment.value) {
			case "available":
				return now <= dueDate;
			case "expired":
				return now > dueDate;
			default:
				return true;
		}
	});
});

const goToCreateAssignment = () => {
	router.push({ name: "createAssignment" });
};

function formatDate(dateString) {
	const date = new Date(dateString);
	const day = date.getDate().toString().padStart(2, "0");
	const month = (date.getMonth() + 1).toString().padStart(2, "0"); // Months are zero-indexed
	const year = date.getFullYear();
	return `${day}/${month}/${year}`;
}

function formatTime(dateString) {
	const date = new Date(dateString);
	let hours = date.getHours();
	const minutes = date.getMinutes();
	const ampm = hours >= 12 ? "PM" : "AM";
	hours = hours % 12;
	hours = hours ? hours : 12; // the hour '0' should be '12'
	const strMinutes = minutes < 10 ? "0" + minutes : minutes;
	return hours + ":" + strMinutes + " " + ampm;
}
</script>

<style scoped>
.assignment-list {
	width: 90%;
	border-collapse: collapse;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 20px;
	padding: 0 20px;
	position: relative;
}

.actions {
	display: flex;
	justify-content: space-between;
	align-items: center;
	width: 100%;
}

.create-assignment-btn {
	background-color: #4caf50;
	color: white;
	border: none;
	border-radius: 5px;
	padding: 10px 20px;
	cursor: pointer;
	font-size: 16px;
}

.create-assignment-btn:hover {
	background-color: #45a049;
}

.filters {
	display: flex;
	justify-content: flex-start;
}

.filters select {
	margin-left: 20px;
	padding: 8px;
	padding-right: 32px; /* Add space for arrow */
	border: 1px solid #ddd;
	border-radius: 4px;
	font-size: 16px;
	appearance: none; /* Remove default arrow */
	background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down"><polyline points="6 9 12 15 18 9"></polyline></svg>')
		no-repeat right 8px center;
	background-size: 16px 16px;
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

.number-column {
	width: 5%;
	text-align: center;
}

.assignment-column {
	width: 15%;
	text-align: center;
}

.due-column {
	width: 15%;
	text-align: center;
}

.grade-column {
	width: 10%;
	text-align: center;
}

a {
	color: #2a73cc;
	text-decoration: none;
	cursor: pointer;
	position: relative;
}

a.disabled {
	color: #000000;
	cursor: not-allowed;
	pointer-events: none;
}

a:hover:not(.disabled) {
	text-decoration: underline;
}

.tooltip {
	position: absolute;
	background-color: #f4f4f4;
	color: #000;
	font-weight: bold;
	padding: 5px;
	border-radius: 3px;
	white-space: nowrap;
	z-index: 10;
	font-size: 12px;
	top: 70%;
	left: 10%;
	transform: translateY(-50%);
	opacity: 0;
	transition: opacity 0.2s ease-in-out;
}

.assignment-column:hover .tooltip {
	opacity: 1;
}

.no-data {
	text-align: center;
	color: #666;
	font-size: 1.2em;
	padding: 20px;
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

	table {
		width: 100%;
		margin: 0;
	}

	th,
	td {
		font-size: 12px;
		padding: 8px;
	}

	.due-column,
	.grade-column {
		width: auto;
	}

	.assignment-column {
		width: auto;
	}
}
</style>
