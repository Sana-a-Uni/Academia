<template>
	<div class="grades-table">
		<h2>Grades Table</h2>
		<table>
			<thead>
				<tr>
					<th>Name</th>
					<th v-for="quiz in quizzes" :key="quiz">{{ quiz }}</th>
					<th v-for="assignment in assignments" :key="assignment">{{ assignment }}</th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="student in students" :key="student.name">
					<td>{{ student.name }}</td>
					<td v-for="quiz in quizzes" :key="quiz">
						{{ student.grades.quizzes[quiz] || "-" }}
					</td>
					<td v-for="assignment in assignments" :key="assignment">
						{{ student.grades.assignments[assignment] || "-" }}
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
	students: {
		type: Array,
		required: true,
	},
	quizzes: {
		type: Array,
		required: true,
	},
	assignments: {
		type: Array,
		required: true,
	},
});
</script>

<style scoped>
.grades-table {
	width: 100%;
	margin: 20px auto;
	border-collapse: collapse;
}

h2 {
	text-align: center;
	margin-bottom: 20px;
}

table {
	width: 100%;
	border: 1px solid #ddd;
}

th,
td {
	padding: 12px;
	border: 1px solid #ddd;
	text-align: center;
}

th {
	background-color: #f4f4f4;
}

td {
	background-color: #fff;
}

@media (max-width: 768px) {
	table,
	th,
	td {
		font-size: 12px;
		padding: 8px;
	}
}
</style>
