enum UpdateTimeline {
    Add,
    Delete,
    Restore
}

type ProfileTimeline = {
    xweet_id: number
    user_id: number
    username: string
    full_name: string
    body: string
    media?: string
    profile_pic: string
    created_at: string
    updated_at?: string
    rexweet_id?: number
    og_user_id?: number
    og_username?: string
    og_full_name?: string
    og_profile_pic?: string
}

type ProfileTimelineResponse = {
    data: ProfileTimeline[]
    success: boolean
}

export { UpdateTimeline, type ProfileTimeline, type ProfileTimelineResponse }