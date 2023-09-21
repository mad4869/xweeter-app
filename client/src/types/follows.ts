import { Users } from "./auth";

type FollowResponse = {
    success: boolean,
    data: Users[]
}

export { type FollowResponse }