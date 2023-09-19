import { defineStore } from 'pinia'
import { AxiosError } from 'axios'
import { authService, sendReqCookie } from '../utils/axiosInstances'

type AuthState = {
    isAuthenticated: boolean,
    signedInUserId: number | undefined,
    signedInUsername: string | undefined
    signedInFullname: string | undefined,
    signedInEmail: string | undefined,
    signedInBio: string | undefined | null,
    signedInRole: 'admin' | 'user' | undefined,
    signedInPfp: string | undefined,
    signedInHeader: string | undefined,
    signedInJoindate: string | undefined,
    signedInUpdate: string | undefined | null
  }

export type User = {
    user_id: number,
    username: string,
    full_name: string,
    email: string,
    bio: string | null,
    role: 'admin' | 'user',
    profile_pic: string,
    header_pic: string,
    created_at: string,
    updated_at: string | null
}

type AuthResponse = {
    success: boolean
    message: string,
    user: User
}

const useAuth = defineStore('auth', {
        state: () => ({
            isAuthenticated: false,
            signedInUserId: undefined,
            signedInUsername: undefined,
            signedInFullname: undefined,
            signedInEmail: undefined,
            signedInBio: undefined,
            signedInRole: undefined,
            signedInPfp: undefined,
            signedInHeader: undefined,
            signedInJoindate: undefined,
            signedInUpdate: undefined
        } as AuthState),
        getters: {
            getIsAuthenticated: state => state.isAuthenticated,
            getSignedInUserId: state => state.signedInUserId,
            getSignedInUsername: state => state.signedInUsername,
            getSignedInFullname: state => state.signedInFullname,
            getSignedInEmail: state => state.signedInEmail,
            getSignedInBio: state => state.signedInBio,
            getSignedInRole: state => state.signedInRole,
            getSignedInPfp: state => state.signedInPfp,
            getSignedInHeader: state => state.signedInHeader,
            getSignedInJoindate: state => state.signedInJoindate,
            getSignedInUpdate: state => state.signedInUpdate
        },
        actions: {
            async signin(credentials: { username: string, password: string }) {
                try {
                    const { data } = await authService.post<AuthResponse | undefined>('/api/signin', credentials)
                    if (data?.success) {
                        this.isAuthenticated = true
                        this.signedInUserId = data.user.user_id
                        this.signedInUsername = data.user.username
                        this.signedInFullname = data.user.full_name
                        this.signedInEmail = data.user.email
                        this.signedInBio = data.user.bio
                        this.signedInRole = data.user.role
                        this.signedInPfp = data.user.profile_pic
                        this.signedInHeader = data.user.header_pic
                        this.signedInJoindate = data.user.created_at
                        this.signedInUpdate = data.user.updated_at
                    }
                } catch (error) {
                    const err = error as AxiosError
                    console.error(err.message)

                    if (err.response?.status === 401) {
                        this.isAuthenticated = false
                        this.signedInUserId = undefined
                        this.signedInUsername = undefined
                        this.signedInFullname = undefined
                        this.signedInEmail = undefined
                        this.signedInBio = undefined
                        this.signedInRole = undefined
                        this.signedInPfp = undefined
                        this.signedInHeader = undefined
                        this.signedInJoindate = undefined
                        this.signedInUpdate = undefined
                    }
                }
            },
            async getUser() {
                try {
                    const { data } = await sendReqCookie.get<AuthResponse | undefined>('/api/signed-in')
                    if (data?.success) {
                        this.isAuthenticated = true
                        this.signedInUserId = data.user.user_id
                        this.signedInUsername = data.user.username
                        this.signedInFullname = data.user.full_name
                        this.signedInEmail = data.user.email
                        this.signedInBio = data.user.bio
                        this.signedInRole = data.user.role
                        this.signedInPfp = data.user.profile_pic
                        this.signedInHeader = data.user.header_pic
                        this.signedInJoindate = data.user.created_at
                        this.signedInUpdate = data.user.updated_at
                    }
                } catch (error) {
                    const err = error as AxiosError
                    console.error(err.message)

                    if (err.response?.status === 401) {
                        this.isAuthenticated = false
                        this.signedInUserId = undefined
                        this.signedInUsername = undefined
                        this.signedInFullname = undefined
                        this.signedInEmail = undefined
                        this.signedInBio = undefined
                        this.signedInRole = undefined
                        this.signedInPfp = undefined
                        this.signedInHeader = undefined
                        this.signedInJoindate = undefined
                        this.signedInUpdate = undefined
                    }
                }
            },
            async signout() {
                try {
                    const { data } = await sendReqCookie.post<AuthResponse | undefined>('/api/signout', '')
                    if (data?.success) {
                        this.isAuthenticated = false
                        this.signedInUserId = undefined
                        this.signedInUsername = undefined
                        this.signedInFullname = undefined
                        this.signedInEmail = undefined
                        this.signedInBio = undefined
                        this.signedInRole = undefined
                        this.signedInPfp = undefined
                        this.signedInHeader = undefined
                        this.signedInJoindate = undefined
                        this.signedInUpdate = undefined
                    }
                } catch (err) {
                    console.error(err)
                }
            }
        },
    })

export default useAuth