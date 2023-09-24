interface Likes {
    like_id: number,
    user_id: number,
    xweet_id: number,
    created_at: string,
    updated_at?: string
}

interface LikesFull extends Likes {
    body: string,
    media?: string,
    username: string,
    full_name: string,
    profile_pic: string,
    og_user_id: number,
    og_username: string,
    og_full_name: string,
    og_profile_pic: string
}

type LikeResponse = {
    data: Likes,
    success: boolean
}

type LikesFullResponse = {
    data: LikesFull[]
    success: boolean
}

export { type LikeResponse, type LikesFull, type LikesFullResponse }