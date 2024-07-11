<template>
	<div class="container">
		<h1>Create a New Quiz</h1>
		<form @submit.prevent="createQuiz">
			<label for="quizTitle">Quiz Title:</label>
			<input type="text" id="quizTitle" v-model="quizStore.quizData.title" />

			<label for="quizInstruction">Quiz Instruction:</label>
			<div ref="quillEditor" class="quill-editor"></div>

			<div class="button-group">
				<button type="button" @click="cancelQuiz">Cancel</button>
				<button type="submit">Next</button>
			</div>
		</form>
	</div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import Quill from "quill";
import { useQuizStore } from "@/stores/teacherStore/quizStore";
import "@vueup/vue-quill/dist/vue-quill.snow.css";

const emit = defineEmits(["quiz-created"]);

const quizStore = useQuizStore();
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
		editor.root.innerHTML = quizStore.quizData.instruction; // Load existing data
		editor.on("text-change", () => {
			quizStore.quizData.instruction = editor.root.innerHTML;
		});
	});
});

const createQuiz = () => {
	emit("quiz-created");
};

const cancelQuiz = () => {
	quizStore.quizData.title = "";
	quizStore.quizData.instruction = "";
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
