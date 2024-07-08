<template>
	<div class="duration-input" ref="durationContainer">
		<input
			type="text"
			:value="formattedDuration"
			@focus="showFields = true"
			@input="updateDuration($event.target.value)"
			placeholder="Enter duration (e.g., 4d 5h 7m 7s)"
			class="input-field"
		/>
		<div v-if="showFields" class="duration-fields">
			<div class="inline-fields">
				<div class="field-container">
					<input
						type="number"
						placeholder="Days"
						class="input-field-small"
						v-model.number="days"
						@input="updateFormattedDuration"
					/>
					<span>days</span>
				</div>
				<div class="field-container">
					<input
						type="number"
						placeholder="Hours"
						class="input-field-small"
						v-model.number="hours"
						@input="updateFormattedDuration"
					/>
					<span>hours</span>
				</div>
				<div class="field-container">
					<input
						type="number"
						placeholder="Minutes"
						class="input-field-small"
						v-model.number="minutes"
						@input="updateFormattedDuration"
					/>
					<span>minutes</span>
				</div>
				<div class="field-container">
					<input
						type="number"
						placeholder="Seconds"
						class="input-field-small"
						v-model.number="seconds"
						@input="updateFormattedDuration"
					/>
					<span>seconds</span>
				</div>
			</div>
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

const emit = defineEmits(["update:modelValue", "update:seconds"]);

const showFields = ref(false);
const days = ref(0);
const hours = ref(0);
const minutes = ref(0);
const seconds = ref(0);
const formattedDuration = ref("");
const durationContainer = ref(null);

const parseDuration = (duration) => {
	const regex = /(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*(\d+s)?/;
	const matches = duration.match(regex);
	if (matches) {
		days.value = matches[1] ? parseInt(matches[1]) : 0;
		hours.value = matches[2] ? parseInt(matches[2]) : 0;
		minutes.value = matches[3] ? parseInt(matches[3]) : 0;
		seconds.value = matches[4] ? parseInt(matches[4]) : 0;
		updateFormattedDuration();
	}
};

const updateFormattedDuration = () => {
	formattedDuration.value = `${days.value}d ${hours.value}h ${minutes.value}m ${seconds.value}s`
		.replace(/0[d|h|m|s]\s*/g, "")
		.trim();
	emit("update:modelValue", formattedDuration.value);
	emit("update:seconds", convertToSeconds());
};

const updateDuration = (value) => {
	parseDuration(value);
};

const convertToSeconds = () => {
	return days.value * 24 * 60 * 60 + hours.value * 60 * 60 + minutes.value * 60 + seconds.value;
};

const handleClickOutside = (event) => {
	if (durationContainer.value && !durationContainer.value.contains(event.target)) {
		showFields.value = false;
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
		parseDuration(newVal);
	},
	{ immediate: true }
);
</script>

<style scoped>
.duration-input {
	position: relative;
}

.duration-fields {
	position: absolute;
	background: white;
	border: 1px solid #ccc;
	padding: 10px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	display: flex;
	gap: 5px;
	margin-top: -10px;
}

.inline-fields {
	display: flex;
	align-items: flex-end; /* Adjusted alignment */
	gap: 10px;
}

.field-container {
	display: flex;
	flex-direction: column;
	align-items: center;
}

.input-field-small {
	width: 50px;
	padding: 5px;
	border: 1px solid #ccc;
	border-radius: 5px;
	text-align: center;
}
</style>
