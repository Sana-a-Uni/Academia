<template>
  <div class="big-card">
    <h1>Reuse Question</h1>
    <div class="scrollable-card">
      <div class="question" v-for="(question, index) in questions" :key="index">
        <div class="question-grade">
          <div class="check">
            <input
              style="
                width: 12px;
                height: 12px;
                transform: scale(1.5);
                margin-right: 14px;
                margin-top: 17px;
              "
              type="checkbox"
            />
            <p>{{ question.content }}</p>
          </div>
        </div>
        
        <ul style="margin-left:10px; margin-top:0">
          <li v-for="(option, idx) in question.options" :key="idx">
            {{ option }}
          </li>
        </ul>
      </div>
      <div class="card-actions">
        <button class="cancel-btn" @click="navigateTo('questionlist')">
          Cancel
        </button>
        <button class="next-btn" @click="navigateTo('questionlist')">
          Reuse
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      questions: [
        {
          title: "Question1",
          content: "Here is the content of question",
          options: ["Option 1", "Option 2", "Option 3"],
        },
        {
          title: "Question2",
          content: "Here is the content of question",
          options: ["Option 1", "Option 2", "Option 3"],
        },
        {
          title: "Question3",
          content: "Here is the content of question",
          options: ["Option 1", "Option 2", "Option 3"],
        },
      ],
    };
  },
  methods: {
    navigateTo(page) {
      this.$router.push(`/${page}`);
    },
  },
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
  width:96%;
  border: 1px solid #ddd;
  height: calc(
    80vh - 80px
  ); /* اجعل البطاقة تشغل ارتفاع الشاشة بالكامل ناقص الأزرار */
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
  margin-bottom: 20px;
}

.question h2 {
  margin-top: 0;
}

.question ul {
  list-style-type: none;
  padding: 0;
}

.question ul li {
  margin: 10px 0;
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
  opacity: 0.9
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
  .app-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .add-question,
  .reuse-question {
    width: 100%;
    margin: 10px 0;
  }

  .question-grade {
    flex-direction: column;
    align-items: flex-start;
  }

  .question-grade h2,
  .question-grade .grade {
    margin-right: 0;
  }
}

@media (max-width: 576px) {
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
  justify-content: space-between;
}
</style>
