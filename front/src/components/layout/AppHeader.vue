<script setup lang="ts">
import { ref } from 'vue';
import IconBell from '../icons/IconBell.vue';
import IconUser from '../icons/IconUser.vue';
import IconBot from '../icons/IconBot.vue';

const hasNotifications = ref(true);
</script>

<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="header-logo">
          <router-link to="/" class="logo-link">
            <IconBot class="logo-icon" />
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
            <IconBell />
            <span v-if="hasNotifications" class="notification-badge"></span>
          </button>
          
          <button class="user-profile">
            <IconUser />
          </button>
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