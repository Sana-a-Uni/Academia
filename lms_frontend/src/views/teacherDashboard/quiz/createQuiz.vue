<template>
	<mainLayout>
		<QuizInformation v-if="currentView === 'information'" @quiz-created="currentView = 'questions'" />
		<QuizQuestion
			v-if="currentView === 'questions'"
			@go-back="currentView = 'information'"
			@settings="currentView = 'settings'"
			@addQuestion="currentView = 'addQuestion'"
			@reuseQuestion="currentView = 'reuseQuestion'"
		/>
		<QuizSettings v-if="currentView === 'settings'" @go-back="currentView = 'questions'" />
		<AddQuestion v-if="currentView === 'addQuestion'" @questions="currentView = 'questions'" />
		<ReuseQuestion v-if="currentView === 'reuseQuestion'" @go-back="currentView = 'questions'" />
	</mainLayout>
</template>
<script setup>
import { ref } from "vue";
import QuizInformation from "@/components/teacher/quiz/QuizInformation.vue";
import QuizQuestion from "@/components/teacher/quiz/QuizQuestion.vue";
import QuizSettings from "@/components/teacher/quiz/QuizSettings.vue";
import AddQuestion from "@/components/teacher/quiz/AddQuestion.vue";
import ReuseQuestion from "@/components/teacher/quiz/ReuseQuestion.vue";
import mainLayout from "@/components/teacher/layout/MainLayout.vue";

const currentView = ref("information");
</script>
