<template>
	<div class="grade-list">
		<div class="header">
			<h2>All Grades</h2>
			<div class="filters">
				<select v-model="selectedGradeType" class="custom-select">
					<option value="all">All Types</option>
					<option value="assignment">Assignment</option>
					<option value="quiz">Quiz</option>
					<option value="project">Project</option>
				</select>
			</div>
		</div>
		<table>
			<thead>
				<tr>
					<th class="title-column">Title</th>
					<th class="type-column">Type</th>
					<th class="grade-column">Grade</th>
				</tr>
			</thead>
			<tbody>
				<tr v-if="filteredGrades.length === 0">
					<td colspan="3" class="no-data">No Data</td>
				</tr>
				<tr v-else v-for="grade in filteredGrades" :key="grade.name">
					<td class="title-column">
						<router-link
							v-if="grade.type === 'quiz'"
							:to="{ name: 'quizDetails', params: { quiz_name: grade.name } }"
						>
							{{ grade.title }}
						</router-link>
						<router-link
							v-else-if="grade.type == 'assignment' || grade.type == 'project'"
							:to="{
								name: 'assignmentDetails',
								params: { assignment_name: grade.name },
							}"
						>
							{{ grade.title }}
						</router-link>
						<span v-else>{{ grade.title }}</span>
					</td>
					<td class="type-column">{{ grade.type }}</td>
					<td class="grade-column">{{ grade.grade }} / {{ grade.total_grades }}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
	grades: {
		type: Array,
		required: true,
	},
});

const selectedGradeType = ref("all");

const filteredGrades = computed(() => {
	if (selectedGradeType.value === "all") {
		return props.grades;
	}
	return props.grades.filter((grade) => grade.type === selectedGradeType.value);
});
</script>

<style scoped>
.grade-list {
	width: 100%;
	margin-top: 70px;
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

.filters {
	flex: 1;
	display: flex;
	justify-content: flex-start;
	margin: 0px;
}

.filters select {
	padding: 8px;
	padding-right: 32px;
	border: 1px solid #ddd;
	border-radius: 4px;
	font-size: 16px;
	appearance: none;
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

.no-data {
	text-align: center;
	color: #666;
	font-size: 1.2em;
	padding: 20px;
}

.title-column {
	width: 40%;
}

.type-column,
.grade-column,
.total-grade-column {
	width: 20%;
	text-align: center;
}

@media (max-width: 768px) {
	h2 {
		font-size: 18px;
		position: static;
		transform: none;
		order: 1;
	}

	.filters {
		order: 2;
		flex: 1;
		display: flex;
		justify-content: flex-end;
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

	.title-column,
	.type-column,
	.grade-column,
	.total-grade-column {
		width: auto;
	}
}
</style>
