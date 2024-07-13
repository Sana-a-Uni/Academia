<template>
	<div class="datetime-picker" ref="pickerContainer">
		<input
			type="text"
			:value="formattedDatetime"
			@focus="showPicker = true"
			@input="updateDatetime($event.target.value)"
			placeholder="Enter datetime (e.g., 2023-07-08 12:30)"
			class="input-field"
		/>
		<div v-if="showPicker" class="datetime-fields">
			<input type="date" v-model="date" @input="updateFormattedDatetime" class="input-field-small" />
			<input type="time" v-model="time" @input="updateFormattedDatetime" class="input-field-small" />
		</div>
	</div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";

const props = defineProps({
	modelValue: {
		type: String,
		default: "",
	},
});

const emit = defineEmits(["update:modelValue"]);

const showPicker = ref(false);
const date = ref("");
const time = ref("");
const formattedDatetime = ref("");
const pickerContainer = ref(null);

const parseDatetime = (datetime) => {
	const [d, t] = datetime.split(" ");
	date.value = d || "";
	time.value = t || "";
	updateFormattedDatetime();
};

const updateFormattedDatetime = () => {
	formattedDatetime.value = `${date.value} ${time.value}`.trim();
	emit("update:modelValue", formattedDatetime.value);
};

const updateDatetime = (value) => {
	parseDatetime(value);
};

const handleClickOutside = (event) => {
	if (pickerContainer.value && !pickerContainer.value.contains(event.target)) {
		showPicker.value = false;
	}
};

onMounted(() => {
	document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
	document.removeEventListener("click", handleClickOutside);
});

watch(
	() => props.modelValue,
	(newVal) => {
		parseDatetime(newVal);
	},
	{ immediate: true }
);
</script>

<style scoped>
.datetime-picker {
	position: relative;
}

.datetime-fields {
	position: absolute;
	background: white;
	border: 1px solid #ccc;
	padding: 10px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	display: flex;
	gap: 5px;
	margin-top: 5px;
}

.input-field {
	width: 200%;
	padding: 8px;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-sizing: border-box;
	font-size: 12px;
}

.input-field-small {
	width: 150px;
	padding: 5px;
	border: 1px solid #ccc;
	border-radius: 5px;
}
</style>
