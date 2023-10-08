<!-- pt-4 before:absolute before:top-0 before:left-16 before:-translate-y-2 before:w-0 before:h-0 before:border-l-8 before:border-r-8 before:border-b-8 before:border-solid before:border-l-transparent before:border-r-transparent before:border-b-sky-800 -->

<!-- import { RepliesResponse } from '../../types/replies'

const { xweetId } = defineProps<{
    xweetId: number
}>() -->

<!-- <input v-else type="button" value="Reply"
                    class="px-4 py-1 bg-sky-600 text-white font-semibold rounded-md transition-colors duration-200 cursor-pointer hover:bg-sky-800 active:shadow-inner disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed"
                    :disabled="charCount > MAX_CHAR_COUNT || (charCount === 0 && !fileUrl) || isLoading" 
                    title="Send reply"
                    @mousedown.prevent="replyXweet"> -->

                    <!-- const replyXweet = async () => {
                        isLoading.value = true
                    
                        try {
                            const { data } = await sendReqCookie.post<RepliesResponse | undefined>(
                                `/api/xweets/${xweetId}/replies`, payload.value
                            )
                    
                            if (data?.success) {
                                isLoading.value = false
                                isSuccess.value = true
                                body.value = ''
                                fileUrl.value = ''
                    
                                setInterval(() => {
                                    isSuccess.value = false
                                }, 3000)
                            }
                        } catch (err) {
                            isError.value = true
                    
                            setInterval(() => {
                                isError.value = false
                            }, 3000)
                    
                            console.error(err)
                        }
                    } -->