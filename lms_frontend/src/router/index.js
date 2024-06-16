import { createRouter, createWebHistory } from "vue-router";

const routes = [
	// {
	// 	path: "/",
	// 	name: "home",
	// 	component: HomeView,
	// },
	{
		path: "/quizView",
		name: "quizView",
		component: () => import("../views/studentDashboard/quiz/quizView"),
	},
	{
		path: "/quizInstructions",
		name: "quizInstructions",
		component: () => import("../views/studentDashboard/quiz/quizInstructions"),
	},
	{
		path: "/quiz",
		name: "quiz",
		component: () => import("../views/studentDashboard/quiz/quiz"),
	},
	{
		path: "/quizResult",
		name: "quizResult",
		component: () => import("../views/studentDashboard/quiz/quizResult"),
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
