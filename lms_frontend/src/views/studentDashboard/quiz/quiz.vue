<template>
	<div class="container">
		<Header />
		<SubHeader
			:formattedTime="formattedTime"
			:currentQuestion="currentQuestion"
			:prevQuestion="prevQuestion"
			:nextQuestion="nextQuestion"
			:submitAnswers="submitAnswers"
		/>
		<div class="main">
			<Sidebar :isCollapsed="isCollapsed" :toggleQuestionList="toggleQuestionList">
				<QuestionList :questions="questions" :goToQuestion="goToQuestion" />
			</Sidebar>
			<div class="content" :style="{ width: isCollapsed ? 'calc(100% - 40px)' : '80%' }" id="content">
				<QuestionContent :questions="questions" :currentQuestion="currentQuestion" />
				<Options
					:questions="questions"
					:currentQuestion="currentQuestion"
					:markAnswered="markAnswered"
				/>
			</div>
		</div>
		<Footer :nextQuestion="nextQuestion" />
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import Header from "@/components/quiz/quiz/Header.vue";
import SubHeader from "@/components/quiz/quiz/SubHeader.vue";
import Sidebar from "@/components/quiz/quiz/Sidebar.vue";
import QuestionList from "@/components/quiz/quiz/QuestionList.vue";
import QuestionContent from "@/components/quiz/quiz/QuestionContent.vue";
import Footer from "@/components/quiz/quiz/Footer.vue";
import Options from "@/components/quiz/quiz/Options.vue";

const isCollapsed = ref(false);
const currentQuestion = ref(0);
const questions = ref([
	{
		label: "Question 1",
		text: "What is 2 + 2?",
		choices: ["3", "4", "5", "6"],
		checked: false,
		points: 7,
	},
	{
		label: "Question 2",
		text: "What is the capital of France?",
		choices: ["Berlin", "Paris", "Rome", "Madrid"],
		checked: false,
		points: 3,
	},
	{
		label: "Question 3",
		text: "What is the largest ocean?",
		choices: ["Atlantic", "Indian", "Arctic", "Pacific"],
		checked: false,
		points: 6,
	},
	{
		label: "Question 4",
		text: "What is the square root of 16?",
		choices: ["2", "4", "6", "8"],
		checked: false,
		points: 8,
	},
	{
		label: "Question 5",
		text: "What is the chemical symbol for water?",
		choices: ["O2", "H2", "H2O", "CO2"],
		checked: false,
		points: 4,
	},
	{
		label: "Question 6",
		text: "What planet is known as the Red Planet?",
		choices: ["Earth", "Mars", "Jupiter", "Saturn"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 7",
		text: "What is the speed of light?",
		choices: ["300,000 km/s", "150,000 km/s", "75,000 km/s", "30,000 km/s"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 8",
		text: "Who wrote 'Romeo and Juliet'?",
		choices: ["Mark Twain", "William Shakespeare", "Charles Dickens", "Jane Austen"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 9",
		text: "What is the capital of Japan?",
		choices: ["Beijing", "Seoul", "Tokyo", "Bangkok"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 10",
		text: "What is the powerhouse of the cell?",
		choices: ["Nucleus", "Ribosome", "Mitochondria", "Chloroplast"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 11",
		text: "What is the value of Pi?",
		choices: ["2.14", "3.14", "3.15", "4.14"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 12",
		text: "What is the smallest prime number?",
		choices: ["0", "1", "2", "3"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 13",
		text: "What is the freezing point of water?",
		choices: ["0°C", "32°C", "100°C", "-32°C"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 14",
		text: "What gas do plants absorb?",
		choices: ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 15",
		text: "What is the currency of the United States?",
		choices: ["Euro", "Pound", "Yen", "Dollar"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 16",
		text: "Who discovered gravity?",
		choices: ["Galileo", "Newton", "Einstein", "Tesla"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 17",
		text: "What is the capital of Australia?",
		choices: ["Sydney", "Melbourne", "Canberra", "Perth"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 18",
		text: "What is the chemical symbol for gold?",
		choices: ["Au", "Ag", "Pb", "Fe"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 19",
		text: "What is the largest planet in our solar system?",
		choices: ["Earth", "Mars", "Jupiter", "Saturn"],
		checked: false,
		points: 10,
	},
	{
		label: "Question 20",
		text: "What is the speed of sound?",
		choices: ["343 m/s", "299,792 m/s", "400 m/s", "1200 m/s"],
		checked: false,
		points: 10,
	},
]);

const timeLeft = ref(45 * 60 * 60); // 45 hours in seconds

const toggleQuestionList = () => {
	isCollapsed.value = !isCollapsed.value;
};

const nextQuestion = () => {
	if (currentQuestion.value < questions.value.length - 1) {
		currentQuestion.value++;
	}
};

const prevQuestion = () => {
	if (currentQuestion.value > 0) {
		currentQuestion.value--;
	}
};

const goToQuestion = (index) => {
	currentQuestion.value = index;
};

const markAnswered = () => {
	questions.value[currentQuestion.value].checked = true;
};

const submitAnswers = () => {
	alert("Answers submitted!");
};

const handleResize = () => {
	if (window.innerWidth <= 768) {
		isCollapsed.value = true;
	} else {
		isCollapsed.value = false;
	}
};

const startTimer = () => {
	const timerInterval = setInterval(() => {
		if (timeLeft.value > 0) {
			timeLeft.value--;
		} else {
			clearInterval(timerInterval);
			submitAnswers();
		}
	}, 1000);
};

const formattedTime = computed(() => {
	const hours = Math.floor(timeLeft.value / 3600);
	const minutes = Math.floor((timeLeft.value % 3600) / 60);
	const seconds = timeLeft.value % 60;
	return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds
		.toString()
		.padStart(2, "0")}`;
});

onMounted(() => {
	window.addEventListener("resize", handleResize);
	handleResize();
	startTimer();
});

onBeforeUnmount(() => {
	window.removeEventListener("resize", handleResize);
});
</script>

<style scoped>
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}
html,
body {
	height: 100%;
	margin: 0;
}
.container {
	display: flex;
	flex-direction: column;
	min-height: 100vh;
}
.header,
.sub-header,
.footer {
	flex-shrink: 0;
}
.main {
	display: flex;
	flex: 1;
	overflow: hidden;
}
.content {
	display: flex;
	flex-direction: column;
	flex: 1;
	overflow: hidden;
}
@media (max-width: 768px) {
	.content {
		width: calc(100% - 40px);
	}
	.sidebar {
		width: 40px;
		overflow: visible;
	}
}
</style>
