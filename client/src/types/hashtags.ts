type Hashtags = {
    hashtag_id: number,
    body: string
}

type HashtagResponse = {
    success: boolean,
    data: Hashtags[]
}

export { type HashtagResponse }