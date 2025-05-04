import storage from "@/utils/storage";

// Пример функции проверки авторизации
export const checkIfUserIsAuthenticated = () => {
    // Вариант 1: Проверка наличия токена в localStorage
    const token = storage.auth.getToken()
    return !!token

    // Вариант 2: Проверка через хранилище Vuex/Pinia
    // return store.getters.isAuthenticated

    // Вариант 3: Проверка через глобальное состояние авторизации
    // return auth.isLoggedIn
}
