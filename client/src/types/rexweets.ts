type Rexweets = {
    rexweet_id: number,
    user_id: number,
    xweet_id: number,
    created_at: string,
    updated_at?: string
}

type RexweetResponse = {
    data: Rexweets,
    success: boolean
}

export { type RexweetResponse }