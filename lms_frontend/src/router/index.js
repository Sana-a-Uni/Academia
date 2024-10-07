import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		path: "/",
		name: "login",
		component: () => import("../views/login"),
	},
	{
		path: "/teacherDashboard",
		name: "teacherDashboard",
		component: () => import("../views/teacherDashboard/dashboard"),
	},
	{
		path: "/teacherDashboard/courseView",
		name: "teacherCourseView",
		component: () => import("../views/teacherDashboard/courseView"),
	},
	{
		path: "/teacherDashboard/courseView/quizList",
		name: "quizzes",
		component: () => import("../views/teacherDashboard/quiz/quizView"),
	},
	{
		path: "/teacherDashboard/courseView/quizList/createQuiz",
		name: "createQuiz",
		component: () => import("../views/teacherDashboard/quiz/createQuiz"),
	},
	{
		path: "/teacherDashboard/courseView/assignments",
		name: "assignments",
		component: () => import("../views/teacherDashboard/assignment/assignmentView"),
	},
	{
		path: "/teacherDashboard/courseView/assignments/createAssignment",
		name: "createAssignment",
		component: () => import("../views/teacherDashboard/assignment/createAssignment"),
	},
	
	{
		path: "/teacherDashboard/courseView/pendingAssessment",
		name: "pendingAssessment",
		component: () => import("../views/teacherDashboard/assessment/pendingAssessment"),
	},
	{
		path: "/teacherDashboard/courseView/pendingAssessment/assignmentAssessment/:submission_name",
		name: "assessmentAssignment",
		component: () => import("../views/teacherDashboard/assessment/assignmentAssessment"),
	}
,	

	////////////////////////////
	{
		path: "/studentDashboard",
		name: "studentDashboard",
		component: () => import("../views/studentDashboard/dashboard"),
	},

	{
		path: "/courseView",
		name: "courseView",
		component: () => import("../views/studentDashboard/courseView"),
	},
	{
		path: "/quizView/:courseName/:studentId",
		name: "quizView",
		component: () => import("../views/studentDashboard/quiz/quizView"),
		props: true,
	},
	{
		path: "/quizInstructions/:quizName",
		name: "quizInstructions",
		component: () => import("../views/studentDashboard/quiz/quizInstructions"),
	},
	{
		path: "/quiz/:quizName",
		name: "quiz",
		component: () => import("../views/studentDashboard/quiz/quiz"),
	},
	{
		path: "/quizResult/:quizAttemptId",
		name: "quizResult",
		component: () => import("../views/studentDashboard/quiz/quizResult"),
	},
	{
		path: "/quizResultList",
		name: "quizResultList",
		component: () => import("../views/studentDashboard/quiz/quizResultList"),
	},
	{
		path: "/quizReview/:quizAttemptId/:questionIndex?",
		name: "quizReview",
		component: () => import("../views/studentDashboard/quiz/quizReview"),
		props: (route) => ({
			quizAttemptId: route.params.quizAttemptId,
			questionIndex: route.params.questionIndex
				? parseInt(route.params.questionIndex, 10)
				: 0,
		}),
	},

	
	
	{
		path: "/assignmentView",
		name: "assignmentView",
		component: () => import("../views/studentDashboard/assignment/assignmentView"),
	},
	{
		path: "/assignment/:assignmentName",
		name: "assignment",
		component: () => import("../views/studentDashboard/assignment/assignment"),
	},
	
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
