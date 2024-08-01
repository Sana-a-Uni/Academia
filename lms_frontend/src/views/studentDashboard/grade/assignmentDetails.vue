<template>
	<main-layout>
		<div class="container">
			<div class="header">View Assignment</div>
			<div v-if="loadingAssignment">Loading...</div>
			<div v-if="errorAssignment">{{ errorAssignment }}</div>
			<div v-if="!loadingAssignment && !errorAssignment">
				<AssignmentDetails
					:assignmentDetails="assignmentDetails"
					:assessmentCriteria="assessmentCriteria"
					:feedback="feedback"
					:assignment_grade="assignment_grade"
				/>
			</div>
		</div>
	</main-layout>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useGradeStore } from "@/stores/studentStore/gradeStore";
import AssignmentDetails from "@/components/student/grade/AssignmentDetails.vue";
import MainLayout from "@/components/MainLayout.vue";

const route = useRoute();
const gradeStore = useGradeStore();

const assignmentDetails = computed(() => gradeStore.assignmentDetails);
const assessmentCriteria = computed(() => gradeStore.assessmentCriteria);
const feedback = computed(() => gradeStore.feedback);
const assignment_grade = computed(() => gradeStore.assignment_grade);
const loadingAssignment = computed(() => gradeStore.loadingAssignment);
const errorAssignment = computed(() => gradeStore.errorAssignment);

onMounted(() => {
	const assignmentName = route.params.assignment_name;
	gradeStore.fetchAssignmentDetails(assignmentName);
});
</script>

<style scoped>
body {
	font-family: Arial, sans-serif;
	background-color: #f4f4f4;
	margin-top: 90px;
	margin-right: auto;
	padding: 0;
}
.container {
	background-color: white;
	width: 100%;
	height: 97vh;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	overflow: hidden;
}
.header {
	background-color: #f8f8f8;
	padding: 20px;
	text-align: center;
	font-size: 24px;
	font-weight: bold;
	border-bottom: 1px solid #ddd;
}
</style>
