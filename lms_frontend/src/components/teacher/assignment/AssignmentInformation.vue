<template>
	<div class="container">
		<h1>Create a New Assignment</h1>
		<form @submit.prevent="createAssignment">
			<label for="assignmentTitle">Assignment Title:</label>
			<input
				type="text"
				id="assignmentTitle"
				v-model="assignmentStore.assignmentData.assignment_title"
			/>

			<label for="assignmentInstruction">Assignment Instruction:</label>
			<div ref="quillEditor" class="quill-editor"></div>

			<div class="button-group">
				<button type="button" @click="cancelAssignment">Cancel</button>
				<button type="submit">Next</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import Quill from "quill";
import { useAssignmentStore } from "@/stores/teacherStore/assignmentStore";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

const emit = defineEmits(["assignment-created"]);

const assignmentStore = useAssignmentStore();
const quillEditor = ref(null);

const editorOptions = {
	theme: "snow",
	modules: {
		toolbar: [
			[{ header: [1, 2, false] }],
			["bold", "italic", "underline"],
			[{ list: "ordered" }, { list: "bullet" }],
			[{ align: [] }],
			["clean"],
		],
	},
};

onMounted(() => {
	nextTick(() => {
		const editor = new Quill(quillEditor.value, editorOptions);
		editor.root.innerHTML = assignmentStore.assignmentData.instruction; // Load existing data
		editor.on("text-change", () => {
			assignmentStore.assignmentData.instruction = editor.root.innerHTML;
		});
	});
});

const createAssignment = () => {
	emit("assignment-created");
};

const cancelAssignment = () => {
	assignmentStore.assignmentData.assignment_title = "";
	assignmentStore.assignmentData.instruction = "";
};
</script>

<style>
body {
	font-family: Arial, sans-serif;
	margin: 0;
	padding: 0;
}

.container {
	width: 94%;
	padding: 2px 20px;
	margin-left: 10px;
	box-sizing: border-box;
}

h1 {
	text-align: center;
	margin-bottom: 20px;
	font-size: 24px;
}

label {
	display: block;
	margin: 10px 0 7px;
}

input,
select,
textarea {
	width: 100%;
	padding: 10px;
	margin-bottom: 20px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
}

.button-group {
	display: flex;
	justify-content: flex-end;
}

button {
	padding: 10px 20px;
	background-color: #0584ae;
	color: #fff;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	width: 15%;
	font-size: 14px;
	margin-left: 10px;
	margin-bottom: 10px;
}

button[type="button"] {
	background-color: #c82333;
}

button:hover {
	opacity: 0.9;
}

button[type="button"]:hover {
	background-color: #dc3545;
}

.quill-editor {
	height: 300px;
	margin-bottom: 20px;
}

@media (max-width: 600px) {
	.container {
		padding: 10px;
	}

	button {
		padding: 8px;
		font-size: 12px;
		width: 25%;
	}
}
</style>
