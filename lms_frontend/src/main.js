import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import { QuillEditor } from "@vueup/vue-quill";
import VTooltip from "v-tooltip";
import { useCourseStore } from "@/stores/teacherStore/courseStore"; 

import "@vueup/vue-quill/dist/vue-quill.snow.css";

const pinia = createPinia();
const app = createApp(App);

app.use(pinia);
app.use(VTooltip);
app.use(router);

app.component("QuillEditor", QuillEditor);

app.mount("#app");

const courseStore = useCourseStore(pinia);
courseStore.loadSelectedCourse();
