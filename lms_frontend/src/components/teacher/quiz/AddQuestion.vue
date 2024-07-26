<template>
  <div class="add-question-page">
    <h1 class="page-title">Add Question</h1>
    <div class="question-card">
      <div class="select-type">
        <h3 style="margin: 0">Question</h3>
        <select id="questionType" v-model="questionType">
          <option value="" disabled selected>Select the type of Question</option>
          <option v-for="type in quizStore.questionTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
      </div>
      <div class="question-content">
        <label for="quizDescription">Question Content:</label>
        <div ref="quillEditor" class="quill-editor" style="height: 150px"></div>
        <h3 style="margin-top: 20px; margin-bottom: 10px">Options</h3>
        <div class="scrollable-card">
          <div class="options" v-for="(option, index) in options" :key="index">
            <input type="checkbox" v-model="option.is_correct" />
            <input
              class="option"
              type="text"
              :placeholder="'Option ' + (index + 1)"
              v-model="option.option"
            />
            <font-awesome-icon
              icon="trash-alt"
              @click="removeOption(index)"
              class="delete-icon"
            />
          </div>
          <div class="v-card-actions">
            <button class="add-option" @click="addOption">Add Option</button>
          </div>
        </div>
        <div class="card-actions">
          <button class="cancel-btn" @click="cancel">Cancel</button>
          <button class="next-btn" @click="addQuestion">Add</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useQuizStore } from '@/stores/teacherStore/quizStore';
import Quill from 'quill';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';

library.add(faTrashAlt);

const emit = defineEmits(['questions']);

const quizStore = useQuizStore();
const questionContent = ref('');
const questionType = ref('');
const options = ref([
  { option: '', is_correct: false },
  { option: '', is_correct: false }
]);
const quillEditor = ref(null);

const editorOptions = {
  theme: 'snow',
  modules: {
    toolbar: [
      [{ header: [1, 2, false] }],
      ['bold', 'italic', 'underline'],
      [{ list: 'ordered' }, { list: 'bullet' }],
      [{ align: [] }],
      ['clean']
    ]
  }
};

onMounted(() => {
  nextTick(() => {
    const editor = new Quill(quillEditor.value, editorOptions);
    editor.on('text-change', () => {
      questionContent.value = editor.root.innerHTML;
    });
  });

  quizStore.fetchQuestionTypes();
});

const addQuestion = () => {
  const questionData = {
    question: questionContent.value,
    question_type: questionType.value,
    // question_grade: 0,
    question_options: options.value
  };
  emit('questions', questionData);
  questionContent.value = '';
  questionType.value = '';
  options.value = [
    { option: '', is_correct: false },
    { option: '', is_correct: false }
  ];
};

const cancel = () => {
  emit('questions');
};

const addOption = () => {
  options.value.push({ option: '', is_correct: false });
};

const removeOption = (index) => {
  options.value.splice(index, 1);
};
</script>


<style scoped>
h1 {
	text-align: center;
	font-size: 24px;
	margin-bottom: 20px;
}

.add-question-page {
	display: flex;
	flex-direction: column;
	align-items: center;
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
.delete-icon {
	color: #dc3545;
	font-size: 20px;
	cursor: pointer;
	margin: 5px;
	margin-right: 15px;
	margin-left: 15px;
	position: relative;
	top: -10px;
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
	width: 30%;
	cursor: pointer;
	appearance: none;
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

@media only screen and (max-width: 768px) {
	.question-card {
		width: 90%;
		margin: 10px;
	}
	.scrollable-card {
		height: 60%;
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

.options {
	display: flex;
	align-items: center;
}

.options input[type="checkbox"] {
	width: 5%;
}

.options .option {
	width: 100%;
}

@media only screen and (max-width: 768px) {
	.options .option {
		width: 60%;
	}
}

@media only screen and (max-width: 480px) {
	.options input[type="checkbox"] {
		width: 10%;
	}
	.options .option {
		width: 50%;
	}
}
</style>
