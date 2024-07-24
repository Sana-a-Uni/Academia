<template>
	<div class="container">
		<h1>Assignment Settings</h1>
		<form @submit.prevent="saveSettings">
			<!-- Availability Section -->
			<div class="form-section">
				<div class="section-header">
					<h3 class="section-title">Assignment Configuration</h3>
					<hr class="section-divider" />
				</div>
				<div class="section-header">
					<input
						id="availability-check"
						type="checkbox"
						v-model="assignmentStore.assignmentData.make_the_assignment_availability"
						class="checkbox-inline"
					/>
					<label for="availability-check" class="label-inline"
						>Make the assignment availability</label
					>
				</div>
				<div
					:class="[
						'date-input',
						{
							active: assignmentStore.assignmentData
								.make_the_assignment_availability,
							faded: !assignmentStore.assignmentData
								.make_the_assignment_availability,
						},
					]"
					id="date-inputs"
				>
					<div class="inline-fields">
						<div class="from-date">
							<h4 style="margin-top: 6px; margin-right: 15px">From</h4>
							<DatetimePicker v-model="assignmentStore.assignmentData.from_date" />
						</div>
						<div class="from-date">
							<h4 style="margin-top: 6px; margin-right: 15px">To</h4>
							<DatetimePicker v-model="assignmentStore.assignmentData.to_date" />
						</div>
					</div>
				</div>
			</div>

			<!-- Student Group Section -->
			<div class="form-section">
				<div class="section-header">
					<h3 class="section-title">Availability For</h3>
					<hr class="section-divider" />
				</div>
				<div class="section-header">
					<input
						id="student-group-check"
						type="checkbox"
						v-model="studentGroupActive"
						class="checkbox-inline"
					/>
					<label for="student-group-check" class="label-inline">Student Group</label>
				</div>
				<div
					:class="[
						'group-input',
						{ active: studentGroupActive, faded: !studentGroupActive },
					]"
					id="group-input"
				>
					<select class="input-field" v-model="selected_group">
						<option value="" disabled selected>Select Group</option>
						<option value="group1">Group 1</option>
						<option value="group2">Group 2</option>
						<option value="group3">Group 3</option>
					</select>
				</div>
			</div>

			<div class="form-section">
				<div class="section-header">
					<input
						id="student-check"
						type="checkbox"
						v-model="studentActive"
						class="checkbox-inline"
					/>
					<label for="student-check" class="label-inline">Student</label>
				</div>
				<div
					:class="['main-content', { active: studentActive, faded: !studentActive }]"
					id="student-section"
				>
					<div style="margin-left: 20px" class="header">
						<div class="search-bar">
							<input
								type="text"
								id="search"
								placeholder="Search"
								v-model="searchTerm"
								class="input-field"
							/>
							<select class="input-field2" v-model="selectedGroupForSearch">
								<option value="" disabled selected>Select Group</option>
								<option value="group1">Group 1</option>
								<option value="group2">Group 2</option>
								<option value="group3">Group 3</option>
							</select>
						</div>
					</div>
					<div class="table-container">
						<table>
							<thead>
								<tr>
									<th style="font-size: 14px">Select</th>
									<th style="font-size: 14px">Student Name</th>
									<th style="font-size: 14px">Group Name</th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="item in filteredItems" :key="item.studentname">
									<td>
										<input
											style="width: 18px; height: 18px"
											type="checkbox"
											v-model="item.selected"
										/>
									</td>
									<td style="font-size: 13px">{{ item.studentname }}</td>
									<td style="font-size: 13px">{{ item.groupname }}</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>

			<!-- Action Buttons -->
			<div class="card-actions">
				<button class="prev-btn" @click="previousPage">Previous</button>
				<button class="save-btn" type="submit">Save</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, onMounted, computed, defineEmits } from "vue";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import moment from "moment";
import DatetimePicker from "@/components/teacher/DatetimePicker.vue";

const emit = defineEmits(["go-back", "save-settings"]);

const assignmentStore = useAssignmentStore();

const studentGroupActive = ref(false);
const studentActive = ref(false);

const searchTerm = ref("");
const selectedGroupForSearch = ref("");

const students = ref([
	{ studentname: "Student 1", groupname: "Group 1", selected: false },
	{ studentname: "Student 2", groupname: "Group 2", selected: false },
	{ studentname: "Student 3", groupname: "Group 3", selected: false },
]);

const filteredItems = computed(() => {
	return students.value.filter((item) => {
		return (
			(item.groupname === selectedGroupForSearch.value || !selectedGroupForSearch.value) &&
			item.studentname.toLowerCase().includes(searchTerm.value.toLowerCase())
		);
	});
});

const saveSettings = () => {
	const settingsData = {
		make_the_assignment_availability:
			assignmentStore.assignmentData.make_the_assignment_availability,
		from_date: assignmentStore.assignmentData.from_date
			? moment(assignmentStore.assignmentData.from_date).format("YYYY-MM-DD HH:mm:ss")
			: null,
		to_date: assignmentStore.assignmentData.to_date
			? moment(assignmentStore.assignmentData.to_date).format("YYYY-MM-DD HH:mm:ss")
			: null,
		selected_group: assignmentStore.assignmentData.selected_group,
		selected_students: students.value
			.filter((student) => student.selected)
			.map((student) => student.studentname),
	};
	emit("save-settings", settingsData);
};

const previousPage = () => {
	emit("go-back");
};
</script>

<style scoped>
/* إضافة CSS المخصص هنا */
.container {
	max-width: 100%;
	margin: 0 auto;
	padding: 10px;
	background-color: #fff;
	box-shadow: 0 0 rgba(0, 0, 0, 0.1);
	box-sizing: border-box;
}

h1 {
	text-align: center;
	margin-bottom: 0px;
	font-size: 24px;
}

.form-section {
	margin-bottom: 20px;
}

.section-header {
	display: flex;
	align-items: center;
}

.section-title {
	margin: 0;
	font-size: 18px;
	font-weight: bold;
}

.inline-fields {
	display: flex;
	align-items: center;
	gap: 10px;
	margin-top: 10px; /* تعديل لخفض الحقول */
}

.date-label {
	margin: 0;
	font-size: 14px;
	line-height: 1.2; /* تعديل المحاذاة الرأسية للنص */
}

.section-header input {
	margin-right: 5px;
	margin-top: 20px;
}

.section-header label {
	font-size: 17px;
	margin-left: 10px;
}

.input-field {
	width: 100%;
	padding: 8px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
	font-size: 12px;
}

.input-field2 {
	padding: 8px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
	font-size: 12px;
}

.date-input,
.time-input,
.attempt-input,
.group-input {
	opacity: 0.5;
	display: block;
	pointer-events: none;
	margin-left: 40px;
}

.date-input.active,
.time-input.active,
.attempt-input.active,
.group-input.active {
	opacity: 1;
	pointer-events: auto;
}

.inline-fields {
	display: flex;
	align-items: center;
}

.inline-fields input {
	width: 150px;
}

.inline-fields span {
	width: 10px;
	text-align: center;
}

.card-actions {
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
}

.save-btn {
	background-color: #0584ae;
}

.prev-btn:hover,
.save-btn:hover {
	opacity: 0.9;
}

.main-content .header .search-bar input {
	font-size: 14px;
}

.main-content table {
	width: 100%;
	border-collapse: collapse;
	background-color: #f0f5f9;
	border-radius: 10px;
	overflow: hidden;
}

.main-content table thead th,
.main-content table tbody td {
	padding: 8px;
	font-size: 12px;
	text-align: left;
	border-bottom: 1px solid #ddd;
}

.main-content table thead {
	background-color: #e0e6ed;
}

.main-content table tbody tr:nth-child(even) {
	background-color: #f9fafc;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 10px;
}

.search-bar {
	display: flex;
	align-items: flex-start;
	margin-top: 10px;
}

.search-bar input {
	width: 180px;
	padding: 6px;
	border: 1px solid #ccc;
	border-radius: 5px;
	margin-right: 10px;
	margin-top: 0;
	font-size: 12px;
}

.search-bar select {
	width: 150px;
	height: 30px;
	padding: 6px;
	border: 1px solid #ccc;
	border-radius: 5px;
	font-size: 12px;
}

.table-container {
	max-height: 400px;
	overflow-y: auto;
}

.checkbox-inline {
	width: 14px;
	height: 14px;
	transform: scale(1.2);
	margin-right: 5px;
	vertical-align: middle;
}

.from-date {
	display: flex;
	width: 100%;
}

.section-header input {
	margin-right: 5px;
	margin-top: 20px;
}

.section-header label {
	font-size: 17px;
	margin-left: 10px;
}

.label-inline {
	vertical-align: middle;
}

.section-divider {
	border: none;
	border-top: 1px solid #ddd;
	margin-left: 10px;
	flex-grow: 1;
}

.results-display-options {
	display: flex;
	align-items: center;
	margin-top: 10px;
}

.option {
	display: flex;
	align-items: center;
	margin-right: 20px;
}

.option input {
	margin-right: 10px;
}
</style>
