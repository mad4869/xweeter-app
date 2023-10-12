import { reactive } from "vue";

export const countStore = reactive({
    xweetsCount: 0,
    incrementXweetsCount() {
        this.xweetsCount++
    },
    repliesCount: 0,
    incrementRepliesCount() {
        this.repliesCount++
    }
})