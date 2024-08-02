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
						>Make the assignment available</label
					>
				</div>
				<div
					:class="[
						'date-input',
						{
							active: assignmentStore.assignmentData.make_the_assignment_availability,
							faded: !assignmentStore.assignmentData.make_the_assignment_availability,
						},
					]"
					id="date-inputs"
				>
					<div class="inline-fields">
						<div class="from-date">
							<h4 style="margin-top: 6px; margin-right: 15px">From</h4>
							<DatetimePicker v-model="assignmentStore.assignmentData.from_date" />
						</div>
						<div class="error-message" v-if="assignmentStore.errors.from_date">
							{{ assignmentStore.errors.from_date }}
						</div>
						<div class="from-date">
							<h4 style="margin-top: 6px; margin-right: 15px">To</h4>
							<DatetimePicker v-model="assignmentStore.assignmentData.to_date" />
						</div>
						<div class="error-message" v-if="assignmentStore.errors.to_date">
							{{ assignmentStore.errors.to_date }}
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
					<select class="input-field" v-model="selectedGroups" multiple>
						<option value="" disabled>Select Group(s)</option>
						<option
							v-for="item in selectedCourse.program_student_batch_group"
							:key="`${item.program}-${item.student_batch}-${item.group}`"
							:value="item"
						>
							{{ item.program }} - {{ item.student_batch }} - {{ item.group }}
						</option>
					</select>
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
import { ref, computed, defineEmits } from "vue";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import { useCourseStore } from "@/stores/teacherStore/courseStore";
import moment from "moment";
import DatetimePicker from "@/components/teacher/DatetimePicker.vue";

const emit = defineEmits(["go-back", "save-settings"]);

const assignmentStore = useAssignmentStore();
const courseStore = useCourseStore();
const selectedCourse = computed(() => courseStore.selectedCourse);

const studentGroupActive = ref(false);
const selectedGroups = ref([]);

const saveSettings = async () => {
	try {
		if (selectedGroups.value.length === 0) {
			throw new Error("Please select at least one student group.");
		}

		const settingsData = {
			make_the_assignment_availability:
				assignmentStore.assignmentData.make_the_assignment_availability,
			from_date: assignmentStore.assignmentData.from_date
				? moment(assignmentStore.assignmentData.from_date).format("YYYY-MM-DD HH:mm:ss")
				: null,
			to_date: assignmentStore.assignmentData.to_date
				? moment(assignmentStore.assignmentData.to_date).format("YYYY-MM-DD HH:mm:ss")
				: null,
			program_student_batch_group: selectedGroups.value,
		};

		assignmentStore.updateAssignmentData(settingsData);
		await assignmentStore.createAssignment();
		emit("save-settings", settingsData);
	} catch (error) {
		console.error("Failed to save settings:", error);
		alert("An error occurred while creating the assignment: " + error.message);
	}
};

const previousPage = () => {
	emit("go-back");
};
</script>

<style scoped>
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
	margin-bottom: 20px;
	font-size: 24px;
}

.error-message {
	color: red;
	font-size: 12px;
	margin-top: 5px;
	display: block;
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
	margin-top: 10px;
}

.date-label {
	margin: 0;
	font-size: 14px;
	line-height: 1.2;
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

.date-input,
.group-input {
	opacity: 0.5;
	display: block;
	pointer-events: none;
	margin-left: 40px;
}

.date-input.active,
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
	font-size: 16px;
}

.main-content table thead th,
.main-content table tbody td {
	padding: 8px;
	font-size: 16px;
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

.card-actions {
	display: flex;
	justify-content: flex-end;
	margin-top: 20px;
	width: 100%;
	position: absolute;
	bottom: 10px;
	right: 10px;
}
</style>
