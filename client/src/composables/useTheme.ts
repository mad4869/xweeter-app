import { defineStore } from 'pinia'

enum ThemeState {
    Light,
    Dark
}

const useTheme = defineStore('theme', {
    state: () => ({
        theme: ThemeState.Dark
    }),
    getters: {
        getTheme: state => state.theme
    },
    actions: {
        switchToLight() {
            this.theme = ThemeState.Light
            localStorage.setItem('theme', 'light')
            document.documentElement.classList.remove('dark')
        },
        resetToDark() {
            this.theme = ThemeState.Dark
            localStorage.setItem('theme', 'dark')
            document.documentElement.classList.add('dark')
        }
    }
})

export default useTheme