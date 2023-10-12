import { sendReqWoCookie } from "@/utils/axiosInstances"
import { RepliesResponse } from "@/types/replies"

const useCountReplies = async (xweetId: number): Promise<number | undefined> => {
    try {
        const { data } = await sendReqWoCookie.get<RepliesResponse | undefined>(`/api/xweets/${xweetId}/replies`)
            if (data?.success) {
                return data.data.length
            }
    } catch (err) {
        console.error(err)
    }
}

export { useCountReplies }