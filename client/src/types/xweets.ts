type Xweets = {
    xweet_id: number,
    user_id: number,
    full_name: string,
    username: string,
    body: string,
    media?: string,
    profile_pic: string,
    created_at: string,
    updated_at?: string
}

type XweetResponse = {
    data: Xweets,
    success: boolean
}

type XweetsResponse = {
    data: Xweets[],
    success: boolean
}

export { type XweetResponse, type XweetsResponse }
