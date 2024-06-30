<template>
	<h1>Add Question</h1>
	<div class="question-card">
		<div class="select-type">
			<h3 style="margin: 0">Question 1</h3>
			<select id="questionType" @change="updateQuestionType">
				<option value="" disabled selected>Select the type of Question</option>
				<option value="handleCheckboxChange">One Answer</option>
				<option value="multipleAnswers">Multiple Answers</option>
			</select>
		</div>
		<div class="question-content">
			<label for="quizDescription">Question Content:</label>
			<QuillEditor
				v-model="quizDescription"
				:options="editorOptions"
				class="quill-editor"
				style="height: 150px"
			></QuillEditor>

			<h3 style="margin-top: 20px; margin-bottom: 10px">Options</h3>
			<div class="scrollable-card">
				<div
					class="options"
					v-for="(option, index) in options"
					:key="index"
					:id="'option' + (index + 1)"
				>
					<input type="checkbox" @change="handleCheckboxChange($event, index)" />
					<input class="option" type="text" :placeholder="'Option ' + (index + 1)" />
					<i class="mdi mdi-delete" @click="removeOption(index)"></i>
				</div>
				<div class="v-card-actions">
					<button class="add-option" @click="addOption">Add Option</button>
				</div>
			</div>
			<div class="card-actions">
				<button class="cancel-btn" @click="addQuestion">Cancel</button>
				<button class="next-btn" @click="cancel">Add</button>
			</div>
		</div>
	</div>
</template>

<script>
import { ref, computed, defineProps, defineEmits } from "vue";

const emit = defineEmits(["questions", "questions"]);

const quizTitle = ref("");
const quizDescription = ref("");

const addQuestion = () => {
	// Emit event to parent to change the view to QuizInformation
	emit("questions");
};

const cancel = () => {
	// Emit event to parent to change the view to QuizInformation
	emit("questions");
};

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
export default {
	data() {
		return {
			currentQuestionType: "",
			options: [1, 2],
			textAlignment: "left",
			fontStyles: [],
		};
	},
	methods: {
		updateQuestionType() {
			this.currentQuestionType = document.getElementById("questionType").value;
		},
		handleCheckboxChange(event, index) {
			if (this.currentQuestionType === "handleCheckboxChange") {
				this.options.forEach((_, i) => {
					if (i !== index) {
						document
							.getElementById(`option${i + 1}`)
							.querySelector('input[type="checkbox"]').checked = false;
					}
				});
			}
		},

		addOption() {
			this.options.push(this.options.length + 1);
		},
		removeOption(index) {
			this.options.splice(index, 1);
		},
		cancel() {
			// Cancel logic
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.options.forEach((_, index) => {
				document
					.getElementById(`option${index + 1}`)
					.querySelector('input[type="checkbox"]').onchange = (event) => {
					if (this.currentQuestionType === "handleCheckboxChange") {
						this.handleCheckboxChange(event, index);
					}
				};
			});
		});
	},
};
</script>

<style scoped>
/* Include your styles here */

h1 {
	text-align: center;
	font-size: 24px;
}
.question-card {
	width: 97%;
	padding-left: 20px;
	padding-right: 20px;
	padding-bottom: 20px;
	background-color: white;
	margin-right: 20px;
	border-radius: 10px;
}
.question-card h3 {
	margin-bottom: 10px;
}
.question-content {
	margin: 0;
}
.scrollable-card {
	background-color: #f4f4f4;
	padding: 20px;
	height: 80%;
	width: 96.5%;
	border-radius: 10px;
	margin-left: 0px;
}
.quill-editor {
	height: 200px;
	margin-right: 10px;
	margin-bottom: 20px;
}
.option {
	padding: 15px;
	border: 1px solid #ddd;
	margin-bottom: 20px;
	border-radius: 5px;
	font-size: 16px;
	background-color: #fff;
	color: #333;
	width: 80%;
	cursor: pointer;
	appearance: none;
}
.card-actions {
	display: flex;
	justify-content: flex-end;
	margin: 20px;
}
.card-actions button {
	padding: 10px 20px;
	margin-top: 20px;
	margin-left: 5px;
	margin-right: 5px;
	font-size: 14px;
	border: none;
	border-radius: 4px;
	cursor: pointer;
}
.card-actions .next-btn {
	background-color: #0584ae;
}
.card-actions .next-btn:hover {
	opacity: 0.9;
}
.card-actions .cancel-btn {
	background-color: #c82333;
}
.card-actions .cancel-btn:hover {
	background-color: #dc3545;
}
.v-card-actions {
	display: flex;
	justify-content: flex-end;
	margin-top: 10px;
}

.add-option {
	background-color: #0584ae;
	padding: 10px;
	border-radius: 10px;
	margin-right: 0;
}
.add-option:hover {
	opacity: 0.9;
}

.options .mdi-delete {
	color: red;
	font-size: 24px;
	cursor: pointer;
	margin-bottom: 20px;
}
.options input[type="checkbox"] {
	width: 15px;
	height: 15px;
	transform: scale(1.5);
	margin-right: 10px;
}
select {
	padding: 10px;
	border: 1px solid #ddd;
	border-radius: 5px;
	margin-right: 20px;
	font-size: 16px;
	background-color: #fff;
	color: #333;
	width: 30%; /* اجعل العرض 100% للتوافق مع الشاشات الصغيرة */
	cursor: pointer;
	appearance: none; /* لإزالة شكل السهم الافتراضي في بعض المتصفحات */
}

select:focus {
	border-color: #4091e8;
	outline: none;
	box-shadow: 0 0 5px rgba(62, 148, 240, 0.5);
}
.select-type {
	display: flex;
	justify-content: space-between;
}

/* Default styles */
@media only screen and (max-width: 768px) {
	/* Styles for screens up to 768px width */
	.question-card {
		width: 90%; /* Adjust width for smaller screens */
		margin: 10px; /* Adjust margin for smaller screens */
	}
	.scrollable-card {
		height: 60%; /* Adjust height for smaller screens */
	}
}

@media (max-width: 600px) {
	.container {
		padding: 10px;
	}

	.next-btn,
	cancel-btn {
		padding: 8px;
		font-size: 12px;
		width: 25%;
	}
}

/* Default styles */
.options {
	display: flex;
	align-items: center;
}

.options input[type="checkbox"] {
	width: 5%; /* Adjust width for checkbox */
}

.options .option {
	width: 100%; /* Adjust width for input */
}

.options .mdi-delete {
	width: 5%; /* Adjust width for delete icon */
	margin-left: 20px;
}

@media only screen and (max-width: 768px) {
	/* Styles for screens up to 768px width */
	.options .option {
		width: 60%; /* Adjust width for smaller screens */
	}
}

@media only screen and (max-width: 480px) {
	/* Styles for screens up to 480px width */
	.options input[type="checkbox"] {
		width: 10%; /* Adjust width for smaller screens */
	}
	.options .option {
		width: 50%; /* Adjust width for smaller screens */
	}
	.options .mdi-delete {
		width: 10%; /* Adjust width for smaller screens */
	}
}
</style>
