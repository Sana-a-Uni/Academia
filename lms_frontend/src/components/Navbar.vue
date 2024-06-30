<template>
  <header class="navbar">
    <div class="navbar-left">
      <button class="drawer-toggle" @click="$emit('toggle-drawer')">
        <font-awesome-icon icon="bars" class="bars-icon" />
      </button>
      <img src="@/assets/images/logo.png" alt="Logo" class="logo" />
    </div>
    <div class="navbar-right">
      <div class="user-menu" @click="toggleDropdown">
        <img src="@/assets/images/Icon.png" alt="User Avatar" class="avatar" />
        <div class="user-details">
          <h2 class="user-name">Student Name</h2>
          <span class="user-major">Computer Science</span>
        </div>
        <font-awesome-icon icon="caret-down" class="caret-icon" />
        <div class="dropdown" :class="{ open: isDropdownOpen }">
          <div class="dropdown-menu">
            <div class="user-details-dropdown">
              <img
                src="@/assets/images/Icon.png"
                alt="User Avatar"
                class="avatar-dropdown"
              />
              <div>
                <h2 class="user-name">Student Name</h2>
                <span class="user-major">Computer Science</span>
              </div>
            </div>
            <a href="#"
              ><font-awesome-icon icon="user" class="dropdown-icon" />
              <span>Profile</span></a
            >
            <a href="#"
              ><font-awesome-icon icon="cog" class="dropdown-icon" />
              <span>Settings</span></a
            >
            <a href="#"
              ><font-awesome-icon icon="sign-out-alt" class="dropdown-icon" />
              <span>Logout</span></a
            >
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faBars,
  faUser,
  faCog,
  faSignOutAlt,
  faCaretDown,
} from "@fortawesome/free-solid-svg-icons";

library.add(faBars, faUser, faCog, faSignOutAlt, faCaretDown);

const isDropdownOpen = ref(false);

const toggleDropdown = (event) => {
  isDropdownOpen.value = !isDropdownOpen.value;
  event.stopPropagation();
};

const handleClickOutside = (event) => {
  const userMenu = document.querySelector(".user-menu");
  if (userMenu && !userMenu.contains(event.target)) {
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  background-color: #f4f4f4;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px;
  margin: auto 0;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  cursor: pointer;
}

.avatar {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-right: -5px;
}

.user-details {
  display: flex;
  flex-direction: column;
  margin-left: 0;
}

.user-name {
  font-size: 14px;
}

.user-major {
  font-size: 10px;
}

.caret-icon {
  margin-left: 10px;
}

.dropdown {
  position: relative;
}

.dropdown-menu {
  display: none;
  position: absolute;
  right: 0;
  top: calc(100% + 5px); /* Adjust this value to move the dropdown closer */
  background-color: #fff;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  z-index: 1001;
  padding: 10px 0;
  width: 200px;
}

.dropdown.open .dropdown-menu {
  display: block;
}

.user-details-dropdown {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  border-bottom: 1px solid #ddd;
}

.avatar-dropdown {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.user-details-dropdown .user-name {
  font-weight: bold;
  margin-bottom: 0px;
  line-height: 1;
}

.user-details-dropdown .user-major {
  font-size: 12px;
  color: #666;
  margin-top: 0px;
  line-height: 1;
}

.dropdown-menu a {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  color: #333;
  text-decoration: none;
}

.dropdown-menu a:hover {
  background-color: #f4f4f4;
}

.dropdown-menu a font-awesome-icon {
  margin-right: 10px;
}

.dropdown-menu a span {
  margin-left: 10px;
}

.dropdown-menu .dropdown-icon {
  color: #0584ae;
}

.bars-icon,
.dropdown-icon,
.caret-icon {
  font-size: 1em;
  margin-right: 10px;
  font-size: 16px;
  width: 16px;
  height: 16px;
}

.drawer-toggle {
  display: none;
}

@media (max-width: 768px) {
  .user-details-dropdown {
    display: flex;
  }

  .avatar-dropdown {
    display: inline;
  }

  .user-details {
    display: none;
  }

  .navbar-left {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .logo {
    margin: 0 auto;
  }

  .drawer-toggle {
    display: block;
    font-size: 1.5em;
  }
}

@media (min-width: 769px) {
  .user-details {
    display: flex;
    align-items: center;
    margin-left: 10px;
  }

  .user-details-dropdown {
    display: none;
  }

  .avatar-dropdown {
    display: none;
  }

  .drawer-toggle {
    display: none;
  }
}
</style>
