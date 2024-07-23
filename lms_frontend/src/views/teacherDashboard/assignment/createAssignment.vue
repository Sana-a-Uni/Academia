<template>
	<main-layout>
		<AssignmentInformation
			v-if="currentView === 'information'"
			@assignment-created="handleAssignmentCreated"
		/>
		<AssignmentQuestion
			v-if="currentView === 'questions'"
			:questions="assignmentStore.assignmentData.assessment_criteria"
			@go-back="currentView = 'information'"
			@settings="currentView = 'settings'"
		/>
		<AssignmentSettings
			v-if="currentView === 'settings'"
			@go-back="currentView = 'questions'"
			@save-settings="handleSaveSettings"
			@files-uploaded="handleFilesUploaded"
		/>
	</main-layout>
</template>

<script setup>
import { ref } from "vue";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import { useRouter } from "vue-router";
import AssignmentInformation from "@/components/teacher/assignment/AssignmentInformation.vue";
import AssignmentQuestion from "@/components/teacher/assignment/AssignmentQuestion.vue";
import AssignmentSettings from "@/components/teacher/assignment/AssignmentSettings.vue";
import mainLayout from "@/components/teacher/layout/MainLayout.vue";

const currentView = ref("information");
const assignmentStore = useAssignmentStore();
const router = useRouter();

const handleAssignmentCreated = () => {
	currentView.value = "questions";
};

const handleSaveSettings = (settingsData) => {
	assignmentStore.updateAssignmentData(settingsData);
	assignmentStore.createAssignment().then(() => {
		resetFields(); // Call resetFields after creating the assignment
		router.push({ name: "assignments" }); // Redirect to assignmentList after creating the assignment
	});
};

const handleFilesUploaded = (files) => {
	assignmentStore.updateAssignmentData({ attachments: files });
};

const resetFields = () => {
	assignmentStore.assignmentData = {
		assignment_title: "",
		course: "00",
		faculty_member: "ACAD-FM-00001",
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
