import { baseurl } from "./baseurl"
import refreshAPI from "./refresh"

export default async function logoutAPI() {
  const url = '/api/v1/logout'
  const response = await refreshAPI(
    async () => await fetch(baseurl + url, {
      method: "post"
    })
  )
  return response
}

