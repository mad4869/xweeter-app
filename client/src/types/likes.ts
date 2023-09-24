type Likes = {
    like_id: number,
    user_id: number,
    xweet_id: number,
    created_at: string,
    updated_at?: string
}

type LikeResponse = {
    data: Likes,
    success: boolean
}

export { type LikeResponse }