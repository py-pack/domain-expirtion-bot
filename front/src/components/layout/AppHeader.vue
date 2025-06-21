<script setup lang="ts">
import {ref} from 'vue';
import {useRouter} from 'vue-router'
import IconBell from '../icons/IconBell.vue';
import IconUser from '../icons/IconUser.vue';
import IconBot from '../icons/IconBot.vue';
import {logout} from '@/api/auth.ts'

const hasNotifications = ref(false);

const showDropdown = ref(false)
const router = useRouter()

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const handleLogout = async () => {
  await logout()
}
</script>

<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="header-logo">
          <router-link to="/" class="logo-link">
            <IconBot class="logo-icon"/>
            <span class="logo-text">DOMAIN EXPIRATION BOT</span>
          </router-link>
        </div>

        <nav class="header-nav">
          <ul class="nav-items">
            <li class="nav-item">
              <router-link to="/domains">Domains</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/integrations">Integrations</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/logs">Logs</router-link>
            </li>
          </ul>
        </nav>

        <div class="header-actions">
          <button class="btn-icon-only notification-btn">
            <IconBell/>
            <span v-if="hasNotifications" class="notification-badge"></span>
          </button>

          <div class="dropdown-wrapper">
            <button class="user-profile" @click="toggleDropdown">
              <IconUser/>
            </button>

            <div v-if="showDropdown" class="dropdown-menu">
              <button class="dropdown-item" @click="handleLogout">Logout</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style lang="scss" scoped>
.header {
  background-color: var(--color-surface);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  height: 64px;
}

.header-logo {
  margin-right: var(--spacing-8);

  .logo-link {
    display: flex;
    align-items: center;
    font-weight: 700;
    color: var(--color-text);
  }

  .logo-icon {
    margin-right: var(--spacing-2);
    color: var(--color-primary);
  }

  .logo-text {
    font-size: var(--font-size-lg);
    font-weight: 600;
  }
}

.header-nav {
  flex: 1;

  .nav-items {
    display: flex;
    gap: var(--spacing-6);
  }

  .nav-item {
    a {
      display: block;
      padding: var(--spacing-2) 0;
      color: var(--color-text-secondary);
      position: relative;
      font-weight: 500;
      transition: color var(--transition-normal) ease;

      &::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 100%;
        height: 2px;
        background-color: var(--color-primary);
        transform: scaleX(0);
        transition: transform var(--transition-normal) ease;
      }

      &:hover,
      &.active {
        color: var(--color-text);
      }

      &.active::after {
        transform: scaleX(1);
      }
    }
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.notification-btn {
  position: relative;

  .notification-badge {
    position: absolute;
    top: 0;
    right: 0;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--color-error);
  }
}

.user-profile {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border);
  overflow: hidden;
  transition: border-color var(--transition-normal) ease;

  &:hover {
    border-color: var(--color-primary);
  }
}

.dropdown-wrapper {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 120px;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 999;
  padding: 4px 0;
}

.dropdown-item {
  width: 100%;
  padding: 8px 16px;
  text-align: left;
  background: none;
  border: none;
  font-size: 14px;
  color: var(--color-text);
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    color: var(--color-surface-hover, #f5f5f5);
  }
}

@media (max-width: 768px) {
  .header-content {
    justify-content: space-between;
  }

  .header-logo {
    .logo-text {
      display: none;
    }
  }

  .header-nav {
    .nav-items {
      gap: var(--spacing-4);
    }
  }
}
</style>