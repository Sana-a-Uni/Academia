<template>
	<div>
		<CompletedAssessment :students="students" :quizzes="quizzes" :assignments="assignments" />
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAssessmentStore } from "@/stores/teacherStore/assessmentStore";
import CompletedAssessment from "@/components/teacherComponents/assessment/CompletedAssessment.vue";

const assessmentStore = useAssessmentStore();
const facultyMember = ref("ACAD-FM-00001");
const course = ref("00");

const loadGrades = () => {
	assessmentStore.fetchQuizAndAssignmentGrades(facultyMember.value, course.value);
};

onMounted(() => {
	loadGrades();
});

const quizzes = computed(() => {
	const quizTitles = assessmentStore.quizzes.map((quiz) => quiz.quiz_title);
	return Array.from(new Set(quizTitles)); // إزالة التكرارات
});

const assignments = computed(() => {
	const assignmentTitles = assessmentStore.assignments.map(
		(assignment) => assignment.assignment_title
	);
	return Array.from(new Set(assignmentTitles)); // إزالة التكرارات
});

const students = computed(() => {
	const studentGrades = {};

	assessmentStore.quizzes.forEach((quiz) => {
		if (!studentGrades[quiz.student_name]) {
			studentGrades[quiz.student_name] = { quizzes: {}, assignments: {} };
		}
		studentGrades[quiz.student_name].quizzes[quiz.quiz_title] = quiz.quiz_grade;
	});

	assessmentStore.assignments.forEach((assignment) => {
		if (!studentGrades[assignment.student_name]) {
			studentGrades[assignment.student_name] = { quizzes: {}, assignments: {} };
		}
		studentGrades[assignment.student_name].assignments[assignment.assignment_title] =
			assignment.assignment_grade;
	});

	return Object.keys(studentGrades).map((studentName) => ({
		name: studentName,
		grades: studentGrades[studentName],
	}));
});
</script>
