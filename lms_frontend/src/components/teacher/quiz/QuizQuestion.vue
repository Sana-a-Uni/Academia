<template>
	<div class="main-card">
		<div class="select-button">
			<button class="question-type" @click="goToAddQuestion">ADD QUESTION</button>
			<button class="question-type" @click="goToReuseQuestion">REUSE QUESTION</button>
		</div>
		<div class="scrollable-card">
			<div class="question" v-for="(question, index) in allQuestions" :key="index">
				<div class="question-grade">
					<h2>Question {{ index + 1 }}</h2>
					<input
						type="number"
						placeholder="Enter the Grade"
						class="grade"
						v-model="question.question_grade"
					/>
				</div>
				<p v-html="question.question"></p>
				<ul class="options-list">
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
					<button class="delete-button" @click="deleteQuestion(index)">Delete</button>
				</div>
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
		default: () => [], // إضافة قيمة افتراضية
	},
});
const emit = defineEmits([
	"go-back",
	"settings",
	"addQuestion",
	"reuseQuestion",
	"deleteQuestion",
]);

const selectedAnswers = ref([]);
const additionalQuestions = ref([]);

const allQuestions = computed(() => {
	return props.questions && Array.isArray(props.questions)
		? [...props.questions, ...additionalQuestions.value]
		: [...additionalQuestions.value];
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
		props.questions.splice(index, 1);
	} else {
		additionalQuestions.value.splice(index - props.questions.length, 1);
	}
	emit("deleteQuestion", index);
};

const addQuestions = (newQuestions) => {
	additionalQuestions.value.push(...newQuestions);
};

// استقبال الأسئلة المضافة
const onAddQuestion = (question) => {
	additionalQuestions.value.push(question);
};

const onAddQuestions = (questions) => {
	additionalQuestions.value.push(...questions);
};

// الاستماع للأسئلة المضافة من صفحة إعادة الاستخدام
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
	padding-top: 20px;
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
	align-items: center; /* لضمان أن الخيارات والنصوص تكون في نفس السطر */
	justify-content: flex-start; /* محاذاة العناصر إلى اليسار */
}

.options-list li.selected {
	background-color: #d3e8ff;
	border-radius: 5px;
}

.options-list li.correct .option-text {
	color: green; /* تغيير لون النص للخيار الصحيح */
	font-weight: bold;
}

.option-label {
	display: flex;
	align-items: center;
}
.options-list li .option-text {
	white-space: nowrap; /* منع النص من الالتفاف */
	color: inherit; /* للحفاظ على لون النص الأصلي */
}

.option-input {
	margin-right: 10px;
	transform: scale(1.2); /* تكبير حجم الراديو أو الشيكبوكس */
	position: relative;
	top: 8px; /* رفع الراديو أو الشيكبوكس قليلاً */
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

@media (max-width: 768px) {
	.select-button {
		flex-direction: column;
	}

	.question-type,
	.reuse-question {
		width: 100%;
		margin-bottom: 10px;
	}

	.question-grade {
		flex-direction: column;
		align-items: flex-start;
	}

	.card-actions {
		flex-direction: column;
		align-items: stretch;
	}

	.card-actions button {
		width: 90%;
		margin: 10px 0;
	}
}

@media (max-width: 576px) {
	.scrollable-card {
		height: calc(100vh - 100px);
		padding: 10px;
	}
}
</style>
