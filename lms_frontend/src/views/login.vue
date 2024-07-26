<template>
	<div class="login-container">
		<div class="login-form">
			<img src="@/assets/images/logo.png" alt="Logo" class="logo" />
			<h3>Login to LMS</h3>
			<form @submit.prevent="handleLogin">
				<div class="input-group">
					<font-awesome-icon :icon="['fas', 'user']" class="icon" />
					<input
						id="email"
						v-model="email"
						type="text"
						required
						placeholder="Enter your email"
					/>
				</div>
				<div class="input-group">
					<font-awesome-icon :icon="['fas', 'lock']" class="icon" />
					<input
						id="password"
						v-model="password"
						:type="passwordVisible ? 'text' : 'password'"
						required
						placeholder="Enter your password"
					/>
					<font-awesome-icon
						:icon="passwordVisible ? ['fas', 'eye-slash'] : ['fas', 'eye']"
						class="toggle-password-icon"
						@click="togglePasswordVisibility"
					/>
				</div>
				<button type="submit" class="login-button">LOGIN</button>
			</form>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faUser, faLock, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

library.add(faUser, faLock, faEye, faEyeSlash);

const email = ref("");
const password = ref("");
const passwordVisible = ref(false);

const handleLogin = () => {
	if (!email.value || !password.value) {
		alert("Please fill in both the student ID and password.");
	} else {
		alert(`Logging in with student ID: ${email.value}`);
	}
};

const togglePasswordVisibility = () => {
	passwordVisible.value = !passwordVisible.value;
};
</script>

<style scoped>
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
}

.login-container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
	background: #e0e0e0;
	padding: 0 50px;
}

.login-form {
	max-width: 400px;
	width: 100%;
	background: white;
	padding: 20px;
	border-radius: 8px;
	box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
	text-align: center;
}

.logo {
	max-width: 100px;
	margin-bottom: -15px;
}

.login-form h3 {
	margin-bottom: 20px;
}

.input-group {
	position: relative;
	margin-bottom: 15px;
}

.input-group .icon {
	position: absolute;
	left: 10px;
	top: 50%;
	transform: translateY(-50%);
	color: black;
}

.input-group input {
	width: 100%;
	padding: 10px 10px 10px 40px;
	border: 1px solid #ddd;
	border-radius: 4px;
	box-sizing: border-box;
	background: #f0f0f0;
}

.toggle-password-icon {
	position: absolute;
	right: 10px;
	top: 50%;
	transform: translateY(-50%);
	cursor: pointer;
	color: black;
}

.login-button {
	width: 100%;
	padding: 10px;
	background: black;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
}

.login-button font-awesome-icon {
	margin-right: 8px;
}
</style>
