<template>
	<main-layout>
		<CompletedAssessment :students="students" :quizzes="quizzes" :assignments="assignments" />
	</main-layout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAssessmentStore } from "@/stores/teacherStore/assessmentStore";
import { useCourseStore } from "@/stores/teacherStore/courseStore";
import CompletedAssessment from "@/components/teacherComponents/assessment/CompletedAssessment.vue";
import mainLayout from "@/components/teacherComponents/layout/MainSub.vue";

const assessmentStore = useAssessmentStore();
const courseStore = useCourseStore();

const selectedCourse = computed(() => courseStore.selectedCourse);

const loadGrades = async () => {
	if (selectedCourse.value) {
		await assessmentStore.fetchQuizAndAssignmentGrades(
			selectedCourse.value.course,
			selectedCourse.value.course_type
		);
		console.log(selectedCourse.value.course);
	}
};

onMounted(() => {
	loadGrades();
});

const quizzes = computed(() => {
	const quizTitles = assessmentStore.quizzes.map((quiz) => quiz.quiz_title);
	return Array.from(new Set(quizTitles));
});

const assignments = computed(() => {
	const assignmentTitles = assessmentStore.assignments.map(
		(assignment) => assignment.assignment_title
	);
	return Array.from(new Set(assignmentTitles));
});

const students = computed(() => {
	const studentGrades = {};

	assessmentStore.quizzes.forEach((quiz) => {
		if (!studentGrades[quiz.student_name]) {
			studentGrades[quiz.student_name] = {
				fullName: quiz.student_full_name,
				quizzes: {},
				assignments: {},
			};
		}
		studentGrades[quiz.student_name].quizzes[quiz.quiz_title] = quiz.quiz_grade;
	});

	assessmentStore.assignments.forEach((assignment) => {
		if (!studentGrades[assignment.student_name]) {
			studentGrades[assignment.student_name] = {
				fullName: assignment.student_full_name,
				quizzes: {},
				assignments: {},
			};
		}
		studentGrades[assignment.student_name].assignments[assignment.assignment_title] =
			assignment.assignment_grade;
	});

	return Object.keys(studentGrades).map((studentName) => ({
		name: studentName,
		fullName: studentGrades[studentName].fullName,
		grades: studentGrades[studentName],
	}));
});
</script>
<style scoped>
* {
	width: 94%;
	margin: 0px;
}
</style>
