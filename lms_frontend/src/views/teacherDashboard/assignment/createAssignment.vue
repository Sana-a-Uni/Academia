<template>
	<main-layout>
		<AssignmentInformation
			v-if="currentView === 'information'"
			@assignment-created="handleAssignmentCreated"
			:errors="errors"
		/>
		<AssignmentQuestion
			v-if="currentView === 'questions'"
			:questions="assignmentStore.assignmentData.assessment_criteria"
			:errors="errors"
			@go-back="currentView = 'information'"
			@settings="currentView = 'settings'"
		/>
		<AssignmentSettings
			v-if="currentView === 'settings'"
			:errors="errors"
			@go-back="currentView = 'questions'"
			@save-settings="handleSaveSettings"
			@files-uploaded="handleFilesUploaded"
		/>
		<SuccessDialog v-if="showDialog" :message="dialogMessage" @close="showDialog = false" />
	</main-layout>
</template>

<script setup>
import { ref } from "vue";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import { useRouter } from "vue-router";
import AssignmentInformation from "@/components/teacherComponents/assignment/AssignmentInformation.vue";
import AssignmentQuestion from "@/components/teacherComponents/assignment/AssignmentQuestion.vue";
import AssignmentSettings from "@/components/teacherComponents/assignment/AssignmentSettings.vue";
import mainLayout from "@/components/teacherComponents/layout/MainLayout.vue";
import SuccessDialog from "@/components/teacherComponents/SuccessDialog.vue";

const currentView = ref("information");
const assignmentStore = useAssignmentStore();
const router = useRouter();
const errors = ref({});
const showDialog = ref(false);
const dialogMessage = ref("");

const handleAssignmentCreated = () => {
	currentView.value = "questions";
};

const handleSaveSettings = async (settingsData) => {
	assignmentStore.updateAssignmentData(settingsData);
	try {
		const response = await assignmentStore.createAssignment();
		if (response.success) {
			dialogMessage.value = "Your assignment has been created successfully.";
			showDialog.value = true;
			setTimeout(() => {
				showDialog.value = false;
				resetFields();
				router.push({ name: "assignments" });
			}, 1000); // Display the dialog for 1 second
		} else {
			errors.value = assignmentStore.errors;
			// Redirect to the view where the error is
			if (errors.value.assignment_title || errors.value.instruction) {
				currentView.value = "information";
			} else if (errors.value.questions || errors.value.assessment_criteria) {
				currentView.value = "questions";
			}
		}
	} catch (err) {
		errors.value = { general: err.message || "An error occurred" };
	}
};

const handleFilesUploaded = (files) => {
	assignmentStore.updateAssignmentData({ attachments: files });
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
	errors.value = {};
};
</script>
