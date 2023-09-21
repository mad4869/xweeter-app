enum UserAuth {
    SignUp,
    SignIn
}

type User = {
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

type AuthResponseUser = {
    success: boolean
    message: string,
    user: User
}

type AuthResponseWoUser = {
    success: boolean
    message: string,
}

export { UserAuth, type AuthResponseUser, type AuthResponseWoUser }