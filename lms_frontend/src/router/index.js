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
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
