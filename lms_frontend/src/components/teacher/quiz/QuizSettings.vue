<template>
  <div class="container">
    <h1>Quiz Settings</h1>
    <form @submit.prevent="saveSettings">
      <div class="form-section">
        <div class="section-header">
          <input
            id="availability-check"
            type="checkbox"
            @change="toggleSection('date-inputs')"
            style="
              width: 14px;   
              height: 14px;
              transform: scale(1.2);
              margin-right: 5px;
            "
          />
          <label for="availability-check">Availability</label>
        </div>
        <div
          :class="[
            'date-input',
            { active: availabilityActive, faded: !availabilityActive },
          ]"
          id="date-inputs"
        >
          <div class="inline-fields">
            <div class="from-date">
              <h4 style=" margin-top:9px;  margin-right:15px;">From</h4>
              <input type="date" placeholder="From Date" class="input-field" />
            </div>
            <div class="from-date">
              <h4 style=" margin-top:9px;  margin-right:15px; margin-left:10px">To</h4>
              <input type="date" placeholder="To Date" class="input-field" />
            </div>
          </div>
        </div>
      </div>

      <div class="form-section">
        <div class="section-header">
          <input
            id="time-limit-check"
            type="checkbox"
            @change="toggleSection('time-input')"
            style="
              width: 14px;
              height: 14px;
              transform: scale(1.2);
              margin-right: 5px;
            "
          />
          <label for="time-limit-check">Time Limit</label>
        </div>
        <div
          :class="[
            'time-input',
            { active: timeLimitActive, faded: !timeLimitActive },
          ]"
          id="time-input"
        >
          <input type="time" placeholder="Enter the time" class="input-field" />
        </div>
      </div>

      <div class="form-section">
        <div class="section-header">
          <input
            id="multiple-attempt-check"
            type="checkbox"
            @change="toggleSection('attempt-input')"
            style="
              width: 14px;
              height: 14px;
              transform: scale(1.2);
              margin-right: 5px;
            "
          />
          <label for="multiple-attempt-check">Multiple Attempt</label>
        </div>
        <div
          :class="[
            'attempt-input',
            { active: multipleAttemptActive, faded: !multipleAttemptActive },
          ]"
          id="attempt-input"
        >
          <input
            type="number"
            placeholder="Enter the number of attempts"
            class="input-field"
          />
        </div>
      </div>

      <div class="form-section">
        <div class="section-header">
          <input
            id="student-group-check"
            type="checkbox"
            @change="toggleSection('group-input')"
            style="
              width: 14px;
              height: 14px;
              transform: scale(1.2);
              margin-right: 5px;
            "
          />
          <label for="student-group-check">Student Group</label>
        </div>
        <div
          :class="[
            'group-input',
            { active: studentGroupActive, faded: !studentGroupActive },
          ]"
          id="group-input"
        >
          <select class="input-field">
            <option value="" disabled selected>Select Group</option>
            <option value="group1">Group 1</option>
            <option value="group2">Group 2</option>
            <option value="group3">Group 3</option>
          </select>
        </div>
      </div>

      <div class="form-section">
        <div class="section-header">
          <input
            id="student-check"
            type="checkbox"
            @change="toggleSection('student-section')"
            style="
             width: 14px;
              height: 14px;
              transform: scale(1.2);
              margin-right: 5px;
            "
          />
          <label for="student-check">Student</label>
        </div>
        <div
          :class="[
            'main-content',
            { active: studentActive, faded: !studentActive },
          ]"
          id="student-section"
        >
          <div  style="margin-left:20px;" class="header">
            <div class="search-bar">
              <input
                type="text"
                id="search"
                placeholder="Search"
                v-model="searchTerm"
                class="input-field"
              />
              <select class="input-field2">
                <option value="" disabled selected>Select Group</option>
                <option value="group1">Group 1</option>
                <option value="group2">Group 2</option>
                <option value="group3">Group 3</option>
              </select>
            </div>
          </div>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th style="font-size:14px;">Select</th>
                  <th style="font-size:14px;">Student Name</th>
                  <th style="font-size:14px;">Group Name</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in filteredItems" :key="item.studentname">
                  <td><input style="width: 18px;
              height: 18px;" type="checkbox" /></td>
                  <td style="font-size:13px;">{{ item.studentname }}</td>
                  <td style="font-size:13px;">{{ item.groupname }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="card-actions">
      <button class="prev-btn" @click="previousPage">Previous</button>
        <button class="save-btn" type="submit">Save</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits } from "vue";

const emit = defineEmits(["go-back"]);

const searchTerm = ref("");
const availabilityActive = ref(false);
const timeLimitActive = ref(false);
const multipleAttemptActive = ref(false);
const studentGroupActive = ref(false);
const studentActive = ref(false);

const items = ref([
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 1" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 2" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 1" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 3" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 3" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 1" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 2" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 1" },
  { studentname: "Khawla Ameen Alareeqi", groupname: "Group 1" },
]);

const filteredItems = computed(() =>
  items.value.filter((item) =>
    item.studentname.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
);

const saveSettings = () => {
  console.log("Settings Saved:");
  console.log({
    availabilityActive: availabilityActive.value,
    timeLimitActive: timeLimitActive.value,
    multipleAttemptActive: multipleAttemptActive.value,
    studentGroupActive: studentGroupActive.value,
    studentActive: studentActive.value,
  });
};

const previousPage = () => {
  // Emit event to parent to change the view to QuizInformation
  emit("go-back");
};

const toggleSection = (inputId) => {
  switch (inputId) {
    case "date-inputs":
      availabilityActive.value = !availabilityActive.value;
      break;
    case "time-input":
      timeLimitActive.value = !timeLimitActive.value;
      break;
    case "attempt-input":
      multipleAttemptActive.value = !multipleAttemptActive.value;
      break;
    case "group-input":
      studentGroupActive.value = !studentGroupActive.value;
      break;
    case "student-section":
      studentActive.value = !studentActive.value;
      break;
  }
};
</script>

<style scoped>
.container {
  max-width: 100%;
  margin: 0 auto;
  padding: 10px;
  background-color: #fff;
  box-shadow: 0 0 rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

h1 {
  text-align: center;
  margin-bottom: 0px;
  font-size: 24px;
}

.form-section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
}
.from-date{
  display: flex;
  display-content:column;
  width:100%;

}

.section-header input {
  margin-right: 5px;
  margin-top: 20px;
}

.section-header label {
  font-size: 17px;
  margin-left: 10px;
}

h3 {
  margin: 0;
  font-size: 14px;
}


.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 12px;
}

.date-input,
.time-input,
.attempt-input,
.group-input {
  opacity: 0.5;
  display: block;
  pointer-events: none;
  margin-left: 20px;
}

.date-input.active,
.time-input.active,
.attempt-input.active,
.group-input.active {
  opacity: 1;
  pointer-events: auto;
}

.inline-fields {
  display: flex;
  gap: 10px;
  align-items: center;
}

.inline-fields h4 {
  margin: 0 5px 0 0;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 15%;
  font-size: 14px;
}

.prev-btn {
  background-color: #0584ae;
}

.save-btn {
  background-color: #0584ae;
}

.prev-btn:hover,
.save-btn:hover {
  opacity: 0.9;
}

.main-content .header .search-bar input {
  font-size: 14px;
}

.main-content table {
  width: 100%;
  border-collapse: collapse;
  background-color: #f0f5f9;
  border-radius: 10px;
  overflow: hidden;
}

.main-content table thead th,
.main-content table tbody td {
  padding: 8px;
  font-size: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.main-content table thead {
  background-color: #e0e6ed;
}

.main-content table tbody tr:nth-child(even) {
  background-color: #f9fafc;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
 
}
.search-bar {
  display: flex;
  align-items: flex-start;
  margin-top: 10px;
}

.search-bar input {
  width: 180px;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
  margin-top: 0;
  font-size: 12px;
}

.search-bar select {
  width: 150px;
  height: 30px;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 12px;
}

.table-container {
  max-height: 400px;
  overflow-y: auto;
}
</style>
