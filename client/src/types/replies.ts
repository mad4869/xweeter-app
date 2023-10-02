type Reply = {
    reply_id: number
    user_id: number
    xweet_id: number
    body: string
    media?: string
    created_at: string
    updated_at?: string
    username: string
    full_name: string
    profile_pic: string
    og_user_id: string
    og_username: string
    og_full_name: string
    og_profile_pic: string
    og_body: string,
    og_media?: string,
}

type RepliesResponse = {
    data: Reply[]
    success: boolean
}

export { type RepliesResponse }