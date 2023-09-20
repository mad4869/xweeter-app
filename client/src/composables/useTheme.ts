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
        },
        resetToDark() {
            this.theme = ThemeState.Dark
        }
    }
})

export default useTheme