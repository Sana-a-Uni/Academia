<template>
	<div class="container">
		<h1>Quiz Settings</h1>
		<form @submit.prevent="saveSettings">
			<div class="form-section">
				<div class="section-header">
					<input
						id="availability-check"
						type="checkbox"
						v-model="make_the_quiz_availability"
						class="checkbox-inline"
					/>
					<label for="availability-check" class="label-inline">Make the quiz availability</label>
				</div>
				<div
					:class="[
						'date-input',
						{ active: make_the_quiz_availability, faded: !make_the_quiz_availability },
					]"
					id="date-inputs"
				>
					<div class="inline-fields">
						<div class="from-date">
							<h4 style="margin-top: 6px; margin-right: 15px">From</h4>
							<DatetimePicker v-model="from_date" />
						</div>
						<div class="from-date">
							<h4 style="margin-top: 6px; margin-right: 15px">To</h4>
							<DatetimePicker v-model="to_date" />
						</div>
					</div>
				</div>
			</div>

			<div class="form-section">
				<div class="section-header">
					<input
						id="time-limit-check"
						type="checkbox"
						v-model="is_time_bound"
						class="checkbox-inline"
					/>
					<label for="time-limit-check" class="label-inline">is Time-Bound</label>
				</div>
				<div
					:class="['time-input', { active: is_time_bound, faded: !is_time_bound }]"
					id="time-input"
				>
					<DurationInput v-model="duration" @update:seconds="updateDurationInSeconds" />
				</div>
			</div>

			<div class="form-section">
				<div class="section-header">
					<input
						id="multiple-attempt-check"
						type="checkbox"
						v-model="multiple_attempts"
						class="checkbox-inline"
					/>
					<label for="multiple-attempt-check" class="label-inline">Multiple Attempts</label>
				</div>
				<div
					:class="['attempt-input', { active: multiple_attempts, faded: !multiple_attempts }]"
					id="attempt-input"
				>
					<label for="number_of_attempts" class="label-inline" v-if="multiple_attempts">
						Number of attempts
					</label>
					<input
						id="number_of_attempts"
						type="number"
						placeholder="Enter the number of attempts"
						class="input-field"
						v-model="number_of_attempts"
					/>
					<label for="grading_basis" class="label-inline" v-if="multiple_attempts">
						Grading Basis
					</label>

					<select
						id="grading_basis"
						placeholder="Select grading basis"
						class="input-field"
						v-if="multiple_attempts"
						v-model="grading_basis"
					>
						<option v-for="option in quizStore.gradingBasisOptions" :key="option" :value="option">
							{{ option }}
						</option>
					</select>
				</div>
			</div>

			<div class="form-section">
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
					:class="['group-input', { active: studentGroupActive, faded: !studentGroupActive }]"
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

			<div class="card-actions">
				<button class="prev-btn" @click="previousPage">Previous</button>
				<button class="save-btn" type="submit">Save</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, onMounted, computed, defineEmits } from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import moment from "moment";
import DurationInput from "@/components/teacher/DurationInput.vue";
import DatetimePicker from "@/components/teacher/DatetimePicker.vue";

const emit = defineEmits(["go-back", "save-settings"]);

const quizStore = useQuizStore();

const make_the_quiz_availability = ref(false);
const is_time_bound = ref(false);
const multiple_attempts = ref(false);
const studentGroupActive = ref(false);
const studentActive = ref(false);

const from_date = ref("");
const to_date = ref("");
const duration = ref("");
const durationInSeconds = ref(0);
const number_of_attempts = ref(1);
const grading_basis = ref("");
const selected_group = ref("");
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

const updateDurationInSeconds = (seconds) => {
	durationInSeconds.value = seconds;
};

const saveSettings = () => {
	const settingsData = {
		make_the_quiz_availability: make_the_quiz_availability.value,
		from_date: make_the_quiz_availability.value
			? moment(from_date.value).format("YYYY-MM-DD HH:mm:ss")
			: null,
		to_date: make_the_quiz_availability.value
			? moment(to_date.value).format("YYYY-MM-DD HH:mm:ss")
			: null,
		is_time_bound: is_time_bound.value,
		duration: is_time_bound.value ? durationInSeconds.value : null,
		multiple_attempts: multiple_attempts.value,
		number_of_attempts: multiple_attempts.value ? number_of_attempts.value : 1,
		grading_basis: multiple_attempts.value ? grading_basis.value : null,
		selected_group: selected_group.value,
		selected_students: students.value
			.filter((student) => student.selected)
			.map((student) => student.studentname),
	};
	emit("save-settings", settingsData);
};

const previousPage = () => {
	emit("go-back");
};

// جلب خيارات "grading_basis" عند تحميل المكون
onMounted(() => {
	quizStore.fetchGradingBasisOptions();
});
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
</style>
