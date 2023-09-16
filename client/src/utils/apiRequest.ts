import axios from 'axios'

const getCookie = (name: string) => {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop()?.split(';').shift() ?? undefined
}

const COOKIE_TOKEN_CONFIG = {
    credentials: 'same-origin',
    headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token')
    }
}

const apiRequest = axios.create(COOKIE_TOKEN_CONFIG)

export default apiRequest