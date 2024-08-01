<template>
	<main-layout>
		<LoadingSpinner v-if="gradeStore.loadingGrades" />
		<div v-else-if="gradeStore.errorGrades">{{ gradeStore.errorGrades }}</div>
		<GradeList v-else :grades="gradeStore.grades" />
	</main-layout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useGradeStore } from "@/stores/studentStore/gradeStore";
import GradeList from "@/components/student/grade/Grades.vue";
import mainLayout from "@/components/MainLayout.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

const route = useRoute();
const gradeStore = useGradeStore();
const courseName = ref("00");

onMounted(() => {
	gradeStore.fetchGrades(courseName.value);
});
</script>
