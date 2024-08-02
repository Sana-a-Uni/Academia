import { createRouter, createWebHistory } from "vue-router";
import Cookies from "js-cookie";

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
		meta: { requiresAuth: true, requiresInstructor: true },
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
	},
	{
		path: "/teacherDashboard/courseView/completedAssessment",
		name: "completedAssessment",
		component: () => import("../views/teacherDashboard/assessment/completedAssessment"),
	},

	////////////////////////////
	{
		path: "/studentDashboard",
		name: "studentDashboard",
		component: () => import("../views/studentDashboard/dashboard"),
		meta: { requiresAuth: true, requiresStudent: true },
	},

	{
		path: "/courseView",
		name: "courseView",
		component: () => import("../views/studentDashboard/courseView"),
	},
	{
		path: "/quizView/:courseName",
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
		path: "/studentDashboard/assignmentView",
		name: "assignmentView",
		component: () => import("../views/studentDashboard/assignment/assignmentView"),
	},
	{
		path: "/studentDashboard/assignmentView/assignment/:assignmentName",
		name: "assignment",
		component: () => import("../views/studentDashboard/assignment/assignment"),
	},
	{
		path: "/studentDashboard/grades",
		name: "grades",
		component: () => import("../views/studentDashboard/grade/grades"),
	},
	{
		path: "/studentDashboard/grades/quizDetails/:quiz_name",
		name: "quizDetails",
		component: () => import("../views/studentDashboard/grade/quizDetails"),
	},
	{
		path: "/studentDashboard/grades/assignmentDetails/:assignment_name",
		name: "assignmentDetails",
		component: () => import("../views/studentDashboard/grade/assignmentDetails"),
	},

	{
		path: "/unauthorized",
		name: "unauthorized",
		component: () => import("../views/Unauthorized.vue"),
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});
router.beforeEach((to, from, next) => {
	const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
	const requiresStudent = to.matched.some((record) => record.meta.requiresStudent);
	const requiresInstructor = to.matched.some((record) => record.meta.requiresInstructor);

	const token = Cookies.get("authToken");
	const role = Cookies.get("role");

	const isLoggedIn = !!token;
	const isStudent = role === "Student";
	const isInstructor = role === "teacher";

	if (requiresAuth && !isLoggedIn) {
		next({ name: "login" }); 
	} else if (requiresAuth && requiresStudent && !isStudent) {
		next({ name: "unauthorized" }); 
	} else if (requiresAuth && requiresInstructor && !isInstructor) {
		next({ name: "unauthorized" }); 
	} else {
		next(); 
	}
});
export default router;
