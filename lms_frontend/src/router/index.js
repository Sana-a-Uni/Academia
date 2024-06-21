import { createRouter, createWebHistory } from "vue-router";

const routes = [
	{
		path: "/quizView",
		name: "quizView",
		component: () => import("../views/studentDashboard/quiz/quizView"),
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
		path: "/createQuiz",
		name: "createQuiz",
		component: () => import("../views/teacherDashboard/quiz/createQuiz"),
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
