import { defineStore } from 'pinia'
import axios from 'axios'

type AuthState = {
    isAuthenticated: boolean;
    signedInUserId: number | null;
    signedInUsername: string | null;
  }

type AuthResponse = {
    success: boolean
    message: string,
    user: {
        user_id: number,
        username: string
    }
}

const BASE_URL = 'http://localhost:5000/api'

const useAuth = defineStore('auth', {
        state: () => ({
            isAuthenticated: false,
            signedInUserId: null,
            signedInUsername: null,
        } as AuthState),
        getters: {
            getIsAuthenticated: state => state.isAuthenticated,
            getSignedInUserId: state => state.signedInUserId,
            getSignedInUsername: state => state.signedInUsername
        },
        actions: {
            async signin(credentials: { username: string, password: string }) {
                try {
                    const { data } = await axios.post<AuthResponse | undefined>(`${BASE_URL}/signin`, credentials)
                    if (data?.success) {
                        this.isAuthenticated = true
                        this.signedInUserId = data.user.user_id
                        this.signedInUsername = data.user.username
                    }
                } catch (err) {
                    console.error(err)
                }
            },
            async signout() {
                try {
                    const { data } = await axios.post<AuthResponse | undefined>(`${BASE_URL}/signout`)
                    if (data?.success) {
                        this.isAuthenticated = false
                        this.signedInUserId = null
                        this.signedInUsername = null
                    }
                } catch (err) {
                    console.error(err)
                }
            }
        },
    })

export default useAuth