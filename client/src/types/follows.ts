import { User } from "./auth";

type FollowResponse = {
    following: {
        success: boolean,
        data: User[]
    },
    followers: {
        success: boolean,
        data: User[]
    },
}

type WhoToFollow = {
    user_id: number,
    username: string,
    full_name: string,
    body: string,
    profile_pic: string
}

type WhoToFollowResponse = {
    data: WhoToFollow[],
    success: boolean
}

type ToFollowResponse = {
    message: string,
    success: boolean
}

export { type FollowResponse, type WhoToFollowResponse, type ToFollowResponse }