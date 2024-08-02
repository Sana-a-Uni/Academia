<template>
	<main-layout>
		<QuizInformation
			v-if="currentView === 'information'"
			@quiz-created="handleQuizCreated"
			:errors="errors"
		/>
		<QuizQuestion
			v-if="currentView === 'questions'"
			:questions="quizStore.quizData.quiz_question"
			:errors="errors"
			@go-back="currentView = 'information'"
			@settings="currentView = 'settings'"
			@addQuestion="currentView = 'addQuestion'"
			@reuseQuestion="currentView = 'reuseQuestion'"
			@deleteQuestion="handleDeleteQuestion"
		/>
		<QuizSettings
			v-if="currentView === 'settings'"
			:errors="errors"
			@go-back="currentView = 'questions'"
			@save-settings="handleSaveSettings"
		/>
		<AddQuestion
			v-if="currentView === 'addQuestion'"
			@questions="handleAddQuestion"
			@cancel="currentView = 'questions'"
		/>
		<ReuseQuestion
			v-if="currentView === 'reuseQuestion'"
			@questions="handleReuseQuestion"
			@cancel="currentView = 'questions'"
		/>
		<SuccessDialog v-if="showDialog" :message="dialogMessage" @close="showDialog = false" />
	</main-layout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import { useCourseStore } from "@/stores/teacherStore/courseStore";
import { useRouter, useRoute } from "vue-router";
import QuizInformation from "@/components/teacherComponents/quiz/QuizInformation.vue";
import QuizQuestion from "@/components/teacherComponents/quiz/QuizQuestion.vue";
import QuizSettings from "@/components/teacherComponents/quiz/QuizSettings.vue";
import AddQuestion from "@/components/teacherComponents/quiz/AddQuestion.vue";
import ReuseQuestion from "@/components/teacherComponents/quiz/ReuseQuestion.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";
import SuccessDialog from "@/components/teacherComponents/SuccessDialog.vue";

const currentView = ref("information");
const quizStore = useQuizStore();
const courseStore = useCourseStore();
const router = useRouter();
const route = useRoute();
const errors = ref({});
const showDialog = ref(false);
const dialogMessage = ref("");

const selectedCourse = computed(() => courseStore.selectedCourse);

onMounted(async () => {
	const courseId = route.params.courseId; // تأكد من أن لديك مسار يحتوي على معرف الدورة
	await courseStore.fetchCourses();
	console.log("Fetched courses:", courseStore.courses); // طباعة الدورات التي تم جلبها للتحقق منها
	const course = courseStore.courses.find((course) => course.id === courseId);
	if (course) {
		courseStore.selectCourse(course);
	} else {
		console.error("Course information is missing.");
		alert("An error occurred: Course information is missing.");
	}
});

const handleQuizCreated = () => {
	currentView.value = "questions";
	if (selectedCourse.value) {
		quizStore.updateQuizData({ course: selectedCourse.value.course });
		console.log("Quiz Data after course update:", quizStore.quizData); // طباعة بيانات الكويز بعد التحديث
	} else {
		console.error("Selected course is missing.");
	}
};

const handleSaveSettings = async (settingsData) => {
	if (selectedCourse.value) {
		settingsData.course = selectedCourse.value.course;
		console.log("Course being used:", settingsData.course); // تأكد من أن الدورة تستخدم هنا
		quizStore.updateQuizData(settingsData);
		console.log("Quiz Data before sending:", quizStore.quizData); // طباعة بيانات الكويز قبل الإرسال
		try {
			const success = await quizStore.createQuiz();
			if (success) {
				dialogMessage.value = "Your quiz has been created successfully.";
				showDialog.value = true;
				setTimeout(() => {
					showDialog.value = false;
					resetFields();
					router.push({ path: "/teacherDashboard/courseView/quizList" });
				}, 2000);
			} else {
				errors.value = quizStore.errors;
				if (errors.value.title || errors.value.instruction) {
					currentView.value = "information";
				} else if (errors.value.questions) {
					currentView.value = "questions";
				}
			}
		} catch (err) {
			if (err.response && err.response.data && err.response.data.errors) {
				errors.value = err.response.data.errors;
				if (errors.value.title || errors.value.instruction) {
					currentView.value = "information";
				} else if (errors.value.questions) {
					currentView.value = "questions";
				}
			}
		}
	} else {
		console.error("Course information is missing.");
		alert("An error occurred: Course information is missing.");
	}
};

const handleAddQuestion = ({ questionData, stayOnPage }) => {
	quizStore.addQuestion(questionData);
	if (!stayOnPage) {
		currentView.value = "questions";
	}
	errors.value = {};
};

const handleReuseQuestion = (selectedQuestions) => {
	if (!selectedQuestions) {
		selectedQuestions = [];
	}
	selectedQuestions.forEach((question) => {
		quizStore.addQuestion({
			name: question.name,
			question: question.question,
			question_options: question.question_options,
			question_grade: question.question_grade,
		});
	});
	currentView.value = "questions";
	errors.value = {};
};

const handleDeleteQuestion = (index) => {
	quizStore.quizData.quiz_question.splice(index, 1);
	if (quizStore.quizData.quiz_question.length === 0) {
		errors.value = { questions: [{ question: "At least one question is required." }] };
	} else {
		errors.value = {};
	}
};

const resetFields = () => {
	quizStore.quizData.title = "";
	quizStore.quizData.instruction = "";
	quizStore.quizData.make_the_quiz_availability = false;
	quizStore.quizData.from_date = "";
	quizStore.quizData.to_date = "";
	quizStore.quizData.is_time_bound = false;
	quizStore.quizData.duration = 0;
	quizStore.quizData.multiple_attempts = false;
	quizStore.quizData.number_of_attempts = "";
	quizStore.quizData.grading_basis = "";
	quizStore.quizData.quiz_question = [];
	quizStore.quizData.show_question_score = false;
	quizStore.quizData.show_correct_answer = false;
	quizStore.quizData.randomize_question_order = false;
	quizStore.quizData.randomize_option_order = false;
	errors.value = {};
};
</script>

<style scoped>
/* أضف أنماط CSS هنا */
</style>
