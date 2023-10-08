type Xweet = {
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
    data: Xweet,
    success: boolean
}

type XweetsResponse = {
    data: Xweet[],
    success: boolean
}

enum XweetMode {
    NewXweet,
    EditXweet,
    ReplyXweet
}

export { type Xweet, type XweetResponse, type XweetsResponse, XweetMode }
