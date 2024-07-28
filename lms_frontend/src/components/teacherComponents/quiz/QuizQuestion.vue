<template>
	<div class="main-card">
		<div class="select-button">
			<button class="question-type" @click="goToAddQuestion">ADD QUESTION</button>
			<button class="question-type" @click="goToReuseQuestion">REUSE QUESTION</button>
		</div>
		<div class="scrollable-card">
			<div class="summary-container">
				<div class="summary-right">
					<div class="summary-item">
						<span>Number of Questions: {{ allQuestions.length }}</span>
					</div>
					<div class="summary-item">
						<span>Total Grades: {{ totalGrades }}</span>
					</div>
				</div>
				<div class="summary-left">
					<label class="grade-word">Grade:</label>
					<input
						type="number"
						placeholder="Enter Grade"
						v-model="newGrade"
						class="new-grade-input"
					/>
					<button class="update-grade-button" @click="updateAllGrades">Update</button>
				</div>
			</div>
			<div v-if="allQuestions.length > 0">
				<div class="question" v-for="(question, index) in allQuestions" :key="index">
					<div class="question-grade">
						<h2>Question {{ index + 1 }}</h2>
						<input
							v-if="question"
							type="number"
							placeholder="Enter the Grade"
							class="grade"
							v-model="question.question_grade"
							:min="0"
						/>
						<span
							v-if="
								errors &&
								errors.questions &&
								errors.questions.find((e) => e.index === index) &&
								errors.questions.find((e) => e.index === index).errors
									.question_grade
							"
							class="error-message"
						>
							{{
								errors.questions.find((e) => e.index === index).errors
									.question_grade
							}}
						</span>
					</div>
					<p v-if="question && question.question" v-html="question.question"></p>
					<ul v-if="question && question.question_options" class="options-list">
						<li
							v-for="(option, optIndex) in question.question_options"
							:key="optIndex"
							:class="{
								selected: selectedAnswers[index] === optIndex,
								correct: option.is_correct,
							}"
						>
							<label class="option-label">
								<input
									:type="
										question.question_type === 'Multiple Choice'
											? 'radio'
											: 'checkbox'
									"
									:name="'question-' + index"
									:v-model="selectedAnswers[index]"
									:value="optIndex"
									class="option-input"
								/>
								<span class="option-text">{{ option.option }}</span>
							</label>
						</li>
					</ul>
					<div class="delete-button-container">
						<button class="delete-button" @click="deleteQuestion(index)">
							Delete
						</button>
					</div>
					<div
						class="error-message"
						v-if="
							errors &&
							errors.questions &&
							errors.questions.find((e) => e.index === index) &&
							errors.questions.find((e) => e.index === index).errors
						"
					>
						<div
							v-if="errors.questions.find((e) => e.index === index).errors.question"
						>
							{{ errors.questions.find((e) => e.index === index).errors.question }}
						</div>
						<div
							v-if="
								errors.questions.find((e) => e.index === index).errors
									.question_type
							"
						>
							{{
								errors.questions.find((e) => e.index === index).errors
									.question_type
							}}
						</div>
						<div
							v-if="
								errors.questions.find((e) => e.index === index).errors
									.question_options
							"
						>
							{{
								errors.questions.find((e) => e.index === index).errors
									.question_options
							}}
						</div>
					</div>
				</div>
			</div>
			<div
				class="error-message"
				v-if="
					errors &&
					errors.questions &&
					errors.questions.length > 0 &&
					errors.questions[0].question
				"
			>
				{{ errors.questions[0].question }}
			</div>
		</div>
		<div class="card-actions">
			<button class="prev-btn" @click="previousPage">Previous</button>
			<button class="next-btn" @click="nextPage">Next</button>
		</div>
	</div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed } from "vue";

const props = defineProps({
	questions: {
		type: Array,
		required: true,
		default: () => [],
	},
	errors: {
		type: Object,
		default: () => ({}),
	},
});
const emit = defineEmits([
	"go-back",
	"settings",
	"addQuestion",
	"reuseQuestion",
	"deleteQuestion",
	"on-add-question",
	"on-add-questions",
]);

const selectedAnswers = ref([]);
const additionalQuestions = ref([]);
const newGrade = ref(0);

const isValidQuestion = (question) => {
	return (
		question &&
		question.question &&
		question.question_options &&
		question.question_options.length > 0
	);
};

const allQuestions = computed(() => {
	const validQuestions = props.questions.filter(isValidQuestion);
	const validAdditionalQuestions = additionalQuestions.value.filter(isValidQuestion);
	return [...validQuestions, ...validAdditionalQuestions];
});

const totalGrades = computed(() => {
	return allQuestions.value.reduce((total, question) => {
		const grade = question?.question_grade ?? 0;
		return total + (parseInt(grade) || 0);
	}, 0);
});

const goToAddQuestion = () => {
	emit("addQuestion");
};

const goToReuseQuestion = () => {
	emit("reuseQuestion");
};

const nextPage = () => {
	emit("settings", allQuestions.value);
};

const previousPage = () => {
	emit("go-back");
};

const selectAnswer = (questionIndex, optionIndex) => {
	selectedAnswers.value[questionIndex] = optionIndex;
};

const deleteQuestion = (index) => {
	if (index < props.questions.length) {
		const updatedQuestions = [...props.questions];
		updatedQuestions.splice(index, 1);
		emit("deleteQuestion", updatedQuestions);
	} else {
		const additionalIndex = index - props.questions.length;
		additionalQuestions.value.splice(additionalIndex, 1);
	}
};

const updateAllGrades = () => {
	allQuestions.value.forEach((question) => {
		question.question_grade = newGrade.value;
	});
};

const addQuestions = (newQuestions) => {
	additionalQuestions.value.push(...newQuestions);
};

const onAddQuestion = (question) => {
	if (isValidQuestion(question)) {
		additionalQuestions.value.push(question);
	}
};

const onAddQuestions = (questions) => {
	const validQuestions = questions.filter(isValidQuestion);
	additionalQuestions.value.push(...validQuestions);
};

emit("on-add-question", onAddQuestion);
emit("on-add-questions", onAddQuestions);
</script>

<style scoped>
body {
	font-family: Arial, sans-serif;
	background-color: #f9f9f9;
	margin: 0;
	padding: 0;
}

.summary-container {
	display: flex;
	justify-content: space-between;
	margin: 20px 0;
	padding: 0 20px;
	align-items: center;
}

.summary-right {
	display: flex;
	flex-direction: column;
	align-items: flex-end;
}

.summary-left {
	display: flex;
	align-items: center;
}

.summary-item {
	font-size: 18px;
	font-weight: bold;
	margin-bottom: 5px;
}
.grade-word {
	margin-bottom: 28px;
}
.new-grade-input {
	width: 80px;
	padding: 5px;
	border: 1px solid #ddd;
	border-radius: 5px;
	font-size: 14px;
	margin-left: 10px;
	margin-right: 10px;
}

.update-grade-button {
	background-color: #0584ae;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	padding: 5px 10px;
	font-size: 14px;
	margin-bottom: 21px;
	width: 80px;
	text-align: center;
}

.update-grade-button:hover {
	opacity: 0.9;
}

.select-button {
	display: flex;
	justify-content: space-between;
	margin-top: 0;
	margin-bottom: 0px;
	margin-right: 23px;
}

.question-type,
.reuse-question {
	background-color: #0584ae;
	color: white;
	margin-top: 0px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	width: 35%;
}

button:hover {
	opacity: 0.9;
}

.scrollable-card {
	background-color: #f4f4f4;
	padding-left: 20px;
	padding-right: 20px;
	width: 96%;
	border: 1px solid #ddd;
	height: calc(78vh - 80px);
	overflow-y: auto;
	border-radius: 10px;
}

.question {
	background-color: white;
	padding: 20px;
	border: 1px solid #ddd;
	border-radius: 10px;
	margin-bottom: 20px;
	position: relative;
}

.question-grade {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 10px;
}

.question-grade h2 {
	margin: 0;
	font-size: 1.2rem;
}

.grade {
	width: 130px;
	padding: 5px;
	border: 1px solid #ccc;
	border-radius: 5px;
	font-size: 0.9rem;
}

.question p {
	font-size: 1rem;
}

.options-list {
	list-style-type: none;
	padding: 0;
	margin: 5px 0 0 0;
	font-size: 0.9rem;
}

.options-list li {
	margin: -20px 0;
	padding: 5px;
	display: flex;
	align-items: center;
	justify-content: flex-start;
}

.options-list li.selected {
	background-color: #d3e8ff;
	border-radius: 5px;
}

.options-list li.correct .option-text {
	color: green;
	font-weight: bold;
}

.option-label {
	display: flex;
	align-items: center;
}
.options-list li .option-text {
	white-space: nowrap;
	color: inherit;
}

.option-input {
	margin-right: 10px;
	transform: scale(1.2);
	position: relative;
	top: 8px;
}

.delete-button-container {
	display: flex;
	justify-content: flex-end;
	margin-top: 10px;
}

.delete-button {
	background-color: #c82333;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	padding: 5px 10px;
	width: 100px;
	text-align: center;
}

.delete-button:hover {
	opacity: 0.9;
}

.card-actions {
	display: flex;
	justify-content: flex-end;
	margin-top: 20px;
	margin-right: 70px;
}

.card-actions button {
	width: 15%;
	font-size: 14px;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	background-color: #0584ae;
	color: white;
}

.card-actions button:hover {
	opacity: 0.9;
}

.card-actions .prev-btn {
	margin-right: 10px;
}

.error-message {
	color: red;
	font-size: 14px;
	margin-top: 10px;
	text-align: center;
}
</style>
