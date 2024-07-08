<template>
	<div class="main-card">
		<div class="select-button">
			<button class="question-type" @click="goToAddQuestion">ADD QUESTION</button>
			<button class="question-type" @click="goToReuseQuestion">REUSE QUESTION</button>
		</div>
		<div class="scrollable-card">
			<div class="question" v-for="(question, index) in questions" :key="index">
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
				<ul>
					<li
						v-for="(option, optIndex) in question.question_options"
						:key="optIndex"
						:class="{ selected: selectedAnswers[index] === optIndex }"
						@click="selectAnswer(index, optIndex)"
					>
						{{ option.option }}
					</li>
				</ul>
			</div>
		</div>
		<div class="card-actions">
			<button class="prev-btn" @click="previousPage">Previous</button>
			<button class="next-btn" @click="nextPage">Next</button>
		</div>
	</div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from "vue";

const props = defineProps({
	questions: {
		type: Array,
		required: true,
	},
});
const emit = defineEmits(["go-back", "settings", "addQuestion", "reuseQuestion"]);

const selectedAnswers = ref([]);

const goToAddQuestion = () => {
	emit("addQuestion");
};

const goToReuseQuestion = () => {
	emit("reuseQuestion");
};

const nextPage = () => {
	emit("settings", props.questions);
};

const previousPage = () => {
	emit("go-back");
};

const selectAnswer = (questionIndex, optionIndex) => {
	selectedAnswers.value[questionIndex] = optionIndex;
};
</script>

<style scoped>
/* التصميم العام */
body {
	font-family: Arial, sans-serif;
	background-color: #f9f9f9;
	margin: 0;
	padding: 0;
}

/* زر الإضافة وإعادة الاستخدام */
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
	width: 35%; /* تعديل العرض ليكون مرناً */
}
button:hover {
	opacity: 0.9;
}
/* بطاقة التمرير */
.scrollable-card {
	background-color: #f4f4f4;
	padding-left: 20px;
	padding-right: 20px;
	padding-top: 20px;
	width: 96%;
	border: 1px solid #ddd;
	height: calc(78vh - 80px); /* اجعل البطاقة تشغل ارتفاع الشاشة بالكامل ناقص الأزرار */
	overflow-y: auto;
	border-radius: 10px;
}

/* أسئلة الكويز */
.question {
	background-color: white;
	padding: 20px;
	border: 1px solid #ddd;
	border-radius: 10px;
	margin-bottom: 20px;
}

.question-grade {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 10px;
}

.question-grade h2 {
	margin: 0;
	font-size: 1.2rem; /* تصغير حجم الخط */
}

.grade {
	width: 130px; /* تعديل العرض ليكون متناسقاً */
	padding: 5px;
	border: 1px solid #ccc;
	border-radius: 5px;
	font-size: 0.9rem; /* تصغير حجم الخط */
}

.question p {
	font-size: 1rem; /* تصغير حجم النص */
}

.question ul {
	list-style-type: none;
	padding: 0;
	margin: 10px 0 0 0;
	font-size: 0.9rem; /* تصغير حجم النص */
}

.question ul li {
	margin: 5px 0;
	padding: 5px;
	cursor: pointer;
}

.question ul li.selected {
	background-color: #d3e8ff;
	border-radius: 5px;
}

/* أزرار الإجراءات */
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
	background-color: #0584ae; /* تغيير اللون */
	color: white; /* تغيير لون النص إلى الأبيض */
}
.card-actions button:hover {
	opacity: 0.9; /* تغيير اللون */
}

.card-actions .prev-btn {
	margin-right: 10px;
}

/* استجابة التصميم للشاشات الصغيرة */
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
		height: calc(100vh - 100px); /* تعديل الارتفاع للشاشات الصغيرة */
		padding: 10px;
	}
}
</style>
