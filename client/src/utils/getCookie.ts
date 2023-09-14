export default function getCookie(name: string) {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    console.log(parts, parts.length, document.cookie)
    if (parts.length === 2) return parts.pop()?.split(';').shift() ?? undefined
  }
  