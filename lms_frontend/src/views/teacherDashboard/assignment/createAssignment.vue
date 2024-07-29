<template>
	<main-layout>
		<AssignmentInformation
			v-if="currentView === 'information'"
			@assignment-created="handleAssignmentCreated"
			:errors="errors"
		/>
		<AssignmentQuestion
			v-if="currentView === 'questions'"
			@go-back="currentView = 'information'"
			@settings="handleSettings"
			:errors="errors"
		/>
		<AssignmentSettings
			v-if="currentView === 'settings'"
			@go-back="currentView = 'questions'"
			@save-settings="handleSaveSettings"
			:errors="errors"
		/>
	</main-layout>
</template>

<script setup>
import { ref } from "vue";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import { useRouter } from "vue-router";
import AssignmentInformation from "@/components/teacherComponents/assignment/AssignmentInformation.vue";
import AssignmentQuestion from "@/components/teacherComponents/assignment/AssignmentQuestion.vue";
import AssignmentSettings from "@/components/teacherComponents/assignment/AssignmentSettings.vue";
import mainLayout from "@/components/MainLayout.vue";

const currentView = ref("information");
const assignmentStore = useAssignmentStore();
const router = useRouter();
const errors = ref({});

const handleAssignmentCreated = () => {
	currentView.value = "questions";
};

const handleSaveSettings = async (settingsData) => {
	assignmentStore.updateAssignmentData(settingsData);
	await assignmentStore.createAssignment();
	if (Object.keys(assignmentStore.errors).length === 0) {
		resetFields();
		router.push({ name: "assignments" });
	} else {
		errors.value = assignmentStore.errors;
		if (errors.value.assignment_title || errors.value.instruction) {
			currentView.value = "information";
		} else if (errors.value.question_or_attachment || errors.value.assessment_criteria) {
			currentView.value = "questions";
		} else if (errors.value.from_date || errors.value.to_date) {
			currentView.value = "settings";
		}
	}
};

const handleSettings = () => {
	currentView.value = "settings";
};

const resetFields = () => {
	assignmentStore.assignmentData = {
		assignment_title: "",
		course: "00",
		instruction: "",
		make_the_assignment_availability: false,
		from_date: "",
		to_date: "",
		question: "",
		assessment_criteria: [],
		attachments: [],
	};
};
</script>
