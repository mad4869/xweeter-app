import { reactive } from "vue";

export const countStore = reactive({
    xweetsCount: 0,
    incrementXweetsCount() {
        this.xweetsCount++
    },
    decrementXweetsCount() {
        this.xweetsCount--
    },
    repliesCount: 0,
    incrementRepliesCount() {
        this.repliesCount++
    },
    decrementRepliesCount() {
        this.repliesCount--
    }
})