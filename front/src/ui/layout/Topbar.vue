<script setup lang="ts">
import {ref} from 'vue'
import {Bell, LogOut, Moon, Sun, UserRound} from 'lucide-vue-next'
import {useThemeStore} from '@/shared/ui/theme.store'
import UiButton from '@/ui/components/common/UiButton.vue'
import IconBot from '@/ui/components/common/icons/IconBot.vue'

const emit = defineEmits<{
  (event: 'logout'): void
}>()

const hasNotifications = ref(false)
const showDropdown = ref(false)

const themeStore = useThemeStore()

function toggleDropdown(): void {
  showDropdown.value = !showDropdown.value
}

function logout(): void {
  showDropdown.value = false
  emit('logout')
}

function toggleTheme(): void {
  themeStore.toggleTheme()
}
</script>

<template>
  <header class="topbar">
    <div class="topbar__inner">
      <RouterLink to="/" class="topbar__brand">
        <IconBot class="topbar__brand-icon" />
        <span>Domain Expiration Bot</span>
      </RouterLink>

      <nav class="topbar__nav">
        <RouterLink to="/domains" class="topbar__link" active-class="topbar__link--active">
          Domains
        </RouterLink>
        <RouterLink
          to="/integrations"
          class="topbar__link"
          active-class="topbar__link--active"
        >
          Integrations
        </RouterLink>
        <RouterLink to="/logs" class="topbar__link" active-class="topbar__link--active">
          Logs
        </RouterLink>
      </nav>

      <div class="topbar__actions">
        <button type="button" class="topbar__icon-btn" @click="toggleTheme">
          <Sun v-if="themeStore.theme === 'dark'" :size="18" />
          <Moon v-else :size="18" />
        </button>

        <button type="button" class="topbar__icon-btn topbar__icon-btn--notification">
          <Bell :size="18" />
          <span v-if="hasNotifications" class="topbar__dot" />
        </button>

        <div class="topbar__profile">
          <button type="button" class="topbar__icon-btn" @click="toggleDropdown">
            <UserRound :size="18" />
          </button>

          <div v-if="showDropdown" class="topbar__dropdown">
            <UiButton size="sm" variant="ghost" @click="logout">
              <LogOut :size="14" />
              Logout
            </UiButton>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.topbar {
  position: sticky;
  top: 0;
  z-index: 40;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);

  &__inner {
    width: min(1200px, 100% - 2 * var(--space-4));
    margin: 0 auto;
    min-height: 64px;
    display: grid;
    gap: var(--space-4);
    align-items: center;
    grid-template-columns: auto 1fr auto;
  }

  &__brand {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    font-weight: 700;

    &-icon {
      color: var(--color-primary);
    }
  }

  &__nav {
    display: inline-flex;
    align-items: center;
    gap: var(--space-4);
  }

  &__link {
    position: relative;
    color: var(--color-text-muted);
    font-weight: 600;

    &--active,
    &:hover {
      color: var(--color-text);
    }

    &--active::after {
      content: '';
      position: absolute;
      left: 0;
      right: 0;
      bottom: -6px;
      height: 2px;
      border-radius: 999px;
      background: var(--color-primary);
    }
  }

  &__actions {
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
  }

  &__icon-btn {
    width: 36px;
    height: 36px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--color-border);
    display: inline-flex;
    align-items: center;
    justify-content: center;

    &:hover {
      background: var(--color-surface-soft);
    }

    &--notification {
      position: relative;
    }
  }

  &__dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--color-danger);
    position: absolute;
    top: 6px;
    right: 6px;
  }

  &__profile {
    position: relative;
  }

  &__dropdown {
    position: absolute;
    right: 0;
    top: calc(100% + var(--space-1));
    min-width: 150px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: var(--space-1);
    background: var(--color-surface);
    box-shadow: var(--card-shadow);
  }
}

@media (max-width: 860px) {
  .topbar {
    &__inner {
      grid-template-columns: 1fr auto;
      grid-template-areas:
        'brand actions'
        'nav nav';
      padding: var(--space-2) 0;
    }

    &__brand {
      grid-area: brand;
    }

    &__actions {
      grid-area: actions;
      justify-self: end;
    }

    &__nav {
      grid-area: nav;
      overflow-x: auto;
      padding-bottom: var(--space-1);
    }
  }
}
</style>
