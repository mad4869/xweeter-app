import { AuthResponse } from './auth'

type UserResponse = Omit<AuthResponse, 'message'>

type TopDailyUser = {
    user_id: number
    username: string
    full_name: string
    xweet_count: number
}

type TopDailyResponse = {
    data: TopDailyUser[]
    success: boolean
}

export { type UserResponse, type TopDailyUser, type TopDailyResponse }