<template>
	<div class="reuse-question-page">
		<h1 class="page-title">Reuse Question</h1>
		<div class="question-card">
			<div class="scrollable-card">
				<div class="question" v-for="(question, index) in questions" :key="index">
					<div class="check">
						<input
							class="checkbox"
							type="checkbox"
							v-model="selectedQuestions"
							:value="question"
						/>
						<p v-html="question.question" class="question-text"></p>
					</div>
					<ul class="options-list">
						<li
							v-for="(option, idx) in question.question_options"
							:key="idx"
							class="option-item"
							:class="{ correct: option.is_correct }"
						>
							<label class="option-label">
								<input
									:type="
										question.question_type === 'Multiple Answer'
											? 'checkbox'
											: 'radio'
									"
									:name="'option-' + index"
									:id="'option-' + index + '-' + idx"
									class="option-input"
									:checked="option.is_correct"
									disabled
								/>
								<span class="option-text">{{ option.option }}</span>
							</label>
						</li>
					</ul>
				</div>
			</div>
			<div class="card-actions">
				<button class="cancel-btn" @click="cancel">Cancel</button>
				<button class="next-btn" @click="reuseQuestions">Reuse</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useQuizStore } from "@/stores/teacherStore/quizStore";

const selectedQuestions = ref([]);
const store = useQuizStore();
const emit = defineEmits(["questions", "cancel"]);

const questions = computed(() => store.questions);

onMounted(async () => {
	await store.fetchQuestionsByCourse("00", "ACAD-FM-00001");
});

const reuseQuestions = () => {
	emit("questions", selectedQuestions.value);
};

const cancel = () => {
	emit("cancel");
};
</script>

<style scoped>
/* أضف تنسيقات CSS الخاصة بـ QuestionList هنا */
.grade {
	width: 130px; /* تعديل العرض ليكون متناسقاً */
	padding: 5px;
	border: 1px solid #ccc;
	border-radius: 5px;
	font-size: 0.9rem; /* تصغير حجم الخط */
}
.add-question {
	flex: 1;
	padding: 10px;
	border: 1px solid #ddd;
	border-radius: 5px;
	margin-right: 20px;
	margin-bottom: 10px;
}
h1 {
	text-align: center;
	margin-bottom: 15px;
	font-size: 24px;
}

.reuse-question {
	background-color: #6ba7e6;
	color: white;
	border: none;
	padding: 10px 20px;
	margin-left: 200px;
	border-radius: 5px;
	margin-bottom: 20px;
	cursor: pointer;
}

.big-card {
	background-color: white;
	border-radius: 10px;
	padding-bottom: 20px;
}

.scrollable-card {
	background-color: #f4f4f4;
	padding: 20px;
	width: 96%;
	border: 1px solid #ddd;
	height: calc(80vh - 160px); /* تعديل ارتفاع البطاقة بحيث تكون الأزرار مرئية */
	overflow-y: auto;
	border-radius: 10px;
}

.question-grade {
	display: flex;
	justify-content: space-between;
}
.select-button {
	display: flex;
	justify-content: space-between;
}

.grade {
	size: 5rem;
	margin-right: 10px;
}

.profile-icon img {
	width: 40px;
	height: 40px;
	border-radius: 50%;
}

.question-container {
	margin-top: 2px;
}

.question {
	background-color: white;
	padding: 20px;
	border: 1px solid #ddd;
	border-radius: 10px;
	margin-bottom: 10px;
}

.question h2 {
	margin-top: 0;
}

.question ul {
	list-style-type: none;
	padding: 0;
}

.options-list {
	padding-left: 0; /* إزالة الحشوة الافتراضية لقائمة ul */
	display: block; /* تعديل العرض */
	gap: px; /* مسافة بين العناصر */
}

.options-list li {
	margin: 5px 0; /* تقليل الهامش بين العناصر */
	display: flex;
	align-items: center; /* لضمان أن الخيارات والنصوص تكون في نفس السطر */
	justify-content: flex-start; /* محاذاة العناصر إلى اليسار */
}

.options-list li .option-input {
	margin-right: 10px; /* مسافة بين الراديو والنص */
	transform: scale(1.2); /* تعديل حجم الراديو ليكون مناسب */
	position: relative;
	top: 8px; /* رفع الراديو قليلاً */
}

.options-list li .option-label {
	display: flex;
	align-items: center; /* لضمان أن الخيارات والنصوص تكون في نفس السطر */
}

.options-list li .option-text {
	white-space: nowrap; /* منع النص من الالتفاف */
	color: inherit; /* للحفاظ على لون النص الأصلي */
}

.question ul li a {
	color: #007bff;
	text-decoration: none;
}

.grade {
	background-color: #f4f7f9;
	padding: 5px 10px;
	border-radius: 5px;
	display: inline-block;
	margin-top: 10px;
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
	font-size: 16px;
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

select {
	padding: 10px;
	border: 1px solid #ddd;
	border-radius: 5px;
	margin-bottom: 20px;
	font-size: 16px;
	background-color: #fff;
	color: #333;
	width: 50%; /* اجعل العرض 100% للتوافق مع الشاشات الصغيرة */
	cursor: pointer;
	appearance: none; /* لإزالة شكل السهم الافتراضي في بعض المتصفحات */
}

select:focus {
	border-color: #4091e8;
	outline: none;
	box-shadow: 0 0 5px rgba(62, 148, 240, 0.5);
}
.question-type {
	background-color: #6ba7e6;
	color: white;
	border: none;
	padding: 10px 20px;
	border-radius: 5px;
	margin-bottom: 20px;
	cursor: pointer;
	width: 20%;
}

/* استعلامات الوسائط للتكيف مع أحجام الشاشات المختلفة */
@media (max-width: 768px) {
	.big-card {
		width: 100%;
	}

	.reuse-question {
		margin-left: 0;
		width: 100%;
	}

	.scrollable-card {
		height: calc(70vh - 160px);
	}

	.options-list li .option-input {
		margin-right: 5px;
		transform: scale(1.1);
	}

	.card-actions {
		flex-direction: column;
		align-items: stretch;
	}

	.card-actions button {
		width: 100%;
		margin: 10px 0;
	}
}

@media (max-width: 576px) {
	.big-card {
		padding: 10px;
	}

	.reuse-question {
		width: 100%;
		padding: 10px 0;
	}

	.scrollable-card {
		height: calc(60vh - 160px);
	}

	.question {
		padding: 10px;
	}

	.options-list li .option-input {
		margin-right: 5px;
		transform: scale(1.1);
	}

	.card-actions {
		flex-direction: column;
		align-items: stretch;
	}

	.card-actions button {
		width: 100%;
		margin: 10px 0;
	}
}

/*reuse*/
.check {
	display: flex;
	align-items: center; /* لجعل العناصر تتماشى أفقياً */
}
.checkbox {
	width: 12px;
	height: 12px;
	transform: scale(1.5);
	margin-right: 14px;
	margin-top: 0; /* إزالة الهوامش العلوية */
}
.question-text {
	margin: 0; /* إزالة الهوامش العلوية والسفلية */
	position: relative;
	top: -10px; /* رفع النص قليلاً */
}

/* إضافة نمط للنص الصحيح */
.correct .option-text {
	color: green;
	font-weight: bold;
}
</style>
