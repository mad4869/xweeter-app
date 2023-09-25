import { AuthResponse } from './auth'

type UserResponse = Omit<AuthResponse, 'message'>

export { type UserResponse }